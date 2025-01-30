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

### \*\*Paso 2: Crear el archivo \*\***`docker-compose.yml`**

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

### \*\*Paso 1: Modificar el archivo \*\***`docker-compose.yml`**

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

## **5. Ahora es tu turno**

Te toca crear dos scripts en Python para interactuar con el clúster de Kafka que acabas de configurar:

1. **Producer:** Crea un script que envíe un mensaje en formato JSON a un topic del clúster.

   - El mensaje debe incluir al menos tres campos clave, como `id`, `timestamp` y `data`. (en el repo hay un archivo json, si lo quieres utiliza. 
   - Debes de crear un archivo local con multiples lineas en json. 
   - El script debe de leer el archivo local y enviar cada linea json al topic.

2. **Consumer:** Crea un script que consuma los mensajes de ese topic, convierta el formato JSON a CSV y guarde los resultados en un archivo local.

**Consejos:**

- Utiliza la librería `kafka-python` para conectarte al clúster.
- Asegúrate de manejar errores como desconexiones del clúster o datos mal formateados.
- Diseña el script del Consumer para que sea eficiente y maneje múltiples mensajes a la vez.

---

## **6. Anexo I: Comandos básicos de Docker**

- **Iniciar contenedores:** `docker-compose up -d`
- **Detener contenedores:** `docker-compose down`
- **Ver logs:** `docker logs kafka1`
- **Acceso a un contenedor:** `docker exec -it kafka1 bash`

---

## **7. Ejecución Manual de Producer y Consumer en Paralelo**

Para monitorear cómo los datos fluyen en tiempo real desde el **Producer** hasta el **Consumer**, sigue estos pasos:

---

### **Paso 1: Ingresar al Contenedor de Python**
Abre la **primera terminal** y ejecuta:

```bash
docker exec -it python-app bash
```

Esto te llevará dentro del contenedor `python-app`, donde correremos los scripts.

---

### **Paso 2: Ejecutar el Producer en la Primera Terminal**
En la misma terminal, ejecuta el **Producer** para enviar datos a Kafka:

```bash
python producer.py
```

📤 **Salida esperada:**  
Cada mensaje enviado se imprimirá en la terminal, indicando que se ha producido correctamente en los topics de Kafka.

---

### **Paso 3: Abrir una Segunda Terminal para el Consumer**
Abre una **segunda terminal** y ejecuta el mismo comando para ingresar al contenedor:

```bash
docker exec -it python-app bash
```

Ahora, dentro del contenedor, ejecuta el **Consumer**:

```bash
python consumer.py
```

📥 **Salida esperada:**  
Cada mensaje recibido desde Kafka se imprimirá en la terminal y se guardará en el archivo **output.csv** dentro del contenedor.

---

### **Paso 4: Verificar los Mensajes Consumidos**
Para revisar los datos almacenados en el archivo CSV dentro del contenedor, usa:

```bash
cat output.csv
```

Si quieres copiar el archivo a tu máquina local:

```bash
docker cp python-app:/app/output.csv ./output.csv
```

---

### **Paso 5: Reiniciar la Ejecución Fácilmente**
Si deseas ejecutar el **Producer y Consumer nuevamente**, usa los siguientes comandos:

#### **Reiniciar Producer**
```bash
docker exec -it python-app bash -c "python producer.py"
```

#### **Reiniciar Consumer**
```bash
docker exec -it python-app bash -c "python consumer.py"
```

---

### **Paso 6: Detener y Reiniciar Todo el Clúster**
Si en algún momento necesitas **detener todos los contenedores** y reiniciar el clúster de Kafka:

```bash
docker-compose down
docker-compose up -d
```

Con estos pasos podrás monitorear en **tiempo real** cómo los mensajes son producidos y consumidos en Apache Kafka. 🚀
