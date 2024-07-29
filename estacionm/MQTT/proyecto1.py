import random
import time
import json
from threading import Thread
from paho.mqtt import client as mqtt_client
import psycopg2
from datetime import datetime
import websocket

broker = "test.mosquitto.org"
port = 1883
base_topic = "estacion"
websocket_url = 'ws://localhost:8000/ws/dashboard/'  # Cambia esto a la URL de tu servidor WebSocket

def Datos(station_id):
    hora_actual = time.localtime()
    fecha_formateada = time.strftime("%Y-%m-%d", hora_actual)
    hora_formateada = time.strftime("%H:%M:%S", hora_actual)
    fecha_hora = datetime.strptime(f"{fecha_formateada} {hora_formateada}", "%Y-%m-%d %H:%M:%S")

    return {
        "estacion_id": station_id,
        "temperatura": round(random.uniform(18, 35), 2),
        "humedad": round(random.uniform(0, 100), 2),
        "presionatmosferica": round(random.uniform(950, 1050), 2),
        "velocidad_del_viento": round(random.uniform(0, 100), 2),
        "direccion_del_viento": round(random.uniform(0, 255), 2),
        "pluvialidad": round(random.uniform(0, 100), 2),
        "hora": fecha_hora
    }

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

def publish(client, station_id):
    ws = websocket.WebSocket()
    ws.connect(websocket_url)
    while True:
        datos = Datos(station_id)
        payload = json.dumps(datos, default=str)
        topic = f"{base_topic}/{station_id}/sensores"
        result = client.publish(topic, payload)
        status = result[0]
        if status == 0:
            print(f"Enviado {payload} a {topic}")
            # Enviar datos al servidor WebSocket
            ws.send(payload)
            print(f"Datos enviados al WebSocket: {payload}")
        else:
            print(f"Mensaje fallido {topic}")
        time.sleep(5)
    ws.close()

def subscribe(client, station_ids):
    def on_message(client, userdata, msg):
        print(f"Recibido {msg.payload.decode()} de {msg.topic}")
        datos = json.loads(msg.payload.decode())
        
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
            VALUES (%(estacion_id)s, %(temperatura)s, %(humedad)s, %(presionatmosferica)s, %(velocidad_del_viento)s, %(direccion_del_viento)s, %(pluvialidad)s, %(hora)s)
            """
            cursor.execute(insert_query, datos)
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

def run_publisher(station_ids):
    threads = []
    for station_id in station_ids:
        client_id = f'publish-{station_id}-{random.randint(0, 1000)}'
        client = connect_mqtt(client_id)
        t = Thread(target=publish, args=(client, station_id))
        t.start()
        threads.append(t)
        time.sleep(5)
    for t in threads:
        t.join()

def run_subscriber(station_ids):
    client_id = f'subscribe-{random.randint(0, 1000)}'
    client = connect_mqtt(client_id)
    subscribe(client, station_ids)
    client.loop_forever()

if __name__ == '__main__':
    try:
        connection = psycopg2.connect(
            host='192.168.100.155',
            user='postgres',
            password='postgres',
            database='AntenaMeteorologica'
        )
        cursor = connection.cursor()
        
        # Crear tablas
        crear_tabla_estac_query = """
            CREATE TABLE IF NOT EXISTS estac (
                id_estacion SERIAL PRIMARY KEY,
                nombre VARCHAR(100),
                descripcion VARCHAR(200)
            )
        """
        cursor.execute(crear_tabla_estac_query)

        crear_tabla_sensor_query = """
            CREATE TABLE IF NOT EXISTS sensor (
                id_sensor SERIAL PRIMARY KEY,
                nombre VARCHAR(100),
                modelo VARCHAR(100),
                descripcion TEXT,
                estacion_id INT REFERENCES estac(id_estacion)
            )
        """
        cursor.execute(crear_tabla_sensor_query)

        crear_tabla_newlectura_query = """
            CREATE TABLE IF NOT EXISTS newlectura (
                id_lectura SERIAL PRIMARY KEY,
                estacion_id INT REFERENCES estac(id_estacion),
                temperatura FLOAT,
                humedad FLOAT,
                presionatmosferica FLOAT,
                velocidad_del_viento FLOAT,
                direccion_del_viento FLOAT,
                pluvialidad FLOAT,
                hora TIMESTAMP
            )
        """
        cursor.execute(crear_tabla_newlectura_query)

        # Insertar estaciones de ejemplo
        estaciones = [
            ('Estación 1', 'Descripción de la Estación 1'),
            ('Estación 2', 'Descripción de la Estación 2')
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
        cursor.execute("SELECT id_estacion FROM estac WHERE nombre IN ('Estación 1', 'Estación 2')")
        estaciones = cursor.fetchall()
        station_ids = [estacion[0] for estacion in estaciones]

        connection.commit()
        cursor.close()
        connection.close()
        print("Tablas creadas y estaciones insertadas correctamente.")
    except Exception as e:
        print(f"Error al crear las tablas o insertar estaciones: {e}")

    Thread(target=run_publisher, args=(station_ids,)).start()
    Thread(target=run_subscriber, args=(station_ids,)).start()
