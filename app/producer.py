import pika, json


def enviar_llamado(nombre, ventanilla):
    connection = pika.BlockingConnection(
        pika.ConnectionParameters("localhost")
    )
    channel = connection.channel()

    channel.queue_declare(queue="voz")

    payload = {
        "nombre": nombre,
        "ventanilla": ventanilla
    }

    channel.basic_publish(
        exchange="",
        routing_key="voz",
        body=json.dumps(payload)
    )

    print("Mensaje enviado:", payload)
    connection.close()


if __name__ == "__main__":
    enviar_llamado("Luis Eduardo", 7)
