🗣️ Bot de Voz con Python + Coqui TTS

Este proyecto implementa un bot de voz utilizando Python, Coqui TTS para síntesis de voz y un entorno virtual para mantener dependencias aisladas.

✅ Requisitos previos (Windows)

Antes de comenzar asegúrate de tener instalado:

1. Python 3.10.x

Verifica tu versión:

python --version


Debe mostrar algo como:

Python 3.10.x


Si no tienes Python 3.10, descárgalo de:
https://www.python.org/downloads/release/python-3100/

Durante la instalación activa:

✔ Add Python to PATH
✔ Install Python Launcher (py.exe)

🚀 Instalación del Proyecto
1. Clonar o crear la carpeta del proyecto
cd C:\Users\TU_USUARIO\Desktop
mkdir bot_voz
cd bot_voz

2. Crear un entorno virtual (Windows)

Primero verifica la ruta exacta de Python:

where python


Ejemplo de salida:

C:\Users\TU_USUARIO\AppData\Local\Programs\Python\Python310\python.exe


Usa esa ruta para crear el entorno:

"C:\Users\TU_USUARIO\AppData\Local\Programs\Python\Python310\python.exe" -m venv venv

3. Activar el entorno virtual
.\venv\Scripts\Activate.ps1


Si aparece error de permisos(IMPORTANTE):

Set-ExecutionPolicy -Scope CurrentUser -ExecutionPolicy RemoteSigned


Luego activa de nuevo el entorno:

.\venv\Scripts\Activate.ps1

4. Instalar dependencias del proyecto
pip install coqui-tts
pip install sounddevice
pip install numpy
pip install pynput


Si tienes un archivo requirements.txt, también puedes usar:

pip install -r requirements.txt

▶️ Ejecución

Una vez con el entorno activado:

python main.py

📁 Estructura recomendada del proyecto
bot_voz/
│
├── venv/                 (entorno virtual)
│
├── app/
│   ├── producer.py       (envía mensajes a la cola)
│   ├── worker.py         (bot que los lee)
│   ├── tts_engine.py     (motor de voz separado)
│   └── utils.py          (funciones de soporte)
│
└── requirements.txt

🧪 Probar instalación de Coqui TTS

Ejemplo básico:

from TTS.api import TTS

tts = TTS("tts_models/en/ljspeech/tacotron2-DDC", progress_bar=False, gpu=False)
tts.tts_to_file(text="Hola, esto es una prueba de Coqui TTS.", file_path="salida.wav")


Ejecuta:

python main.py

❗ Problemas Comunes
🔹 "python3.10 no se reconoce"

Usa la ruta exacta obtenida con:

where python

🔹 No se activa el entorno virtual

Ejecuta:

Set-ExecutionPolicy -Scope CurrentUser -ExecutionPolicy RemoteSigned

🔹 Coqui TTS tarda en instalar

Es normal: descarga modelos, compila libs y pesa varios MB.