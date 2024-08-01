import random
import time
import json
from threading import Thread
from paho.mqtt import client as mqtt_client
from datetime import datetime


broker = "test.mosquitto.org"
port = 1883
base_topic = "estacion"

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
    while True:
        datos = Datos(station_id)
        payload = json.dumps(datos, default=str)
        topic = f"{base_topic}/{station_id}/sensores"
        result = client.publish(topic, payload)
        status = result[0]
        if status == 0:
            print(f"Enviado {payload} a {topic}")
        else:
            print(f"Mensaje fallido {topic}")
        time.sleep(5)

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

if __name__ == '__main__':
    station_ids = [15, 10]  # IDs de ejemplo de las estaciones
    run_publisher(station_ids)