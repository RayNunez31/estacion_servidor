"""
ASGI config for estacionm project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/howto/deployment/asgi/
"""
import os
from channels.auth import AuthMiddlewareStack
from django.core.asgi import get_asgi_application
from channels.security.websocket import AllowedHostsOriginValidator
from channels.routing import ProtocolTypeRouter, URLRouter

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'estacionm.settings')

application = get_asgi_application()

import estaciones.routing

application = ProtocolTypeRouter({
    'http': application,
    "websocket": AllowedHostsOriginValidator(
        AuthMiddlewareStack(URLRouter(estaciones.routing.websocket_urlpatterns))
    ),
})