import re
from num2words import num2words

def limpiar_texto(texto):
    texto = texto.strip()
    texto = " ".join(texto.split())
    def repl(m):
        n = int(m.group(0))
        return num2words(n, lang="es")
    texto = re.sub(r"\d+", repl, texto)
    return texto

def identidad_a_palabras(identidad):
    mapa = {
        "0": "cero",
        "1": "uno",
        "2": "dos",
        "3": "tres",
        "4": "cuatro",
        "5": "cinco",
        "6": "seis",
        "7": "siete",
        "8": "ocho",
        "9": "nueve",
    }
    salida = []
    for ch in str(identidad):
        if ch.isdigit():
            salida.append(mapa.get(ch, ch))
        else:
            salida.append(ch)
    return " ".join(salida)
