| **Section**       | **Client (Patient/User)**                                                     | **Doctor**                              | **Technician**                          |
| ----------------- | ----------------------------------------------------------------------------- | --------------------------------------- | --------------------------------------- |
| **meta**          | ✅ View physician, bed, system status *(patient ID may be masked if required)* | ✅ Full access                           | ✅ Full access                           |
| **pump**          | ❌ No access                                                                   | ✅ Read-only                             | ✅ Read & Write (Full Control)           |
| **ecg**           | ❌ No access                                                                   | ✅ Full access (waveform, rhythm, HR)    | ✅ Full access                           |
| **respiration**   | ✅ Basic view *(respiratory rate only)*                                        | ✅ Full access                           | ✅ Full access                           |
| **vitals**        | ✅ Full access                                                                 | ✅ Full access                           | ✅ Full access                           |
| **dialysate**     | ❌ No access                                                                   | ✅ Read-only                             | ✅ Read & Write                          |
| **session**       | ✅ Full access                                                                 | ✅ Full access                           | ✅ Full access                           |
| **fluid_balance** | ✅ Full access                                                                 | ✅ Full access                           | ✅ Full access                           |
| **events**        | ✅ Patient-friendly events only                                                | ✅ All clinical events & alarms          | ✅ All events (clinical + technical)     |
| **streaming**     | ❌ No access                                                                   | ✅ Real-time ECG & respiratory waveforms | ✅ Real-time ECG & respiratory waveforms |
