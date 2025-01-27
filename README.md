# Guía Completa: Taller de Apache Kafka con Docker Compose

Esta guía detalla el proceso paso a paso para configurar y trabajar con Apache Kafka utilizando Docker Compose. Además, incluye ejemplos en Python para producir y consumir mensajes, y una explicación de los conceptos clave para estudiantes de nivel intermedio.

---

## **1. Introducción a Apache Kafka**

**¿Qué es Apache Kafka?**

Apache Kafka es una plataforma distribuida de streaming diseñada para manejar grandes volúmenes de datos en tiempo real. Es ampliamente utilizada para:

- Construir pipelines de datos.
- Procesar datos en tiempo real.
- Crear sistemas de mensajería distribuida.

**Conceptos clave:**
- **Broker:** Servidor que almacena y distribuye mensajes.
- **Topic:** Canal donde se publican y consumen mensajes.
- **Producer:** Publica mensajes en un topic.
- **Consumer:** Lee mensajes de un topic.
- **Partition:** División de un topic que permite escalabilidad.
- **Replica:** Copia redundante de una partición para tolerancia a fallos.

---

## **2. Configuración Inicial: Un Broker con Docker Compose**

### **Paso 1: Instalar Docker y Docker Compose**

Asegúrte de tener Docker y Docker Compose instalados en tu máquina. Puedes seguir las instrucciones oficiales en [https://docs.docker.com/get-docker/](https://docs.docker.com/get-docker/).

### **Paso 2: Crear el archivo `docker-compose.yml`**

Crea un directorio para el proyecto y dentro de él un archivo llamado `docker-compose.yml` con el siguiente contenido:

```yaml
version: '3.8'
services:
  zookeeper:
    image: 'confluentinc/cp-zookeeper:7.4.0'
    hostname: zookeeper
    environment:
      ZOOKEEPER_CLIENT_PORT: 2181
      ZOOKEEPER_TICK_TIME: 2000

  kafka:
    image: 'confluentinc/cp-kafka:7.4.0'
    hostname: kafka
    depends_on:
      - zookeeper
    ports:
      - '9092:9092'
    environment:
      KAFKA_BROKER_ID: 1
      KAFKA_ZOOKEEPER_CONNECT: zookeeper:2181
      KAFKA_ADVERTISED_LISTENERS: PLAINTEXT://kafka:9092
      KAFKA_LISTENERS: PLAINTEXT://0.0.0.0:9092
      KAFKA_OFFSETS_TOPIC_REPLICATION_FACTOR: 1
```

**Explicación:**
- **Zookeeper** gestiona la coordinación entre los brokers.
- **Kafka** es el broker principal que escucha en el puerto `9092`.

### **Paso 3: Levantar los servicios**

Ejecuta el siguiente comando para iniciar los contenedores:

```bash
docker-compose up -d
```

### **Paso 4: Validar que el broker está levantado**

1. **Verificar contenedores activos:**
   ```bash
   docker ps
   ```
   Asegúrte de que ambos servicios (Zookeeper y Kafka) estén en ejecución.

2. **Listar topics en Kafka:**
   ```bash
   docker exec -it kafka kafka-topics --list --bootstrap-server localhost:9092
   ```
   Este comando no debe generar errores.

3. **Probar conexión:**
   Publica un mensaje en un topic temporal:
   ```bash
   docker exec -it kafka kafka-console-producer --broker-list localhost:9092 --topic test-topic
   ```
   Escribe un mensaje como:
   ```
   Hello, Kafka!
   ```
   Luego, consúmelo:
   ```bash
   docker exec -it kafka kafka-console-consumer --bootstrap-server localhost:9092 --topic test-topic --from-beginning
   ```
   Si ves el mensaje publicado, la configuración es correcta.

---

## **3. Ampliación: Configuración de un Clúster con 3 Brokers**

### **Paso 1: Modificar el archivo `docker-compose.yml`**

Actualiza el archivo para incluir dos brokers adicionales:

```yaml
version: '3.8'
services:
  zookeeper:
    image: 'confluentinc/cp-zookeeper:7.4.0'
    hostname: zookeeper
    environment:
      ZOOKEEPER_CLIENT_PORT: 2181
      ZOOKEEPER_TICK_TIME: 2000

  kafka1:
    image: 'confluentinc/cp-kafka:7.4.0'
    hostname: kafka1
    depends_on:
      - zookeeper
    ports:
      - '9092:9092'
    environment:
      KAFKA_BROKER_ID: 1
      KAFKA_ZOOKEEPER_CONNECT: zookeeper:2181
      KAFKA_LISTENER_SECURITY_PROTOCOL_MAP: PLAINTEXT:PLAINTEXT
      KAFKA_ADVERTISED_LISTENERS: PLAINTEXT://kafka1:9092
      KAFKA_LISTENERS: PLAINTEXT://0.0.0.0:9092
      KAFKA_OFFSETS_TOPIC_REPLICATION_FACTOR: 3

  kafka2:
    image: 'confluentinc/cp-kafka:7.4.0'
    hostname: kafka2
    depends_on:
      - zookeeper
    ports:
      - '9093:9092'
    environment:
      KAFKA_BROKER_ID: 2
      KAFKA_ZOOKEEPER_CONNECT: zookeeper:2181
      KAFKA_LISTENER_SECURITY_PROTOCOL_MAP: PLAINTEXT:PLAINTEXT
      KAFKA_ADVERTISED_LISTENERS: PLAINTEXT://kafka2:9093
      KAFKA_LISTENERS: PLAINTEXT://0.0.0.0:9093
      KAFKA_OFFSETS_TOPIC_REPLICATION_FACTOR: 3

  kafka3:
    image: 'confluentinc/cp-kafka:7.4.0'
    hostname: kafka3
    depends_on:
      - zookeeper
    ports:
      - '9094:9092'
    environment:
      KAFKA_BROKER_ID: 3
      KAFKA_ZOOKEEPER_CONNECT: zookeeper:2181
      KAFKA_LISTENER_SECURITY_PROTOCOL_MAP: PLAINTEXT:PLAINTEXT
      KAFKA_ADVERTISED_LISTENERS: PLAINTEXT://kafka3:9094
      KAFKA_LISTENERS: PLAINTEXT://0.0.0.0:9094
      KAFKA_OFFSETS_TOPIC_REPLICATION_FACTOR: 3

  kafdrop:
    image: obsidiandynamics/kafdrop
    hostname: kafdrop
    depends_on:
      - kafka1
      - kafka2
      - kafka3
    ports:
      - "9000:9000"
    environment:
      KAFKA_BROKERCONNECT: "kafka1:9092,kafka2:9093,kafka3:9094"
      JVM_OPTS: "-Xms32M -Xmx64M"
```

### **Paso 2: Levantar el clúster**

Ejecuta:
```bash
docker-compose up -d
```
Esto creará un clúster con tres brokers: `kafka1`, `kafka2`, y `kafka3`.

### **Paso 3: Implementar Kafdrop para la visualización del clúster**

1. **Levantar Kafdrop junto con el clúster:**
   ```bash
   docker-compose up -d
   ```

2. **Acceder a Kafdrop:**
   Una vez levantado, abre un navegador y dirígete a `http://localhost:9000`.

3. **Funciones principales de Kafdrop:**
   - Explorar topics, particiones y mensajes.
   - Ver consumidores y offsets.
   - Consultar información sobre brokers y configuraciones del clúster.

---

## **4. Configuración de Topics**

1. **Crear un topic simple:**
   ```bash
   docker exec -it kafka1 kafka-topics --create \
     --topic simple-topic \
     --bootstrap-server kafka1:9092 \
     --partitions 1 \
     --replication-factor 1
   ```

2. **Crear un topic con particiones y réplicas:**
   ```bash
   docker exec -it kafka1 kafka-topics --create \
     --topic replicated-topic \
     --bootstrap-server kafka1:9092 \
     --partitions 3 \
     --replication-factor 3
   ```

3. **Listar los topics existentes:**
   ```bash
   docker exec -it kafka1 kafka-topics --list --bootstrap-server kafka1:9092
   ```

---

## **5. Anexo I: Comandos básicos de Docker**

- **Iniciar contenedores:** `docker-compose up -d`
- **Detener contenedores:** `docker-compose down`
- **Ver logs:** `docker logs kafka1`
- **Acceso a un contenedor:** `docker exec -it kafka1 bash`

---
