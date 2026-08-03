from urllib.parse import parse_qs
from channels.db import database_sync_to_async
from django.contrib.auth.models import AnonymousUser
from authentication.supabase_auth import SupabaseAuthentication


class SupabaseAuthMiddleware:
    def __init__(self, inner):
        self.inner = inner
        self.auth = SupabaseAuthentication()

    async def __call__(self, scope, receive, send):
        query_string = scope.get("query_string", b"").decode()
        params = parse_qs(query_string)
        token = params.get("token", [None])[0]

        if not token:
            print("⚠️ [WS Auth] Connection attempt without token.")
            scope["user"] = AnonymousUser()
            scope["role"] = None
            return await self.inner(scope, receive, send)

        print(f"🔑 [WS Auth] WS Connection Token: {token[:20]}...")
        user = await self.get_user(token)

        if user:
            scope["user"] = user
            scope["role"] = getattr(user, "role", "patient")
            print(f"✅ [WS Auth] WS Connected: User={user.email} | Role={scope['role']}")
        else:
            print("❌ [WS Auth] WS Connection Failed: Invalid or Expired Token.")
            scope["user"] = AnonymousUser()
            scope["role"] = None

        return await self.inner(scope, receive, send)

    @database_sync_to_async
    def get_user(self, token):
        try:
            return self.auth.get_user_from_token(token)
        except Exception:
            return None