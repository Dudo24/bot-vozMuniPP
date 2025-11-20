import pika, json, time, os
from utils import limpiar_texto, identidad_a_palabras
from tts_engine import generar_audio, reproducir_audio


def construir_frase(nombre, ventanilla, identidad=None, tipo_identidad=None, preferir_identidad=False):
    if (preferir_identidad and identidad) or (not nombre and identidad):
        tipo = (tipo_identidad or "identidad").lower()
        if tipo == "dni":
            etiqueta = "DNI"
        elif tipo == "pasaporte":
            etiqueta = "Pasaporte"
        elif tipo == "carnet":
            etiqueta = "Carnet de extranjería"
        else:
            etiqueta = "identidad"
        id_hablada = identidad_a_palabras(identidad)
        frase = f"Cliente con {etiqueta} {id_hablada}, por favor acercarse a la ventanilla número {ventanilla}."
    else:
        frase = f"{nombre}, por favor acercarse a la ventanilla número {ventanilla}."
    return limpiar_texto(frase)


def llamar(frase, intentos=2, pausa_seg=2):
    for intento in range(1, intentos + 1):
        print(f"[INTENTO {intento}] {frase}")
        archivo = generar_audio(frase)
        reproducir_audio(archivo)
        if intento < intentos:
            time.sleep(pausa_seg)


def llamar_persona(nombre, ventanilla, identidad=None, tipo_identidad=None, preferir_identidad=False, intentos=2):
    frase = construir_frase(nombre, ventanilla, identidad, tipo_identidad, preferir_identidad)
    llamar(frase, intentos=intentos)


def llamar_persona_una_vez(nombre, ventanilla, identidad=None, tipo_identidad=None, preferir_identidad=False):
    frase = construir_frase(nombre, ventanilla, identidad, tipo_identidad, preferir_identidad)
    llamar(frase, intentos=1)




def callback(ch, method, properties, body):
    try:
        data = json.loads(body.decode())
        nombre = data.get("nombre")
        ventanilla = data["ventanilla"]
        identidad = data.get("identidad")
        tipo_identidad = data.get("tipo_identidad")
        preferir_identidad = data.get("preferir_identidad", False)
        una_vez = data.get("una_vez", False)
        intentos = int(data.get("intentos", 2))
        if una_vez:
            intentos = 1
        if intentos < 1:
            intentos = 1
        llamar_persona(nombre, ventanilla, identidad, tipo_identidad, preferir_identidad, intentos=intentos)
    except KeyboardInterrupt:
        raise
    except Exception as e:
        print(f"Error procesando mensaje: {e}")
    finally:
        try:
            ch.basic_ack(delivery_tag=method.delivery_tag)
        except Exception:
            pass


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

    try:
        channel.start_consuming()
    except KeyboardInterrupt:
        print("Interrumpido por el usuario. Cerrando conexión...")
        try:
            channel.stop_consuming()
        except Exception:
            pass
        try:
            connection.close()
        except Exception:
            pass


if __name__ == "__main__":
    iniciar_bot()
