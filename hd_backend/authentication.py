"""

Attaches the "role" claim from the JWT
directly onto the user object so that "request.user.role" is always
available without an extra DB query.
"""

from rest_framework_simplejwt.authentication import JWTAuthentication
from django.contrib.auth import get_user_model


# ----------------------------THIS IS THE AUTHENTICATION LAYER------------------------------------------

class CustomJWTAuthentication(JWTAuthentication):


    def get_user(self, validated_token):
        """
        Creates a stateless User object purely from the JWT payload
        to prevent a database query on every single API request.
        """
        User = get_user_model()
        
        # create a dummy user in memory (this does not hit the database)
        user = User()
        
        # populate the fields directly from the decrypted/validated token dictionary
        user.id = validated_token.get("user_id")
        user.pk = user.id
        user.role = validated_token.get("role", "patient") # Fallback to patient for safety
        user.name = validated_token.get("name", "")

        return user
