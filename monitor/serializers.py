from rest_framework import serializers


# meta
class MetaSerializer(serializers.Serializer):
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
class RespirationSerializer(serializers.Serializer):
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
class EventSerializer(serializers.Serializer):
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
