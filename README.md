# HD back

1. 
```bash
docker compose up --build
```

## Data Format

1. patient / session meta
```json
{
  "patient_id": "HDX-00472",
  "physician": "Dr. P. Sengupta",
  "bed": "Bed 07 - ICU-B",
  "system_status": "RUNNING"
}
```

2. pump control
```json
{
  "blood_flow_rate": 300,
  "dialysate_flow_rate": 500,
  "ultrafiltration_rate": 200,
  "heparin_infusion": 1200,
  "pump_state": "START"   // START | HOLD | STOP
}
```

3. ECG data
```json
{
  "ecg": {
    "lead": "II",
    "heart_rate": 73,
    "sampling_rate": 25,
    "gain": "10 mm/mV",
    "rhythm": "Normal Sinus",
    "waveform": []
  }
}
```

4. Respiratory Data
```json
{
  "respiration": {
    "respiratory_rate": 17,
    "tidal_volume": 497,
    "waveform": [/* signal values */],
    "inspiratory_time": 1.4,
    "expiratory_time": 2.4,
    "ie_ratio": "1:1.7",
    "minute_ventilation": 8.4,
    "status": "Regular"
  }
}
```

5. patient vitals
```json
{
  "vitals": {
    "heart_rate": 73,
    "blood_pressure": {
      "systolic": 120,
      "diastolic": 77
    },
    "spo2": 97,
    "temperature": 36.8,
    "respiratory_rate": 17
  }
}
```

6. dialystate params
```json
{
  "dialysate": {
    "conductivity": 14.0,
    "temperature": 37.0,
    "ph": 7.38,
    "bicarbonate": 32,
    "sodium": 140,
    "potassium": 2.0
  }
}
```

7. session progress
```json
{
  "session": {
    "elapsed_time": "02:14",
    "remaining_time": "01:45",
    "target_time": "04:00",
    "completion_percent": 56
  }
}
```

8. fluid balance
```json
{
  "fluid_balance": {
    "uf_removed": 2385,
    "uf_goal": 2500
  }
}
```

9. Event Log
```json
{
  "events": [
    {
      "time": "10:02",
      "type": "info",
      "message": "Session started — all systems nominal"
    },
    {
      "time": "10:18",
      "type": "warning",
      "message": "Venous pressure slightly elevated — monitoring"
    },
    {
      "time": "10:30",
      "type": "success",
      "message": "Heparin bolus administered (2000 units)"
    },
    {
      "time": "11:05",
      "type": "critical",
      "message": "Air detector triggered — Line checked, cleared"
    }
  ]
}
```

10. Streaming
```json
{
  "timestamp": 1711717171,
  "ecg_wave_chunk": [...],
  "resp_wave_chunk": [...]
}
```

### Main Backend API structure

```json
{
  "meta": {},
  "pump": {},
  "ecg": {},
  "respiration": {},
  "vitals": {},
  "dialysate": {},
  "session": {},
  "fluid_balance": {},
  "events": []
}
```
