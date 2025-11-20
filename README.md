🗣️ Bot de Voz con Python + Coqui TTS + RabbitMQ (Windows)

Este documento explica la instalación completa: Python, Erlang/OTP, RabbitMQ, dependencias del bot, ejecución y verificación.

✅ Requisitos previos
- Windows 10/11 de 64 bits
- Python 3.10.x instalado y en PATH
- Permisos de PowerShell para scripts: `Set-ExecutionPolicy -Scope CurrentUser -ExecutionPolicy RemoteSigned`

Verifica Python:
```
python --version
```

🔧 Instalar Erlang/OTP (requerido por RabbitMQ)
- Descarga e instala Erlang/OTP para Windows (64 bits) desde el sitio oficial.
    https://www.erlang.org/downloads
- Asegúrate de instalar una versión compatible con tu RabbitMQ.
- Durante la instalación, permite que se agregue Erlang al PATH.

Validar instalación de Erlang:
```
erl -version
```

📦 Instalar RabbitMQ (Windows)
https://www.rabbitmq.com/docs/install-windows
1) Instala RabbitMQ para Windows (instalador MSI).
2) Abre PowerShell como administrador y ve al directorio `sbin` de RabbitMQ, por ejemplo:
```
cd "C:\Program Files\RabbitMQ Server\rabbitmq_server-<VERSION>\sbin"
```
3) Instala RabbitMQ como servicio de Windows y arráncalo:
```
./rabbitmq-service.bat install
./rabbitmq-service.bat start
```
4) Habilita la consola web de administración:
```
./rabbitmq-plugins.bat enable rabbitmq_management
```
5) Crea un usuario propio seguro y restringe el usuario por defecto:
```
./rabbitmqctl.bat add_user muni_bot <TU_PASSWORD_FUERTE>
./rabbitmqctl.bat set_permissions -p / muni_bot ".*" ".*" ".*"
./rabbitmqctl.bat set_user_tags muni_bot administrator
```
Opcionalmente deshabilita acceso remoto del usuario `guest` (solo sirve en localhost):
```
./rabbitmqctl.bat clear_password guest
```

Verifica servicio y plugin de gestión:
- Estado del servidor: `./rabbitmqctl.bat status`
- Consola web: `http://localhost:15672` (usuario y password que creaste)


IMPORTANTE 
🐍 Preparar entorno de Python (venv)
1) Crear y activar entorno virtual:
```
python -m venv venv
./venv/Scripts/Activate.ps1
```
2) Instalar dependencias del bot:
```
pip install TTS pygame num2words pika scipy
```
Nota: `TTS` descargará modelos y dependencias. `scipy` se usa para escribir WAV.

🔧 Configurar variables de entorno para el bot
En PowerShell (mientras el worker está corriendo, hereda estas variables):
```
$env:RABBITMQ_HOST = "localhost"
$env:RABBITMQ_PORT = "5672"
$env:RABBITMQ_USER = "muni_bot"
$env:RABBITMQ_PASS = "<TU_PASSWORD_FUERTE>"
```
Si necesitas que sean persistentes, configúralas en Variables de Entorno del Sistema.

📁 Estructura del proyecto
```
bot-vozMuniPP/
├── venv/
└── app/
    ├── producer.py      (publica mensajes en la cola 'voz')
    ├── worker.py        (consume 'voz' y reproduce audio)
    ├── tts_engine.py    (motor TTS y reproducción)
    └── utils.py         (normalización y lectura de identidad)
```

▶️ Ejecutar el bot de voz
1) Inicia RabbitMQ (servicio ya instalado):
```
cd "C:\Program Files\RabbitMQ Server\rabbitmq_server-<VERSION>\sbin"
./rabbitmq-service.bat start
```
2) Activa el entorno Python y arranca el worker:
```
cd C:\Users\TU_USUARIO\Desktop\bot-vozMuniPP
./venv/Scripts/Activate.ps1
python app/worker.py
```
Verás: "Bot de voz escuchando mensajes..."

3) En otra consola, envía un llamado con el producer (CLI):
Por nombre:
```
python app/producer.py --ventanilla 7 --nombre "Jose Rodrigo Orozco Gomez"
```
Por identidad (DNI/pasaporte/carnet):
```
python app/producer.py --ventanilla 3 --identidad 12345678 --tipo-identidad dni --preferir-identidad
```

