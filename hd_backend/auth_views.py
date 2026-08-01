"""
This is an endpoint: GET /api/auth/me/  ---> returns the authenticated user's info from the JWT.
"""

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated


class CurrentUserView(APIView):
    """
    GET /api/auth/me/

    Returns the current user's id, name, role.
    Requires a valid JWT access token.
    """

    # all roles can access it, but needs to be authenticated/logged-in 
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        return Response({
            "id": user.id,
            "name": user.name,
            "role": user.role,
        })
