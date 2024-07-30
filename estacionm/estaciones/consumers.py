import json
from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync
import threading
from .models import Estac, Newlectura
import time
from datetime import datetime, timedelta
from django.core.exceptions import ObjectDoesNotExist


class DashboardConsumer(WebsocketConsumer):
    def connect(self):
        self.GROUP_NAME = 'estacion-dashboard'
        async_to_sync(self.channel_layer.group_add)(
            self.GROUP_NAME, self.channel_name
        )
        self.accept()

    def disconnect(self, close_code):
        async_to_sync(self.channel_layer.group_discard)(
            self.GROUP_NAME, self.channel_name
        )
    
    def receive(self, text_data):
        # Recibir datos del WebSocket
        data = json.loads(text_data)
        print('Mensaje Recibido')
        # Envía los datos a todos los clientes conectados al grupo
        async_to_sync(self.channel_layer.group_send)(
            self.GROUP_NAME,
            {
                'type': 'send_dashboard_data',  # Añade el tipo de mensaje
                'estacion_id': data.get('estacion_id'),  # Incluye el ID de la estación en los datos enviados
                'temperatura': data.get('temperatura'),
                'humedad': data.get('humedad'),
                'presionatmosferica': data.get('presionatmosferica'),
                'velocidad_del_viento': data.get('velocidad_del_viento'),
                'direccion_del_viento': data.get('direccion_del_viento'),
                'pluvialidad': data.get('pluvialidad'),
                'hora': data.get('hora')
            }
        )

    def send_dashboard_data(self, event):
        # Envía los datos de vuelta al WebSocket
        self.send(text_data=json.dumps({
            'estacion_id': event['estacion_id'],
            'temperatura': event['temperatura'],
            'humedad': event['humedad'],
            'presionatmosferica': event['presionatmosferica'],
            'velocidad_del_viento': event['velocidad_del_viento'],
            'direccion_del_viento': event['direccion_del_viento'],
            'pluvialidad': event['pluvialidad'],
            'hora': event['hora']
        }))

class AllUsersConsumer(WebsocketConsumer):
    def connect(self):
        self.GROUP_NAME = 'realtime-updates'
        async_to_sync(self.channel_layer.group_add)(
            self.GROUP_NAME, self.channel_name
        )
        self.accept()

        # Start the periodic task
        self.keep_running = True
        self.check_thread = threading.Thread(target=self.check_for_inactive_stations)
        self.check_thread.start()

    def disconnect(self, close_code):
        async_to_sync(self.channel_layer.group_discard)(
            self.GROUP_NAME, self.channel_name
        )
        self.keep_running = False
        self.check_thread.join()

    def check_for_inactive_stations(self):
        while self.keep_running:
            now = datetime.now()
            one_minute_ago = now - timedelta(minutes=1)
            print('Checking communication status...')
            for station in Estac.objects.all():
                try:
                    ultima_actualizacion = station.ultima_actualizacion
                    tiempo_transcurrido = datetime.now() - ultima_actualizacion
                    if tiempo_transcurrido > timedelta(minutes=2):
                        self.send_station_inactive_notification(station)
                except ObjectDoesNotExist:
                    # Manejar caso donde no existe última actualización
                    pass

            time.sleep(120)  # Check every minute

    def send_station_inactive_notification(self, station):
        async_to_sync(self.channel_layer.group_send)(
            self.GROUP_NAME,
            {
                'type': 'station.inactive',
                'message': f'La estacion {station.nombre} actualmente se encuentra desconectada',
                
            }
        )

    def station_inactive(self, event):
        message = event['message']
        self.send(text_data=message)