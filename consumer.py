import json
import csv
import os
from kafka import KafkaConsumer

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

# Definir el archivo de salida CSV en la carpeta /app dentro del contenedor
csv_filename = "/app/output.csv"

# Crear el archivo si no existe y asegurarse de que tenga permisos adecuados
if not os.path.exists(csv_filename):
    with open(csv_filename, mode="w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(["id", "timestamp", "ufc_event", "fighter_1", "fighter_2", "champion", "title"])
    os.chmod(csv_filename, 0o666)  # Permisos de escritura para todos los usuarios
    print("📄 Archivo CSV creado correctamente: output.csv")

# Consumir mensajes y escribir en CSV
with open(csv_filename, mode="a", newline="", encoding="utf-8") as file:
    writer = csv.writer(file)

    print("📥 Escuchando mensajes de Kafka...")

    try:
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
            file.flush()  # Asegurar que se escriba en disco inmediatamente
            print(f"✅ Guardado en CSV: {row}")
    except KeyboardInterrupt:
        print("\n🛑 Deteniendo el consumidor.")