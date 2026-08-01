"""

Role resolution.

Reads the role from ``request.user.role`` (set by JWT authentication).
Falls back to DEFAULT_ROLE for unauthenticated or role-less requests.

"""

VALID_ROLES = ("technician", "doctor", "patient")
DEFAULT_ROLE = "patient"


def get_role(request) -> str:
    """
    Return the role for the incoming request.

    Returns one of "technician", "doctor", or "patient".
    Unknown / missing values fall back to DEFAULT_ROLE.

    """
    role = getattr(request.user, "role", None)
    if role and role in VALID_ROLES:
        return role
    return DEFAULT_ROLE
