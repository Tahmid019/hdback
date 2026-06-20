"""
Role-based permission for DRF views.

HOW IT WORKS
────────────
1.  HARDCODED_ROLE is the "currently logged-in" role.
    → Change this one value to test different access scenarios.
    → Later this will come from real auth (JWT / session).

2.  Each view may declare:
        required_roles = ['doctor', 'technician']
    If the attribute is missing the view is PUBLIC (anyone can access).

3.  If HARDCODED_ROLE is NOT in the view's required_roles the
    request is rejected with 403 + a JSON body.
"""

from rest_framework.permissions import BasePermission

# ─── Hardcoded role — swap this single value to test access ────────────────────
HARDCODED_ROLE = "patient"

# ─── Role → user-info map (mirrors the old frontend MOCK_USERS) ───────────────
ROLE_USER_MAP = {
    "doctor": {
        "id": "USR-DOC-001",
        "name": "Dr. Aris Thorne",
        "allowed_paths": ["/doctor"],
    },
    "technician": {
        "id": "USR-TEC-001",
        "name": "Tech. Maya Singh",
        "allowed_paths": ["/technician"],
    },
    "patient": {
        "id": "USR-PAT-001",
        "name": "James O'Brien",
        "allowed_paths": ["/patient"],
    },
}


def get_current_user() -> dict:
    """Return the full user dict for the hardcoded role."""
    user = ROLE_USER_MAP.get(HARDCODED_ROLE, {})
    return {"role": HARDCODED_ROLE, **user}


class RoleBasedPermission(BasePermission):
    """
    Deny access unless the hardcoded role is listed in
    ``view.required_roles``.  If the view does not define
    ``required_roles`` the endpoint is treated as public.
    """

    message = "Your role does not have permission to access this resource."

    def has_permission(self, request, view):
        required = getattr(view, "required_roles", None)

        # No restriction declared → public endpoint
        if required is None:
            return True

        return HARDCODED_ROLE in required
