from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import timedelta
from your_app.models import Estac, Newlectura

class Command(BaseCommand):
    help = 'Check if Newlectura table is receiving data and update Estac table'

    def handle(self, *args, **kwargs):
        now = timezone.now()
        five_minutes_ago = now - timedelta(minutes=5)

        # Get the latest readings for each station
        stations = Estac.objects.all()
        for station in stations:
            last_reading = Newlectura.objects.filter(estacion=station).order_by('-hora').first()

            if last_reading and last_reading.hora >= five_minutes_ago:
                station.receiving_data = True
            else:
                station.receiving_data = False

            station.save()

        self.stdout.write(self.style.SUCCESS('Successfully updated data status.'))