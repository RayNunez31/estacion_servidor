import json
from channels.generic.websocket import WebsocketConsumer

class DashboardConsumer(WebsocketConsumer):
    def connect(self):
        self.accept()

    def disconnect(self, close_code):
            self.channel_layer.group_discard(
            self.group_name,
            self.channel_name
        )

    def receive(self, text_data):
            self.channel_layer.group_send(
            self.group_name,
            {
                'type': 'update_data',
                'message': text_data
            }
        )

    def update_data(self, event):
        message = event['message']

        self.send(text_data=json.dumps({
            'message': message
        }))