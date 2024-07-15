import json
from channels.generic.websocket import AsyncWebsocketConsumer

class NewlecturaConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.group_name = "data_group"
        await self.channel_layer.group_add(self.group_name, self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.group_name, self.channel_name)

    async def receive(self, text_data):
        # Ejemplo básico de manejo de mensajes recibidos
        data = json.loads(text_data)
        # Aquí puedes agregar la lógica para manejar los datos recibidos
        # Por ejemplo, reenviar el mensaje al grupo
        await self.channel_layer.group_send(
            self.group_name,
            {
                'type': 'send_new_data',
                'data': data
            }
        )

    async def send_new_data(self, event):
        new_data = event['data']
        await self.send(text_data=json.dumps(new_data))