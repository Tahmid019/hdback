from rest_framework import serializers
from .role_config import ROLE_FIELD_ACCESS


# ─── Role-aware field filtering ────────────────────────────────────────────────

class RoleAwareSerializerMixin:
    """
    It filters serializer fields based on the user's role.

    The role is passed via serializer context: context={"role": request.user.role} --> look in 'iot/views.py'
    
    Field access rules are defined in role_config.ROLE_FIELD_ACCESS.

    Usage:

        class MySerializer(RoleAwareSerializerMixin, serializers.Serializer):
            class Meta:
                section_name = "pump"        ----> name of the section whose field we want to filter
            ...

    Then instantiate with:

        MySerializer(data=payload, context={"role": request.user.role})
    """

    def get_fields(self):
        fields = super().get_fields()  # it is a dictionary of Field Objects.

        role = self.context.get("role")
        if not role:        # None means "all fields allowed"
            return fields

        section = getattr(self.Meta, "section_name", None) if hasattr(self, "Meta") else None
        if not section:     # None means "all fields allowed"
            return fields

        allowed = ROLE_FIELD_ACCESS.get(role, {}).get(section)
        if allowed is None:     # None means "all fields allowed"
            return fields

        return {k: v for k, v in fields.items() if k in allowed}

# meta
class MetaSerializer(RoleAwareSerializerMixin, serializers.Serializer):
    class Meta:
        section_name = "meta"

    patient_id    = serializers.CharField(required=False, allow_null=True)
    physician     = serializers.CharField(required=False, allow_null=True)
    bed           = serializers.CharField(required=False, allow_null=True)
    system_status = serializers.ChoiceField(
        choices=["RUNNING", "HOLD", "STOPPED", "ERROR"],
        required=False, allow_null=True,
    )


# pump
class PumpSerializer(serializers.Serializer):
    blood_flow_rate       = serializers.FloatField(required=False, allow_null=True)
    dialysate_flow_rate   = serializers.FloatField(required=False, allow_null=True)
    ultrafiltration_rate  = serializers.FloatField(required=False, allow_null=True)
    heparin_infusion      = serializers.FloatField(required=False, allow_null=True)
    pump_state            = serializers.ChoiceField(
        choices=["START", "HOLD", "STOP"],
        required=False, allow_null=True,
    )


# ecg
class EcgSerializer(serializers.Serializer):
    lead          = serializers.CharField(required=False, allow_null=True)
    heart_rate    = serializers.FloatField(required=False, allow_null=True)
    sampling_rate = serializers.IntegerField(required=False, allow_null=True)
    gain          = serializers.CharField(required=False, allow_null=True)
    rhythm        = serializers.CharField(required=False, allow_null=True)
    waveform      = serializers.ListField(
        child=serializers.FloatField(), required=False, allow_null=True, default=list
    )


# respiration
class RespirationSerializer(RoleAwareSerializerMixin, serializers.Serializer):
    class Meta:
        section_name = "respiration"

    respiratory_rate  = serializers.FloatField(required=False, allow_null=True)
    tidal_volume      = serializers.FloatField(required=False, allow_null=True)
    waveform          = serializers.ListField(
        child=serializers.FloatField(), required=False, allow_null=True, default=list
    )
    inspiratory_time  = serializers.FloatField(required=False, allow_null=True)
    expiratory_time   = serializers.FloatField(required=False, allow_null=True)
    ie_ratio          = serializers.CharField(required=False, allow_null=True)
    minute_ventilation = serializers.FloatField(required=False, allow_null=True)
    status            = serializers.CharField(required=False, allow_null=True)


# bp
class BloodPressureSerializer(serializers.Serializer):
    systolic  = serializers.FloatField(required=False, allow_null=True)
    diastolic = serializers.FloatField(required=False, allow_null=True)


# vitals
class VitalsSerializer(serializers.Serializer):
    heart_rate       = serializers.FloatField(required=False, allow_null=True)
    blood_pressure   = BloodPressureSerializer(required=False, allow_null=True)
    spo2             = serializers.FloatField(required=False, allow_null=True)
    temperature      = serializers.FloatField(required=False, allow_null=True)
    respiratory_rate = serializers.FloatField(required=False, allow_null=True)


# dialysate
class DialysateSerializer(serializers.Serializer):
    conductivity  = serializers.FloatField(required=False, allow_null=True)
    temperature   = serializers.FloatField(required=False, allow_null=True)
    ph            = serializers.FloatField(required=False, allow_null=True)
    bicarbonate   = serializers.FloatField(required=False, allow_null=True)
    sodium        = serializers.FloatField(required=False, allow_null=True)
    potassium     = serializers.FloatField(required=False, allow_null=True)


# session
class SessionSerializer(serializers.Serializer):
    elapsed_time       = serializers.CharField(required=False, allow_null=True)
    remaining_time     = serializers.CharField(required=False, allow_null=True)
    target_time        = serializers.CharField(required=False, allow_null=True)
    completion_percent = serializers.FloatField(required=False, allow_null=True)


# fluid
class FluidBalanceSerializer(serializers.Serializer):
    uf_removed = serializers.FloatField(required=False, allow_null=True)
    uf_goal    = serializers.FloatField(required=False, allow_null=True)


# event
class EventSerializer(RoleAwareSerializerMixin, serializers.Serializer):
    class Meta:
        section_name = "events"

    time    = serializers.CharField()
    type    = serializers.ChoiceField(choices=["info", "warning", "success", "critical"])
    message = serializers.CharField()


# section map — used by IoT endpoint
SECTION_SERIALIZERS = {
    "meta":          MetaSerializer,
    "pump":          PumpSerializer,
    "ecg":           EcgSerializer,
    "respiration":   RespirationSerializer,
    "vitals":        VitalsSerializer,
    "dialysate":     DialysateSerializer,
    "session":       SessionSerializer,
    "fluid_balance": FluidBalanceSerializer,
    "events":        EventSerializer,
}
