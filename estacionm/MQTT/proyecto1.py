from asyncio import sleep
import random
import time
import json
from threading import Thread, Lock
from paho.mqtt import client as mqtt_client
import psycopg2
from datetime import datetime

broker = "test.mosquitto.org"
port = 1883
base_topic = "estacion"

# Variables globales para el ID de lectura
last_id_lectura = 0
id_lock = Lock()

def get_next_id():
    global last_id_lectura
    with id_lock:
        last_id_lectura += 1
        return last_id_lectura

def Datos(station_id):
    hora_actual = time.localtime()
    fecha_formateada = time.strftime("%Y-%m-%d", hora_actual)
    hora_formateada = time.strftime("%H:%M:%S", hora_actual)
    fecha_hora = datetime.strptime(f"{fecha_formateada} {hora_formateada}", "%Y-%m-%d %H:%M:%S")

    return {
        "id_lectura": get_next_id(),  # Obtener el siguiente ID de lectura
        "id_estacion": station_id,
        "temperatura": round(random.uniform(18, 35), 2),
        "humedad": round(random.uniform(0, 100), 2),
        "presionAtmosferica": round(random.uniform(950, 1050), 2),
        "velocidadViento": round(random.uniform(0, 100), 2),
        "direccionViento": round(random.uniform(0, 255), 2),
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
    while True:
        datos = Datos(station_id)
        payload = json.dumps(datos, default=str)  # Usar default=str para serializar datetime
        topic = f"{base_topic}/{station_id}/sensores"
        result = client.publish(topic, payload)
        status = result[0]
        if status == 0:
            print(f"Enviado `{payload}` a `{topic}`")
        else:
            print(f"Mensaje fallido {topic}")
        time.sleep(5)

def subscribe(client, station_ids):
    def on_message(client, userdata, msg):
        print(f"Recibido `{msg.payload.decode()}` de `{msg.topic}`")
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
            INSERT INTO newlectura (id_lectura, id_estacion, temperatura, humedad, presionAtmosferica, velocidad_del_viento, direccion_del_viento, pluvialidad, hora)
            VALUES (%(id_lectura)s, %(id_estacion)s, %(temperatura)s, %(humedad)s, %(presionAtmosferica)s, %(velocidadViento)s, %(direccionViento)s, %(pluvialidad)s, %(hora)s)
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
        sleep(5)
    for t in threads:
        t.join()

def run_subscriber():
    client_id = f'subscribe-{random.randint(0, 1000)}'
    client = connect_mqtt(client_id)
    station_ids = ["estacion1", "estacion2"]  # Puedes agregar más estaciones aquí si es necesario
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
        crear_tabla_query = """
            CREATE TABLE IF NOT EXISTS newLectura (
                id SERIAL PRIMARY KEY,
                id_lectura INT,
                id_estacion VARCHAR(50),
                temperatura FLOAT,
                humedad FLOAT,
                presionAtmosferica FLOAT,
                velocidad_del_viento FLOAT,
                direccion_del_viento FLOAT,
                pluvialidad FLOAT,
                hora TIMESTAMP
            )
            """
        cursor.execute(crear_tabla_query)
        connection.commit()
        cursor.close()
        connection.close()
        print("Tabla creada correctamente o ya existía.")
    except Exception as e:
        print(f"Error al crear la tabla: {e}")

    Thread(target=run_publisher, args=([f"estacion{i}" for i in range(1, 3)],)).start()
    Thread(target=run_subscriber).start()