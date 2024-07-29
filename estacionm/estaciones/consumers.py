import json
from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync

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

