import json
import time
from kafka import KafkaProducer
import os

# Definir los brokers desde el environment de Docker
brokers = os.getenv("KAFKA_BROKERS", "kafka1:9092,kafka2:9093,kafka3:9094").split(",")

try:
    producer = KafkaProducer(
        bootstrap_servers=brokers,
        value_serializer=lambda v: json.dumps(v).encode("utf-8")
    )
    print("🟢 Conectado correctamente a Kafka.")
except Exception as e:
    print("🔴 Error conectando a Kafka:", e)
    exit(1)

json_file = "/app/ufc_championships_extended.json"

def validate_json(record):
    required_keys = {"id", "timestamp", "data"}
    required_data_keys = {"ufc_event", "fighter_1", "fighter_2", "champion", "title"}

    if not required_keys.issubset(record.keys()):
        return False
    if not isinstance(record["id"], int) or not isinstance(record["timestamp"], str):
        return False
    if not isinstance(record["data"], dict) or not required_data_keys.issubset(record["data"].keys()):
        return False

    return True

with open(json_file, "r", encoding="utf-8") as file:
    data = json.load(file)

    for record in data:
        if validate_json(record):
            producer.send("simple-topic", value=record)
            producer.send("replicated-topic", value=record)
            print(f"📤 Enviado a ambos topics: {record}")
            time.sleep(1)
        else:
            print(f"⚠️ Error: JSON inválido {record}")

producer.flush()
producer.close()