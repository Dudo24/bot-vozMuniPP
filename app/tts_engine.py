from TTS.api import TTS
import pygame
import time

# Inicializar pygame para reproducir audio
pygame.mixer.init()

# Cargar modelo Coqui TTS español
tts = TTS("tts_models/es/css10/vits")


def generar_audio(texto, archivo="voz.wav"):
    """Genera un archivo de audio desde texto."""
    tts.tts_to_file(text=texto, file_path=archivo)
    return archivo


def reproducir_audio(archivo="voz.wav"):
    """Reproduce un archivo de audio WAV."""
    pygame.mixer.music.load(archivo)
    pygame.mixer.music.play()

    while pygame.mixer.music.get_busy():
        time.sleep(0.1)
