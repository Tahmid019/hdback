"""

Role view configuration.

This is the "single edit point" for changing what each role sees from the
"monitor" API. Editing the lists/flags below and restarting the Django
process is sufficient & no other code change is required.

Keys must match top-level keys produced by :func:`monitor.state.get_state`.

"""

# --- Doctor ----------------------------------------------------------------
# Sections (keys of the state snapshot) the doctor is allowed to see.
DOCTOR_SECTIONS = [
    "vitals",
    "dialysate",
    "fluid_balance",
    "session",
]

# Whether the doctor's dashboard payload includes waveform samples.
DOCTOR_INCLUDE_WAVE = False

# --- Technician ------------------------------------------------------------
# 'None' means "all sections" (no filtering).
TECHNICIAN_SECTIONS = None
TECHNICIAN_INCLUDE_WAVE = True
TECHNICIAN_WAVE_CHUNK_SIZE = 25

# --- Patient ---------------------------------------------------------------
# Sections a patient is allowed to see (from ROLE.md).
PATIENT_SECTIONS = [
    "meta",
    "respiration",
    "vitals",
    "session",
    "fluid_balance",
    "events",
]

PATIENT_INCLUDE_WAVE = False


# ----- Field level access (used by RoleAwareSerializerMixin) ------------------------------
# None = all fields allowed for that section
# List = only these fields are visible / accepted

ROLE_FIELD_ACCESS = {
    "patient": {
        "meta":        ["physician", "bed", "system_status"],  # patient_id masked
        "respiration": ["respiratory_rate"],                    # basic view only
        "vitals":      None,                                   # full access
        "session":     None,                                    # full access
        "fluid_balance": None,                                 # full access
        "events":      ["time", "type", "message"],            # patient-friendly only
    },
    "doctor": {
        # all fields for all allowed sections
    },
    "technician": {
        # all fields for all allowed sections
    },
}
