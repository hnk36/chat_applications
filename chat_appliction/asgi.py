
"""
ASGI config for chat_appliction project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/howto/deployment/asgi/

The AllowedHostOriginValidator is used in Django's Channels library,
which handles WebSocket connections, to ensure that only WebSocket connections from allowed origins are accepted.
This is especially important for security, as it helps prevent
Cross-Site WebSocket Hijacking (CSWSH).

"""

import os
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
import chat_appliction.routing
from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'chat_appliction.settings')


application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": AuthMiddlewareStack(
        URLRouter(
            chat_appliction.routing.websocket_urlpatterns
        )
    ),
})