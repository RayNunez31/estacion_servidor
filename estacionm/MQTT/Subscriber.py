import json
import time
import psycopg2
from threading import Thread
from paho.mqtt import client as mqtt_client
import websocket
import random
from datetime import datetime

broker = "test.mosquitto.org"
port = 1883
base_topic = "estacion"
websocket_url = 'wss://itt363-5.smar.com.do/ws/dashboard/'  # Cambia esto a la URL de tu servidor WebSocket

def connect_mqtt(client_id):
    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print(f"Conectado al broker {client_id}!")
        else:
            print(f"Conexion fallida {rc}\n")

    client = mqtt_client.Client(client_id=client_id, callback_api_version=mqtt_client.CallbackAPIVersion.VERSION1)
    client.on_connect = on_connect
    client.connect(broker, port)
    return client

def subscribe(client, station_ids):
    def on_message(client, userdata, msg):
        print(f"Recibido {msg.payload.decode()} de {msg.topic}")
        datos = json.loads(msg.payload.decode())
        # Enviar datos al servidor WebSocket
        mapped_data = {
            "estacion_id": datos.get("estacion_id"),
            "temperatura": datos.get("temperatura"),
            "humedad": datos.get("humedad"),
            "presionatmosferica": datos.get("presion"),
            "velocidad_del_viento": datos.get("velocidad_viento"),
            "direccion_del_viento": datos.get("direccion_viento"),
            "pluvialidad": datos.get("pluvialidad"),
            "hora": datos.get("fecha")  # Asegúrate de que la fecha esté en el formato adecuado
        }

        ws = websocket.WebSocket()
        try:
            ws.connect(websocket_url)
            ws.send(json.dumps(mapped_data, default=str))
            print(f"Datos enviados al WebSocket: {json.dumps(mapped_data, default=str)}")
        except Exception as e:
            print(f"Error al conectar o enviar datos al WebSocket: {e}")
        finally:
            ws.close()
        try:
            connection = psycopg2.connect(
                host='192.168.100.155',
                user='postgres',
                password='postgres',
                database='AntenaMeteorologica'
            )
            cursor = connection.cursor()
            insert_query = """
            INSERT INTO newlectura (estacion_id, temperatura, humedad, presionatmosferica, velocidad_del_viento, direccion_del_viento, pluvialidad, hora)
            VALUES (%(estacion_id)s, %(temperatura)s, %(humedad)s, %(presionatmosferica)s, %(velocidad_del_viento)s , %(direccion_del_viento)s, %(pluvialidad)s, %(hora)s)
            """
            cursor.execute(insert_query, mapped_data)
            connection.commit()
            cursor.close()
            connection.close()
            print("Datos insertados correctamente en la base de datos.")
        except Exception as e:
            print(f"Error al insertar en la base de datos: {e}")

    for station_id in station_ids:
        topic = f"{base_topic}/{station_id}/sensores"
        client.subscribe(topic)
        client.message_callback_add(topic, on_message)

def run_subscriber(station_ids):
    client_id = f'subscribe-{random.randint(0, 1000)}'
    client = connect_mqtt(client_id)
    subscribe(client, station_ids)
    client.loop_forever()

if __name__ == '_main_':
    try:
        connection = psycopg2.connect(
            host='192.168.100.155',
            user='postgres',
            password='postgres',
            database='AntenaMeteorologica'
        )
        cursor = connection.cursor()

        # Insertar estaciones de ejemplo
        estaciones = [
            ('Estación 1', 'Descripción de la Estación 1')
        ]

        for nombre, descripcion in estaciones:
            # Check if the station already exists
            cursor.execute("SELECT id_estacion FROM estac WHERE nombre = %s", (nombre,))
            station_exists = cursor.fetchone()
            
            if station_exists:
                print(f"Estación '{nombre}' ya existe con ID {station_exists[0]}.")
            else:
                try:
                    cursor.execute("""
                        INSERT INTO estac (nombre, descripcion) 
                        VALUES (%s, %s)
                    """, (nombre, descripcion))
                    print(f"Estación '{nombre}' insertada correctamente.")
                except Exception as e:
                    print(f"Error al insertar estación '{nombre}': {e}")

        # Obtener IDs de estaciones
        cursor.execute("SELECT id_estacion FROM estac WHERE nombre IN ('Estación 1')")
        estaciones = cursor.fetchall()
        station_ids = [estacion[0] for estacion in estaciones]

        connection.commit()
        cursor.close()
        connection.close()
        print("Tablas creadas y estaciones insertadas correctamente.")
    except Exception as e:
        print(f"Error al crear las tablas o insertar estaciones: {e}")

    Thread(target=run_subscriber, args=(station_ids,)).start()