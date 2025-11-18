def limpiar_texto(texto):
    """Limpia texto antes de enviarlo a TTS."""
    texto = texto.strip()
    texto = " ".join(texto.split())
    return texto
