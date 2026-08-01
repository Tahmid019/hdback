
"""
Custom JWT token: it includes role + name in the access token claims.

Response shape on login:

    {
        "access": "JWT_ACCESS_TOKEN",
        "refresh": "JWT_REFRESH_TOKEN",
        "user": { "id": 12, "name": "A", "role": "doctor" }
    }
"""

from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):

    @classmethod
    def get_token(cls, user):          
        # This builds the inner dictionary   
        token = super().get_token(user)
        # including role in JWT so the auth class can read it without a db hit,
        token["role"] = user.role
        token["name"] = user.name
        return token

    def validate(self, attrs):  
        # "attrs" is the raw data user sends (dict of email and password)
        
        data = super().validate(attrs)
        
        # add user info to response body (alongside access/refresh)
        data["user"] = {
            "id": self.user.id,
            "name": self.user.name,
            "role": self.user.role,
        }
        return data   # contains 'access', 'refresh' and 'user'


class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer
