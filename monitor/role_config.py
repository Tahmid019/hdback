"""

Role view configuration.

This is the "single edit point" for changing what each role sees from the
"monitor" API. Editing the lists/flags below and restarting the Django
process is sufficient & no other code change is required.

Keys must match top-level keys produced by :func:`monitor.state.get_state`.

"""

# --- Doctor ----------------------------------------------------------------
# Sections (top-level keys of the state snapshot) the doctor is allowed to see.
DOCTOR_SECTIONS = [
    "vitals",
    "dialysate",
    "fluid_balance",
    "session",
]

# Whether the doctor's dashboard payload includes waveform samples.
DOCTOR_INCLUDE_WAVE = False

# --- Technician ------------------------------------------------------------
# ``None`` means "all sections" (no filtering).
TECHNICIAN_SECTIONS = None
TECHNICIAN_INCLUDE_WAVE = True
TECHNICIAN_WAVE_CHUNK_SIZE = 25
