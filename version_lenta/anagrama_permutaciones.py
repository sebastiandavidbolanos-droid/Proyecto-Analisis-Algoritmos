"""
=============================================================
  DETECCIÓN DE ANAGRAMAS — VERSIÓN LENTA (FUERZA BRUTA)
  Complejidad: O(n!)
=============================================================

Este algoritmo genera TODAS las permutaciones posibles de
una palabra y busca si la segunda palabra está entre ellas.

ADVERTENCIA: Para palabras de más de 10 letras,
    este algoritmo puede tardar HORAS o ser imposible.
=============================================================
"""

from itertools import permutations
import time
import os
import sys

# Agregar el directorio raíz al path para poder importar utils
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from utils import normalizar_texto

def factorial(n: int) -> int:
    """Calcula el factorial de n."""
    if n <= 1:
        return 1
    resultado = 1
    for i in range(2, n + 1):
        resultado *= i
    return resultado

def son_anagramas_permutaciones(palabra1: str, palabra2: str, progress_callback=None) -> bool:
    """
    Determina si dos palabras son anagramas generando
    todas las permutaciones de la primera palabra.

    Complejidad temporal: O(n!)
    Complejidad espacial: O(n!) — almacena todas las permutaciones
    """
    p1 = normalizar_texto(palabra1)
    p2 = normalizar_texto(palabra2)

    # Verificación rápida de longitud
    if len(p1) != len(p2):
        if progress_callback: 
            progress_callback("error_longitud", 0, 1, "Longitudes diferentes tras normalizar.")
        return False

    contador = 0
    total_perms = factorial(len(p1))

    # Generar TODAS las permutaciones de la primera palabra
    for perm in permutations(p1):
        contador += 1
        # Convertir la tupla en string
        palabra_permutada = ''.join(perm)
        
        # Reportar progreso a la GUI (cada cierto intervalo para no bloquear la UI en python puro)
        if progress_callback and (contador % 500 == 0 or contador == total_perms or contador < 50):
            progress_callback("progreso", contador, total_perms, palabra_permutada)

        # Comparar con la segunda palabra
        if palabra_permutada == p2:
            if progress_callback:
                progress_callback("exito", contador, total_perms, palabra_permutada)
            print(f"  [OK] Encontrada despues de {contador:,} permutaciones!")
            return True

    if progress_callback:
        progress_callback("fallo", contador, total_perms, "")
        
    print(f"  [X] No encontrada despues de {contador:,} permutaciones.")
    return False

# ============================================================
# DEMOSTRACIÓN DE EXPOSICIÓN
# ============================================================
if __name__ == "__main__":
    print("=" * 60)
    print("  DETECCIÓN DE ANAGRAMAS — VERSIÓN PERMUTACIONES O(n!)")
    print("=" * 60)
    print()

    # Casos de prueba con soporte para acentos
    casos = [
        ("roma", "amor", True),
        ("Álvaro", "valora", True),
        ("casa", "saca", True),
        ("hola", "aloh", True),
        ("python", "nohtyp", True),
        ("hello", "world", False),
    ]

    for palabra1, palabra2, esperado in casos:
        p1_norm = normalizar_texto(palabra1)
        n = len(p1_norm)
        total_perms = factorial(n)

        print(f"Buscando: '{palabra1}' vs '{palabra2}'")
        print(f"   Normalizadas: '{p1_norm}' vs '{normalizar_texto(palabra2)}'")
        print(f"   Letras utiles: {n} -> Permutaciones posibles: {total_perms:,}")

        inicio = time.perf_counter()
        resultado = son_anagramas_permutaciones(palabra1, palabra2)
        fin = time.perf_counter()
        tiempo = fin - inicio

        estado = "[OK] Son anagramas" if resultado else "[X] NO son anagramas"
        print(f"   Resultado: {estado}")
        print(f"   Tiempo transcurrido: {tiempo:.6f} segundos")
        print()

    # Advertencia sobre palabras largas
    print("=" * 60)
    print("[!] ADVERTENCIA sobre escalabilidad:")
    print("=" * 60)
    print()
    for n in [5, 8, 10, 12, 15]:
        f = factorial(n)
        print(f"   {n:>2} letras -> {f:>20,} permutaciones")
    print()
    print("   ¡Con 12-15 letras ya es prácticamente IMPOSIBLE por la explosión combinatoria!")
    print("   Prueba las versiones optimizadas en la carpeta 'version_optimizada/'")
