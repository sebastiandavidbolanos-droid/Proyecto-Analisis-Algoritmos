"""
=============================================================
  MÓDULO DE UTILIDADES COMPARTIDAS — PROYECTO ANAGRAMAS
=============================================================
Este archivo contiene la lógica de normalización unificada
para todos los algoritmos de detección de anagramas.

Prioriza la sencillez y la claridad para fines expositivos.
=============================================================
"""

def normalizar_texto(texto: str) -> str:
    """
    Normaliza una cadena de texto para una comparación justa de anagramas:
    1. Convierte todo el texto a minúsculas.
    2. Quita los acentos y diéresis comunes en español (á -> a, ü -> u, etc.).
    3. Mantiene la letra 'ñ', ya que es una letra diferenciada en el abecedario español.
    4. Elimina espacios, números y signos de puntuación.

    Ejemplo:
        "¡Álvaro!" -> "alvaro"
        "Ramón"    -> "ramon"
    """
    # 1. Convertir a minúsculas
    texto = texto.lower()

    # 2. Tabla de reemplazo explícita para acentos (ideal para explicar en diapositivas)
    acentos = {
        'á': 'a', 'é': 'e', 'í': 'i', 'ó': 'o', 'ú': 'u', 'ü': 'u',
        'à': 'a', 'è': 'e', 'ì': 'i', 'ò': 'o', 'ù': 'u'
    }
    for letra_con_acento, letra_limpia in acentos.items():
        texto = texto.replace(letra_con_acento, letra_limpia)

    # 3. Filtrar y conservar únicamente letras de la 'a' a la 'z' y la 'ñ'
    letras_limpias = []
    for caracter in texto:
        if ('a' <= caracter <= 'z') or caracter == 'ñ':
            letras_limpias.append(caracter)

    return "".join(letras_limpias)
