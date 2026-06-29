"""

Role resolution.

We can replace "get_role" with whatever resolves the authenticated user's role
(e.g. request.user.role)

So until auth is ready, role is read from the "X-Role" request header so that
the rest of the system can be developed and tested independently.

"""

VALID_ROLES = ("technician", "doctor")
DEFAULT_ROLE = "technician"


def get_role(request) -> str:
    """Return the role for the incoming request.

    Returns one of "technician" or "doctor". Unknown values fall back
    to DEFAULT_ROLE.

    """
    raw = request.headers.get("X-Role", DEFAULT_ROLE)              # until auth is ready, role is read from the "X-Role"
    role = (raw or DEFAULT_ROLE).strip().lower()
    if role not in VALID_ROLES:
        return DEFAULT_ROLE
    return role
