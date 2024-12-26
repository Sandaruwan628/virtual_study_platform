"""
ASGI config for virtual_study_platform project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/howto/deployment/asgi/
"""

import os
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from django.urls import path
from collaborative_tools.consumers import WhiteboardConsumer
from messaging.routing import websocket_urlpatterns

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'virtual_study_platform.settings')

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": AuthMiddlewareStack(
        URLRouter(
            websocket_urlpatterns + [  # Combine `websocket_urlpatterns` with additional paths
                path("ws/whiteboard/<int:board_id>/", WhiteboardConsumer.as_asgi()),
            ]
        )
    ),
})
