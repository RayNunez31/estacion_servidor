import json
from channels.generic.websocket import AsyncWebsocketConsumer

class NewlecturaConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.channel_layer.group_add("data_group", self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        pass

    async def send_new_data(self, event):
        new_data = event['data']
        await self.send(text_data=json.dumps(new_data))