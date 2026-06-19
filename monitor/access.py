"""
Role based shaping of state snapshots.

"""

from . import state
from .role_config import (
    DOCTOR_INCLUDE_WAVE,
    DOCTOR_SECTIONS,
    TECHNICIAN_INCLUDE_WAVE,
    TECHNICIAN_SECTIONS,
    TECHNICIAN_WAVE_CHUNK_SIZE,
)


def build_dashboard_payload(role: str) -> dict:
    """
    
    Return the role based dashboard payload.

    The returned dict always has the shape {"role": <role>, "data": {...}}
    so the frontend can rely on it regardless of role.
    
    """
    snap = state.get_state()

    if role == "doctor":
        sections = DOCTOR_SECTIONS
        include_wave = DOCTOR_INCLUDE_WAVE
        wave_n = 0
    else:                                                 # technician (default / fallback)
        sections = TECHNICIAN_SECTIONS
        include_wave = TECHNICIAN_INCLUDE_WAVE
        wave_n = TECHNICIAN_WAVE_CHUNK_SIZE

    if sections is None:                                 # defaults to technician
        data = snap
    else:
        data = {k: snap[k] for k in sections if k in snap}

    if include_wave:
        data["wave"] = state.generate_wave_chunk(n=wave_n)

    return {"role": role, "data": data}


def is_section_allowed(role: str, section: str) -> bool:
    """
    Return whether role may read 'section' via SectionView.
    
    """

    if role == "technician":
        return True
    if role == "doctor":
        return section in DOCTOR_SECTIONS
    return False
