from django.urls import path

from . import views
from .views import login_view, register_view, logout_view, crear_estacion, dashboard_estacion

app_name = "estaciones"
urlpatterns = [
    #path('', views.mediciones_list, name='mediciones_list'),
    path('logout/', logout_view, name='logout'),
    path('login/', login_view, name='login'),
    path('register/', register_view, name='register'),
    path('crear_estacion/', crear_estacion, name='crear_estacion'),
    path('dashboard/', dashboard_estacion, name='dashboard'),
    path('', views.estaciones, name='estaciones'),
]