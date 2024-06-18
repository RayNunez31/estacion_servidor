"""
ASGI config for estacionm project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/howto/deployment/asgi/
"""

import os

from django.core.asgi import get_asgi_application
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from estacionm import routing  # Importa tu archivo de routing.py


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'estacionm.settings')

application = get_asgi_application()


# ESTACION/estacion/asgi.py

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'estacion.settings')

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": URLRouter(
        routing.websocket_urlpatterns
    ),
})
