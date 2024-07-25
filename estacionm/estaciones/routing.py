
from estaciones.consumers import DashboardConsumer
from channels.routing import ProtocolTypeRouter, URLRouter
from django.urls import path
from channels.security.websocket import OriginValidator
from channels.auth import AuthMiddlewareStack


application = ProtocolTypeRouter({

    "websocket": OriginValidator(
        AuthMiddlewareStack(
            URLRouter([
                path('/dashboard/', DashboardConsumer.as_asgi()),
            ])
        ),
        ["*"],
    ),
})

