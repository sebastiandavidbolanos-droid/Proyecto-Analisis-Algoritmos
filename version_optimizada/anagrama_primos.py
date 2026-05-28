"""
=============================================================
  DETECCIÓN DE ANAGRAMAS — VERSIÓN MATEMÁTICA (PRIMOS)
  Complejidad: O(n) en tiempo, O(1) en espacio auxiliar
=============================================================

Este algoritmo asigna un número primo único a cada una de las
27 letras del abecedario español (incluyendo la 'ñ').
Para comprobar si dos palabras son anagramas, multiplica los
primos de sus letras correspondientes y compara los productos.

Por el Teorema Fundamental de la Aritmética:
"Todo número entero positivo se puede representar de forma única
como producto de factores primos."

Por lo tanto:
- El producto resultante es único para cada combinación de letras.
- Como la multiplicación es conmutativa, el orden de las letras
  no altera el producto (ej. "roma" y "amor" producen el mismo número).
- Dos palabras son anagramas si y solo si sus productos son idénticos.

Sin colisiones de hash (seguridad matemática del 100%).
Complejidad temporal de O(n) con bajísimo costo constante.
=============================================================
"""

import time
import os
import sys

# Agregar el directorio raíz al path para poder importar utils
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from utils import normalizar_texto

# Mapeo de las 27 letras del alfabeto español a los primeros 27 números primos
PRIMOS_ALFABETO = {
    'a': 2,   'b': 3,   'c': 5,   'd': 7,   'e': 11,  'f': 13,  'g': 17,
    'h': 19,  'i': 23,  'j': 29,  'k': 31,  'l': 37,  'm': 41,  'n': 43,
    'ñ': 47,  'o': 53,  'p': 59,  'q': 61,  'r': 67,  's': 71,  't': 73,
    'u': 79,  'v': 83,  'w': 89,  'x': 97,  'y': 101, 'z': 103
}

def calcular_valor_primo(palabra_normalizada: str, id_palabra="1", progress_callback=None) -> int:
    """
    Calcula el producto de los números primos de las letras de la palabra.
    """
    producto = 1
    total = len(palabra_normalizada)
    for i, letra in enumerate(palabra_normalizada):
        # Si la letra está en nuestro diccionario, multiplicamos por su primo.
        primo = PRIMOS_ALFABETO.get(letra, 1)
        producto *= primo
        
        if progress_callback:
            progress_callback(id_palabra, i + 1, total, letra, primo, producto)
            
    return producto

def son_anagramas_primos(palabra1: str, palabra2: str, progress_callback=None) -> bool:
    """
    Determina si dos palabras son anagramas multiplicando números primos.

    Complejidad temporal: O(n) donde n = longitud de la palabra.
    Complejidad espacial: O(1) espacio auxiliar (solo almacena el producto).
    """
    p1 = normalizar_texto(palabra1)
    p2 = normalizar_texto(palabra2)

    # Verificación rápida de longitud
    if len(p1) != len(p2):
        if progress_callback:
            progress_callback("error", 0, 1, "Difieren en longitud")
        return False

    # Calcular productos de primos y comparar
    prod1 = calcular_valor_primo(p1, "palabra1", progress_callback)
    prod2 = calcular_valor_primo(p2, "palabra2", progress_callback)
    
    son_iguales = (prod1 == prod2)
    if progress_callback:
        progress_callback("resultado", 1, 1, son_iguales)
        
    return son_iguales

# ============================================================
# DEMOSTRACIÓN DE EXPOSICIÓN
# ============================================================
if __name__ == "__main__":
    print("=" * 65)
    print("  DETECCIÓN DE ANAGRAMAS — ENFOQUE MATEMÁTICO DE NÚMEROS PRIMOS")
    print("=" * 65)
    print()

    casos = [
        ("roma", "amor"),
        ("Álvaro", "valora"),
        ("atención", "no te inca"),
        ("hola", "aloh"),
        ("python", "nohtyp"),
        ("espectador", "respetado"), # No son anagramas (longitud distinta tras normalizar)
        ("casa", "saca")
    ]

    for p1, p2 in casos:
        p1_norm = normalizar_texto(p1)
        p2_norm = normalizar_texto(p2)
        
        val1 = calcular_valor_primo(p1_norm)
        val2 = calcular_valor_primo(p2_norm)
        son_anag = (val1 == val2) and (len(p1_norm) == len(p2_norm))

        print(f"Buscando: '{p1}' vs '{p2}'")
        print(f"   Normalizadas: '{p1_norm}' vs '{p2_norm}'")
        print(f"   Matemáticamente:")
        # Mostrar el cálculo paso a paso para la exposición
        calculo1 = " * ".join(str(PRIMOS_ALFABETO[c]) for c in p1_norm)
        calculo2 = " * ".join(str(PRIMOS_ALFABETO[c]) for c in p2_norm)
        
        print(f"   - '{p1_norm}': {calculo1} = {val1:,}")
        print(f"   - '{p2_norm}': {calculo2} = {val2:,}")
        print(f"   Resultado: {'[OK] SI son anagramas (mismo producto)' if son_anag else '[X] NO son anagramas (diferente producto)'}")
        print("-" * 65)
