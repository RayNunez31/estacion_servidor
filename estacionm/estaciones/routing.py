
from estaciones.consumers import DashboardConsumer, AllUsersConsumer
from django.urls import path

websocket_urlpatterns = [
    path('ws/dashboard/', DashboardConsumer.as_asgi()),
    path('ws/all_users/', AllUsersConsumer.as_asgi()),

]