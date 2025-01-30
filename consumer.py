import json
import csv
from kafka import KafkaConsumer
import os

# Definir los brokers desde el environment de Docker
brokers = os.getenv("KAFKA_BROKERS", "kafka1:9092,kafka2:9093,kafka3:9094").split(",")

try:
    consumer = KafkaConsumer(
        "simple-topic",
        "replicated-topic",
        bootstrap_servers=brokers,
        value_deserializer=lambda v: json.loads(v.decode("utf-8")),
        enable_auto_commit=True
    )
    print("🟢 Conectado correctamente a Kafka.")
except Exception as e:
    print("🔴 Error conectando a Kafka:", e)
    exit(1)

# Definir el archivo de salida CSV
csv_filename = "output.csv"

# Verificar si el archivo ya existe y tiene encabezados
write_header = True
try:
    with open(csv_filename, "r") as f:
        if f.readline():
            write_header = False
except FileNotFoundError:
    pass

# Consumir mensajes y escribir en CSV
with open(csv_filename, mode="a", newline="") as file:
    writer = csv.writer(file)

    # Escribir encabezados si es la primera vez
    if write_header:
        writer.writerow(["id", "timestamp", "ufc_event", "fighter_1", "fighter_2", "champion", "title"])

    print("📥 Escuchando mensajes de Kafka...")
    for message in consumer:
        data = message.value
        row = [
            data["id"],
            data["timestamp"],
            data["data"]["ufc_event"],
            data["data"]["fighter_1"],
            data["data"]["fighter_2"],
            data["data"]["champion"],
            data["data"]["title"],
        ]
        writer.writerow(row)
        print(f"✅ Guardado en CSV: {row}")