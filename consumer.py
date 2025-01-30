import json
import csv
from kafka import KafkaConsumer

# Usamos localhost para conexiones fuera de Docker
brokers = ["kafka1:9092", "kafka2:9093", "kafka3:9094"]

consumer = KafkaConsumer(
    "simple-topic",
    "replicated-topic",
    bootstrap_servers=brokers,
    value_deserializer=lambda v: json.loads(v.decode("utf-8")),
    auto_offset_reset="earliest",
    enable_auto_commit=True,
    api_version=(2, 7, 0)
)

csv_filename = "output.csv"

write_header = True
try:
    with open(csv_filename, "r") as f:
        if f.readline():
            write_header = False
except FileNotFoundError:
    pass

with open(csv_filename, mode="a", newline="") as file:
    writer = csv.writer(file)

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