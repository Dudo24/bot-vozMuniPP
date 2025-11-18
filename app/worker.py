import pika, json, time, os
from utils import limpiar_texto
from tts_engine import generar_audio, reproducir_audio


def llamar_persona(nombre, ventanilla):
    frase = f"{nombre}, por favor acercarse a la ventanilla número {ventanilla}."
    frase = limpiar_texto(frase)

    for intento in range(1, 4):
        print(f"[INTENTO {intento}] {frase}")

        archivo = generar_audio(frase)
        reproducir_audio(archivo)

        if intento < 3:
            time.sleep(3)


def callback(ch, method, properties, body):
    data = json.loads(body.decode())
    nombre = data["nombre"]
    ventanilla = data["ventanilla"]

    llamar_persona(nombre, ventanilla)

    ch.basic_ack(delivery_tag=method.delivery_tag)


def iniciar_bot():
    host = os.getenv("RABBITMQ_HOST", "localhost")
    port = int(os.getenv("RABBITMQ_PORT", "5672"))
    user = os.getenv("RABBITMQ_USER", "guest")
    password = os.getenv("RABBITMQ_PASS", "guest")

    credentials = pika.PlainCredentials(user, password)
    params = pika.ConnectionParameters(host=host, port=port, credentials=credentials, heartbeat=60)

    try:
        connection = pika.BlockingConnection(params)
    except pika.exceptions.AMQPConnectionError:
        print(f"No se pudo conectar a RabbitMQ en {host}:{port}. Verifica que el servicio esté iniciado.")
        return

    channel = connection.channel()

    channel.queue_declare(queue="voz")

    print("Bot de voz escuchando mensajes...")

    channel.basic_consume(
        queue="voz",
        on_message_callback=callback,
        auto_ack=False
    )

    channel.start_consuming()


if __name__ == "__main__":
    iniciar_bot()
