

import json
from channels.generic.websocket import AsyncWebsocketConsumer
from estaciones.models import Medicionescombinadas as Lectura  # Importa tu modelo de Lectura desde estaciones.models
import logging

logger = logging.getLogger(__name__)

class MyConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        logger.info("WebSocket connection established")
        await self.accept()

    async def disconnect(self, close_code):
        logger.info("WebSocket connection closed")

    async def receive(self, text_data):
        logger.info(f"Received message: {text_data}")
        # Procesa el mensaje recibido y envía respuestas si es necesario

class LecturaConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()

    async def disconnect(self, close_code):
        pass

    async def receive(self, text_data):
        data = json.loads(text_data)
        valor = data['valor']  # Suponiendo que recibes un JSON con 'valor'

        # Guardar el valor en la base de datos
        lectura = Lectura(valor=valor)
        await lectura.save()

        # Puedes enviar el nuevo valor a todos los clientes conectados
        await self.send(text_data=json.dumps({
            'valor': valor
        }))