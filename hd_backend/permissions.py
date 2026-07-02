"""
Role-based permission for DRF views.

What it does:
    1.  The JWT access token carries the user's role.
        "CustomJWTAuthentication" decodes it and sets "request.user.role".

    2.  Each view may declare:
            required_roles = ['doctor', 'technician']
        If it's missing the view is PUBLIC (anyone can access).

    3.  If "request.user.role" is NOT in the view's required_roles the
        request is rejected with 403 + a JSON body.
"""

from rest_framework.permissions import BasePermission


# -------------------------------This is the Role-Based-Permission layer (for views)---------------------------------------------

class RoleBasedPermission(BasePermission):
    """
    Deny access unless the authenticated user's role is listed in
    'view.required_roles'.  If the view does not define
    'required_roles' the endpoint is treated as public.
    """

    message = "Your role does not have permission to access this resource."

    def has_permission(self, request, view):
        required = getattr(view, "required_roles", None)

        # No restriction declared: public endpoint
        if required is None:
            return True

        # Must be authenticated
        if not request.user or not request.user.is_authenticated:
            return False

        return getattr(request.user, "role", None) in required
