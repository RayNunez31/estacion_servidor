from django.urls import path

from . import views

app_name = "estaciones"
urlpatterns = [
    path('lecturas/', views.mediclima_list, name='mediclima_list'),
]