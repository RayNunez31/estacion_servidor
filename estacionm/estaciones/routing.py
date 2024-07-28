
from estaciones.consumers import DashboardConsumer
from django.urls import path

websocket_urlpatterns = [
    path('ws/dashboard/', DashboardConsumer.as_asgi()),
]