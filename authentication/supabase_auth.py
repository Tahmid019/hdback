import jwt
from django.conf import settings
from django.contrib.auth import get_user_model
from rest_framework import authentication, exceptions

User = get_user_model()

JWKS_CLIENT = jwt.PyJWKClient(
    f"{settings.SUPABASE_URL}/auth/v1/.well-known/jwks.json",
    cache_keys=True,
)


class SupabaseAuthentication(authentication.BaseAuthentication):
    def authenticate(self, request):
        auth_header = request.headers.get("Authorization")

        if not auth_header or not auth_header.startswith("Bearer "):
            return None

        token = auth_header.split(" ", 1)[1]
        print(f"🔑 [REST Auth] Extracted Token: {token[:20]}...")
        user = self.get_user_from_token(token)

        request.role = getattr(user, "role", "patient")
        print(f"✅ [REST Auth] Successfully authenticated User: {user.email} | Role: {request.role}")

        return (user, token)

    @staticmethod
    def decode_token(token):
        try:
            signing_key = JWKS_CLIENT.get_signing_key_from_jwt(token)

            return jwt.decode(
                token,
                signing_key.key,
                algorithms=["ES256", "RS256"],
                audience="authenticated",
            )

        except jwt.ExpiredSignatureError:
            raise exceptions.AuthenticationFailed("Token has expired.")

        except jwt.InvalidTokenError as e:
            raise exceptions.AuthenticationFailed(f"Invalid token: {str(e)}")

    def get_user_from_token(self, token):
        try:
            payload = self.decode_token(token)
            print(f"🔓 [REST Auth] Decoded JWT Payload: sub={payload.get('sub')}, email={payload.get('email')}")

            supabase_id = payload.get("sub")
            email = payload.get("email")

            if not supabase_id or not email:
                raise exceptions.AuthenticationFailed("Invalid user payload in token.")

            metadata = payload.get("user_metadata", {})
            app_metadata = payload.get("app_metadata", {})

            role = metadata.get("role") or app_metadata.get("role") or "patient"
            full_name = metadata.get("full_name") or email.split("@")[0]

            user, created = User.objects.get_or_create(
                supabase_id=supabase_id,
                defaults={
                    # "username": email,
                    "email": email,
                    "name": full_name,
                    "role": role,
                },
            )

            if not created and (
                user.email != email
                or user.name != full_name
                or user.role != role
            ):
                user.email = email
                user.name = full_name
                user.role = role
                user.save(update_fields=["email", "name", "role"])

        except Exception as e:
            print(f"[REST Auth] Token verification failed: {e}")
            raise e
        
        return user