import threading
import time
import math
import random

# lock
_lock = threading.Lock()

# defaults
_state = {
    "meta": {
        "patient_id": "HDX-00472",
        "physician": "Dr. P. Sengupta",
        "bed": "Bed 07 - ICU-B",
        "system_status": "RUNNING",
    },
    "pump": {
        "blood_flow_rate": 300,
        "dialysate_flow_rate": 500,
        "ultrafiltration_rate": 200,
        "heparin_infusion": 1200,
        "pump_state": "START",
    },
    "ecg": {
        "lead": "II",
        "heart_rate": 73,
        "sampling_rate": 25,
        "gain": "10 mm/mV",
        "rhythm": "Normal Sinus",
        "waveform": [],
    },
    "respiration": {
        "respiratory_rate": 17,
        "tidal_volume": 497,
        "waveform": [],
        "inspiratory_time": 1.4,
        "expiratory_time": 2.4,
        "ie_ratio": "1:1.7",
        "minute_ventilation": 8.4,
        "status": "Regular",
    },
    "vitals": {
        "heart_rate": 73,
        "blood_pressure": {"systolic": 120, "diastolic": 77},
        "spo2": 97,
        "temperature": 36.8,
        "respiratory_rate": 17,
    },
    "dialysate": {
        "conductivity": 14.0,
        "temperature": 37.0,
        "ph": 7.38,
        "bicarbonate": 32,
        "sodium": 140,
        "potassium": 2.0,
    },
    "session": {
        "elapsed_time": "02:14",
        "remaining_time": "01:45",
        "target_time": "04:00",
        "completion_percent": 56,
    },
    "fluid_balance": {
        "uf_removed": 2385,
        "uf_goal": 2500,
    },
    "events": [
        {"time": "10:02", "type": "info",     "message": "Session started — all systems nominal"},
        {"time": "10:18", "type": "warning",  "message": "Venous pressure slightly elevated — monitoring"},
        {"time": "10:30", "type": "success",  "message": "Heparin bolus administered (2000 units)"},
        {"time": "11:05", "type": "critical", "message": "Air detector triggered — Line checked, cleared"},
    ],
}


# read
def get_state():
    with _lock:
        import copy
        return copy.deepcopy(_state)


# write
def patch_state(section: str, payload: dict):
    with _lock:
        if section not in _state:
            return False
        if isinstance(_state[section], list):
            _state[section].extend(payload if isinstance(payload, list) else [payload])
        else:
            _state[section].update(payload)
        return True


# waveform
def _ecg_sample(t):
    base = math.sin(2 * math.pi * 1.2 * t)
    spike = 1.5 * math.exp(-50 * ((t % (1 / 1.2)) - 0.3) ** 2)
    return round(base + spike + random.uniform(-0.05, 0.05), 4)


def _resp_sample(t):
    return round(0.6 * math.sin(2 * math.pi * 0.28 * t) + random.uniform(-0.02, 0.02), 4)


def generate_wave_chunk(n=25):
    t_base = time.time()
    ecg  = [_ecg_sample(t_base + i * 0.04)  for i in range(n)]
    resp = [_resp_sample(t_base + i * 0.04) for i in range(n)]
    with _lock:
        _state["ecg"]["waveform"]         = ecg
        _state["respiration"]["waveform"] = resp
    return {
        "timestamp":       int(t_base),
        "ecg_wave_chunk":  ecg,
        "resp_wave_chunk": resp,
    }
