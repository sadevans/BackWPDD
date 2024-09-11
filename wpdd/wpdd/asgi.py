# wpdd/asgi.py

import os
from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from django.core.asgi import get_asgi_application
from .core import routing  # Import the routing module

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'wpdd.settings')

application = ProtocolTypeRouter({
    "http": get_asgi_application(),  # HTTP protocol
    "websocket": AuthMiddlewareStack(
        URLRouter(
            routing.websocket_urlpatterns  # Use the routing from routing.py
        )
    ),
})
