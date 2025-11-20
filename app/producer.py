import pika, json, argparse, os


def enviar_llamado(nombre=None, ventanilla=None, identidad=None, tipo_identidad=None, preferir_identidad=False, una_vez=False, intentos=None):
    host = os.getenv("RABBITMQ_HOST", "localhost")
    port = int(os.getenv("RABBITMQ_PORT", "5672"))
    user = os.getenv("RABBITMQ_USER", "guest")
    password = os.getenv("RABBITMQ_PASS", "guest")

    params = pika.ConnectionParameters(host=host, port=port, credentials=pika.PlainCredentials(user, password))
    connection = pika.BlockingConnection(params)
    channel = connection.channel()

    channel.queue_declare(queue="voz")

    payload = {
        "nombre": nombre,
        "ventanilla": ventanilla,
        "identidad": identidad,
        "tipo_identidad": tipo_identidad,
        "preferir_identidad": preferir_identidad,
        "una_vez": una_vez,
    }
    if intentos is not None:
        payload["intentos"] = intentos

    channel.basic_publish(
        exchange="",
        routing_key="voz",
        body=json.dumps(payload)
    )

    print("Mensaje enviado:", payload)
    connection.close()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Envia llamados de voz a la cola 'voz'")
    parser.add_argument("--ventanilla", type=int, required=True, help="Número de ventanilla")
    parser.add_argument("--nombre", type=str, help="Nombre completo del cliente")
    parser.add_argument("--identidad", type=str, help="Número de identidad (DNI, pasaporte, carnet)")
    parser.add_argument("--tipo-identidad", type=str, choices=["dni", "pasaporte", "carnet"], help="Tipo de identidad")
    parser.add_argument("--preferir-identidad", action="store_true", help="Usar identidad en lugar del nombre si ambos existen")
    parser.add_argument("--una-vez", action="store_true", help="Realizar un solo llamado")
    parser.add_argument("--intentos", type=int, help="Cantidad de intentos de llamado")

    args = parser.parse_args()

    enviar_llamado(
        nombre=args.nombre,
        ventanilla=args.ventanilla,
        identidad=args.identidad,
        tipo_identidad=args.tipo_identidad,
        preferir_identidad=args.preferir_identidad,
        una_vez=args.una_vez,
        intentos=args.intentos,
    )
