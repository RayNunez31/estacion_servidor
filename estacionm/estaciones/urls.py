from django.urls import path

from . import views

app_name = "estaciones"
urlpatterns = [
    path('', views.mediciones_list, name='mediciones_list'),
]