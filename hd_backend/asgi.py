import os
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.security.websocket import AllowedHostsOriginValidator

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "hd_backend.settings")

# init
django_asgi = get_asgi_application()

from monitor.routing import websocket_urlpatterns

application = ProtocolTypeRouter(
    {
        "http": django_asgi,
        "websocket": AllowedHostsOriginValidator(
            URLRouter(websocket_urlpatterns)
        ),
    }
)
