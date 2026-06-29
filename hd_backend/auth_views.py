"""
Auth views — currently returns the hardcoded user.
Replace with real auth lookup once JWT / session auth is wired up.
"""

from rest_framework.views import APIView
from rest_framework.response import Response
from .permissions import get_current_user


class CurrentUserView(APIView):
    """
    GET /api/auth/me/

    Returns the current user's id, name, role, and allowed_paths.
    This endpoint is PUBLIC (no required_roles) so the frontend
    can always know who is logged in.
    """

    # No required_roles → public
    def get(self, request):
        return Response(get_current_user())
