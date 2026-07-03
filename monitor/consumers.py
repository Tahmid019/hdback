import asyncio
import base64
import json
import time
from urllib.parse import parse_qs
from channels.generic.websocket import AsyncWebsocketConsumer
from . import state


def validate_supabase_jwt(token):
    if not token:
        return False
    try:
        parts = token.split('.')
        if len(parts) != 3:
            return False
        
        # Base64 padding fix
        payload_b64 = parts[1]
        missing_padding = len(payload_b64) % 4
        if missing_padding:
            payload_b64 += '=' * (4 - missing_padding)
            
        payload_bytes = base64.urlsafe_b64decode(payload_b64)
        payload = json.loads(payload_bytes.decode('utf-8'))
        
        # Check expiration
        exp = payload.get('exp')
        if exp and exp < time.time():
            return False
            
        # Verify it has standard JWT fields
        if not any(k in payload for k in ('sub', 'role', 'email')):
            return False
            
        return True
    except Exception:
        return False


class MonitorConsumer(AsyncWebsocketConsumer):
    GROUP = "monitor"

    # connect
    async def connect(self):
        query_string = self.scope.get("query_string", b"").decode("utf-8")
        query_params = parse_qs(query_string)
        token = query_params.get("token", [None])[0]

        if not validate_supabase_jwt(token):
            # Reject connection
            await self.close()
            return

        await self.channel_layer.group_add(self.GROUP, self.channel_name)
        await self.accept()
        await self.send(json.dumps({"type": "snapshot", "data": state.get_state()}))
        self._task = asyncio.ensure_future(self._push_loop())

    # disconnect
    async def disconnect(self, code):
        if hasattr(self, "_task"):
            self._task.cancel()
        await self.channel_layer.group_discard(self.GROUP, self.channel_name)

    # loop
    async def _push_loop(self):
        while True:
            await asyncio.sleep(0.04)
            chunk = await asyncio.to_thread(state.generate_wave_chunk)
            await self.send(json.dumps({"type": "wave", "data": chunk}))

    # broadcast
    async def monitor_broadcast(self, event):
        await self.send(json.dumps({"type": "update", "data": event["data"]}))

