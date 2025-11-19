from TTS.api import TTS
import pygame
import time
import tempfile
import os

pygame.mixer.init()

tts = TTS("tts_models/es/css10/vits")


def generar_audio(texto):
    tmp = tempfile.NamedTemporaryFile(suffix=".wav", delete=False)
    path = tmp.name
    tmp.close()
    tts.tts_to_file(text=texto, file_path=path)
    return path


def reproducir_audio(archivo):
    sound = pygame.mixer.Sound(archivo)
    channel = sound.play()
    try:
        while channel.get_busy():
            time.sleep(0.1)
    finally:
        try:
            os.remove(archivo)
        except OSError:
            pass
