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
        data = json.loads(text_data)
        self.send(text_data=json.dumps({
            'temperatura': data['temperatura'],
            'humedad': data['humedad'],
            'presionatmosferica': data['presionatmosferica'],
            'velocidad_del_viento': data['velocidad_del_viento'],
            'direccion_del_viento': data['direccion_del_viento'],
            'pluvialidad': data['pluvialidad'],
        }))