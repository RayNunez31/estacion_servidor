from celery import shared_task
from django.utils import timezone
from datetime import timedelta
from estaciones.models import Estac, Newlectura

@shared_task
def check_data_status():
    now = timezone.now()
    five_minutes_ago = now - timedelta(minutes=5)

    stations = Estac.objects.all()
    for station in stations:
        last_reading = Newlectura.objects.filter(estacion=station).order_by('-hora').first()

        if last_reading and last_reading.hora >= five_minutes_ago:
            station.receiving_data = True
        else:
            station.receiving_data = False

        station.save()