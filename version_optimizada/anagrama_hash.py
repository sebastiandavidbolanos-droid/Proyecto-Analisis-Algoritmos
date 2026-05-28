"""
=============================================================
  DETECCIÓN DE ANAGRAMAS — VERSIÓN OPTIMIZADA (HASHING)
  Complejidad: O(n) ≈ O(1) para alfabetos fijos
=============================================================

Este algoritmo cuenta la frecuencia de cada letra en ambas
palabras y compara los conteos usando tablas hash (Counter).

Funciona instantáneamente incluso con palabras de
    millones de caracteres.
=============================================================
"""

import time
import os
import sys
from collections import Counter

# Agregar el directorio raíz al path para poder importar utils
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from utils import normalizar_texto


def son_anagramas_hash(palabra1: str, palabra2: str, progress_callback=None) -> bool:
    """
    Determina si dos palabras son anagramas usando
    conteo de frecuencias (hash map).

    Complejidad temporal: O(n) donde n = longitud de la palabra
    Complejidad espacial: O(k) donde k = tamaño del alfabeto (constante)
    """
    p1 = normalizar_texto(palabra1)
    p2 = normalizar_texto(palabra2)

    # Verificación rápida de longitud
    if len(p1) != len(p2):
        if progress_callback:
            progress_callback("error", 0, 1, "Difieren en longitud")
        return False

    if progress_callback:
        # Modo GUI: Conteo manual para poder enviar el estado en vivo
        freq1 = {}
        for i, char in enumerate(p1):
            freq1[char] = freq1.get(char, 0) + 1
            # Reportamos avance en la palabra 1
            progress_callback("palabra1", i + 1, len(p1), char, dict(freq1))

        freq2 = {}
        for i, char in enumerate(p2):
            freq2[char] = freq2.get(char, 0) + 1
            # Reportamos avance en la palabra 2
            progress_callback("palabra2", i + 1, len(p2), char, dict(freq2))
            
        son_iguales = (freq1 == freq2)
        progress_callback("resultado", 1, 1, son_iguales)
        return son_iguales
    else:
        # Modo Máxima Velocidad (CLI Benchmark)
        return Counter(p1) == Counter(p2)


def mostrar_frecuencias(palabra: str) -> dict:
    """Muestra las frecuencias de cada letra en una palabra normalizada."""
    p = normalizar_texto(palabra)
    freq = {}
    for char in p:
        freq[char] = freq.get(char, 0) + 1
    return dict(sorted(freq.items()))


# ============================================================
# DEMOSTRACIÓN DE EXPOSICIÓN
# ============================================================
if __name__ == "__main__":
    print("=" * 60)
    print("  DETECCIÓN DE ANAGRAMAS — VERSIÓN OPTIMIZADA O(n) HASH")
    print("=" * 60)
    print()

    # Casos de prueba
    casos = [
        ("roma", "amor"),
        ("Álvaro", "valora"),
        ("hola", "aloh"),
        ("anagrama", "maganara"),
        ("escuchar", "cucharEs"),
        ("atención", "no te inca"),
        ("hello", "world"),
    ]

    for palabra1, palabra2 in casos:
        p1_norm = normalizar_texto(palabra1)
        p2_norm = normalizar_texto(palabra2)
        
        print(f"Buscando: '{palabra1}' vs '{palabra2}'")
        print(f"   Normalizadas: '{p1_norm}' vs '{p2_norm}'")

        # Mostrar frecuencias
        freq1 = mostrar_frecuencias(palabra1)
        freq2 = mostrar_frecuencias(palabra2)
        print(f"   Frecuencias de '{p1_norm}': {freq1}")
        print(f"   Frecuencias de '{p2_norm}': {freq2}")

        # Método Hash Map (Counter)
        inicio = time.perf_counter()
        resultado_hash = son_anagramas_hash(palabra1, palabra2)
        tiempo_hash = time.perf_counter() - inicio

        estado = "[OK] Son anagramas" if resultado_hash else "[X] NO son anagramas"
        print(f"   Resultado: {estado}")
        print(f"   Tiempo Hash Map: {tiempo_hash:.9f} s")
        print()
        print("-" * 60)
        print()

    # Demostración de escalabilidad extrema
    print("=" * 60)
    print("  [START] PRUEBA DE ESCALABILIDAD CON PALABRAS EXTREMADAMENTE LARGAS")
    print("=" * 60)
    print()

    import random
    import string

    for longitud in [100, 1_000, 10_000, 100_000, 1_000_000]:
        # Generar palabra aleatoria
        palabra_original = ''.join(random.choices(string.ascii_lowercase, k=longitud))
        # Crear anagrama (mezclar las letras)
        letras = list(palabra_original)
        random.shuffle(letras)
        anagrama = ''.join(letras)

        inicio = time.perf_counter()
        resultado = son_anagramas_hash(palabra_original, anagrama)
        tiempo = time.perf_counter() - inicio

        print(f"   {longitud:>10,} letras -> {tiempo:.6f} s  ({'[OK]' if resultado else '[X]'})")

    print()
    print("   ¡Incluso con 1,000,000 de letras el conteo por Hash Map tarda milisegundos!")