Opciones de repetición (nuevas):
- Un solo llamado:
```
python app/producer.py --ventanilla 7 --nombre "Eduardo Saldaña" --una-vez
```
- Llamado con intentos personalizados (por defecto 2):
```
python app/producer.py --ventanilla 7 --nombre "Eduardo Saldaña" --intentos 2
```
Notas:
- Si se envía `--una-vez`, el worker fuerza 1 intento.
- Si se envía `--intentos N`, el worker usa N intentos (mínimo 1).

🔎 Verificación en RabbitMQ
- Abre `http://localhost:15672` y verifica la cola `voz`.
- El worker confirma mensajes y evita reentregas incluso si se interrumpe.

🛟 Operación como servicio del worker (opcional)
- Puedes usar el Programador de Tareas de Windows para iniciar `python app/worker.py` al arranque.
- Alternativas como NSSM pueden correr el script Python como servicio.

⚠️ Problemas comunes y soluciones
- No conecta a RabbitMQ: verifica servicio (`rabbitmqctl status`), firewall y credenciales.
- Advertencia `pkg_resources` de Pygame: es inocua, se puede ignorar.
- `PermissionError` al guardar WAV: resuelto usando archivos temporales; no se reutiliza `voz.wav`.
- Dígitos no admitidos por TTS: se convierten a palabras en español automáticamente.
- Al presionar Ctrl+C: el worker cierra limpio y confirma el mensaje.
- Audio bloqueado o errores de permisos: el bot usa archivos WAV temporales y los elimina al finalizar la reproducción.

🔗 Integración desde PHP 7.4 (referencia)
- Usa una librería AMQP como `php-amqplib/php-amqplib`.
- Publica en la cola `voz` con un JSON que contenga: `nombre`, `ventanilla`, `identidad`, `tipo_identidad`, `preferir_identidad`, y opcionalmente `una_vez` o `intentos`.
- El bot de Python es un proceso independiente; no se ejecuta dentro de PHP.

Ejemplo PHP (publicar en la cola `voz`):
```
<?php
require __DIR__ . '/vendor/autoload.php';

use PhpAmqpLib\Connection\AMQPStreamConnection;
use PhpAmqpLib\Message\AMQPMessage;

$host = getenv('RABBITMQ_HOST') ?: 'localhost';
$port = getenv('RABBITMQ_PORT') ? intval(getenv('RABBITMQ_PORT')) : 5672;
$user = getenv('RABBITMQ_USER') ?: 'muni_bot';
$pass = getenv('RABBITMQ_PASS') ?: 'TU_PASSWORD_FUERTE';

$conn = new AMQPStreamConnection($host, $port, $user, $pass);
$ch = $conn->channel();
$ch->queue_declare('voz', false, true, false, false);

// Ejemplo: llamar una vez por nombre
$payload = [
  'ventanilla' => 7,
  'nombre' => 'Eduardo Saldaña',
  'una_vez' => true,
];

$msg = new AMQPMessage(json_encode($payload), ['content_type' => 'application/json']);
$ch->basic_publish($msg, '', 'voz');

echo "Mensaje enviado: ", json_encode($payload), "\n";
$ch->close();
$conn->close();
```

Ejemplo con identidad y 2 intentos:
```
$payload = [
  'ventanilla' => 3,
  'identidad' => '12345678',
  'tipo_identidad' => 'dni',
  'preferir_identidad' => true,
  'intentos' => 2,
];
```

📌 Comandos rápidos
- Arrancar worker: `python app/worker.py`
- Enviar por nombre: `python app/producer.py --ventanilla 7 --nombre "Nombre Apellido"`
- Enviar por DNI: `python app/producer.py --ventanilla 2 --identidad 12345678 --tipo-identidad dni --preferir-identidad`
- Llamar una vez: `python app/producer.py --ventanilla 7 --nombre "Nombre Apellido" --una-vez`
- Llamar con intentos N: `python app/producer.py --ventanilla 7 --nombre "Nombre Apellido" --intentos N`

Con esto, tienes todo lo necesario para instalar RabbitMQ/Erlang, preparar el entorno Python y ejecutar el bot de voz de punta a punta en Windows.