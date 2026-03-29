import logging
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from monitor import state
from monitor.serializers import SECTION_SERIALIZERS

logger = logging.getLogger(__name__)


# ingest
class IoTIngestView(APIView):
    """
    POST /iot/ingest/
    Body: { "section": "<name>", "payload": { ... } }
    Any missing or invalid field is silently dropped — backend never breaks.
    """

    def post(self, request):
        section = request.data.get("section")
        payload = request.data.get("payload")

        # validate section
        if section not in SECTION_SERIALIZERS:
            return Response(
                {"error": f"unknown section '{section}'"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if not isinstance(payload, (dict, list)):
            return Response(
                {"error": "payload must be a JSON object or array"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # serialize
        ser_class = SECTION_SERIALIZERS[section]
        if section == "events":
            items = payload if isinstance(payload, list) else [payload]
            valid_items = []
            for item in items:
                s = ser_class(data=item)
                if s.is_valid():
                    valid_items.append(s.validated_data)
                else:
                    logger.warning("IoT event dropped: %s", s.errors)
            cleaned = valid_items
        else:
            s = ser_class(data=payload)
            if not s.is_valid():
                logger.warning("IoT payload partial errors for [%s]: %s", section, s.errors)
            cleaned = {k: v for k, v in (s.validated_data if s.is_valid() else {}).items()}

        # patch
        if cleaned:
            state.patch_state(section, cleaned)
            self._broadcast(section, cleaned)

        return Response({"status": "ok", "section": section, "accepted": bool(cleaned)})

    # broadcast
    def _broadcast(self, section, data):
        try:
            layer = get_channel_layer()
            async_to_sync(layer.group_send)(
                "monitor",
                {"type": "monitor.broadcast", "data": {section: data}},
            )
        except Exception as e:
            logger.error("WS broadcast failed: %s", e)


# bulk
class IoTBulkIngestView(APIView):
    """
    POST /iot/ingest/bulk/
    Body: { "meta": {...}, "pump": {...}, "ecg": {...}, ... }
    Each section is optional — missing ones are skipped, not errored.
    """

    def post(self, request):
        results = {}
        for section, payload in request.data.items():
            if section not in SECTION_SERIALIZERS:
                results[section] = "skipped: unknown"
                continue
            if not isinstance(payload, (dict, list)):
                results[section] = "skipped: bad type"
                continue

            ser_class = SECTION_SERIALIZERS[section]
            if section == "events":
                items = payload if isinstance(payload, list) else [payload]
                valid_items = []
                for item in items:
                    s = ser_class(data=item)
                    if s.is_valid():
                        valid_items.append(s.validated_data)
                cleaned = valid_items
            else:
                s = ser_class(data=payload)
                cleaned = s.validated_data if s.is_valid() else {}

            if cleaned:
                state.patch_state(section, cleaned)
                results[section] = "accepted"
            else:
                results[section] = "skipped: validation failed"

        # broadcast full updated state
        try:
            layer = get_channel_layer()
            async_to_sync(layer.group_send)(
                "monitor",
                {"type": "monitor.broadcast", "data": state.get_state()},
            )
        except Exception as e:
            logger.error("WS broadcast failed: %s", e)

        return Response({"status": "ok", "results": results})


# health
class IoTHealthView(APIView):
    def get(self, request):
        return Response({"status": "online"})
