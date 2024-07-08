from django.urls import path
from .consumers import NewlecturaConsumer

websocket_urlpatterns = [
    path('ws/data/', NewlecturaConsumer.as_asgi()),
]