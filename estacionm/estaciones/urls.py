from django.urls import path

from . import views
from .views import login_view, register_view, logout_view, crear_estacion, dashboard_view, registro_lectura_view, lectura_detalle, administrar_view, agregar_sensor_view, alarmas_view

app_name = "estaciones"
urlpatterns = [
    path('view/', views.mediciones_list, name='mediciones_list'),
    path('logout/', logout_view, name='logout'),
    path('login/', login_view, name='login'),
    path('register/', register_view, name='register'),
    path('crear_estacion/', crear_estacion, name='crear_estacion'),
    path('dashboard/', dashboard_view, name='dashboard'),
    path('registro_lectura/', registro_lectura_view, name='registro_lectura'),
    path('lectura_detalle/', lectura_detalle, name='lectura_detalle'),
    path('administrar/', administrar_view, name='administrar'),
    path('administrar/agregar_sensor/', agregar_sensor_view, name = 'agregar_sensor'),
    path('', views.estaciones, name='estaciones'),
    path('UserAccount/', views.user_account_view, name = 'UserAccount'),
    path('eliminar_cuenta/', views.eliminar_cuenta, name='eliminar_cuenta'),
    path('alarmas/', views.alarmas_view, name = 'alarmas'),

    
]