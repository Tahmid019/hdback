import os
from django.core.asgi import get_asgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "hd_backend.settings")
django_asgi = get_asgi_application()

from channels.routing import ProtocolTypeRouter, URLRouter
from authentication.websocket_auth import SupabaseAuthMiddleware
from monitor.routing import websocket_urlpatterns

application = ProtocolTypeRouter(
    {
        "http": django_asgi,
        "websocket": SupabaseAuthMiddleware(
            URLRouter(
                websocket_urlpatterns
            )
        ),
    }
)