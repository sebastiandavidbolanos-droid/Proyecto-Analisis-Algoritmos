"""
=============================================================
  BENCHMARK COMPARATIVO — DETECCIÓN DE ANAGRAMAS
  Permutaciones O(n!) vs Hash Map O(n) vs Primos O(n)
=============================================================

Mide los tiempos de ejecución de cada uno de los tres
algoritmos con diferentes tamaños de entrada y guarda
los resultados en un archivo CSV para graficar.
=============================================================
"""

import sys
import os
import time
import csv
import random
import string

# Agregar el directorio raíz al path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from utils import normalizar_texto
from version_lenta.anagrama_permutaciones import son_anagramas_permutaciones, factorial
from version_optimizada.anagrama_hash import son_anagramas_hash
from version_optimizada.anagrama_primos import son_anagramas_primos, calcular_valor_primo


def benchmark_permutaciones(palabra1: str, palabra2: str) -> float:
    """Mide el tiempo de ejecución del algoritmo de permutaciones."""
    inicio = time.perf_counter()
    _ = son_anagramas_permutaciones(palabra1, palabra2)
    fin = time.perf_counter()
    return fin - inicio


def benchmark_hash(palabra1: str, palabra2: str) -> float:
    """Mide el tiempo de ejecución del algoritmo de conteo por hashing."""
    inicio = time.perf_counter()
    _ = son_anagramas_hash(palabra1, palabra2)
    fin = time.perf_counter()
    return fin - inicio


def benchmark_primos(palabra1: str, palabra2: str) -> float:
    """Mide el tiempo de ejecución del algoritmo matemático de primos."""
    inicio = time.perf_counter()
    _ = son_anagramas_primos(palabra1, palabra2)
    fin = time.perf_counter()
    return fin - inicio


def generar_par_anagramas(n: int) -> tuple:
    """Genera un par de palabras que son anagramas válidos de longitud n."""
    # Usar solo caracteres a-z para simplificar la generación
    palabra = ''.join(random.choices(string.ascii_lowercase, k=n))
    letras = list(palabra)
    random.shuffle(letras)
    anagrama = ''.join(letras)
    return palabra, anagrama


def main():
    print("=" * 80)
    print("  INICIANDO BENCHMARK COMPARATIVO - PROYECTO ANAGRAMAS")
    print("=" * 80)
    print()

    # Directorio de resultados
    resultados_dir = os.path.join(os.path.dirname(__file__), '..', 'resultados')
    os.makedirs(resultados_dir, exist_ok=True)

    # Archivo CSV para guardar los resultados
    csv_path = os.path.join(resultados_dir, 'tiempos.csv')

    # Tamaños de palabra a probar
    # Para permutaciones (O(n!)), probamos solo hasta 9 o 10 letras para evitar congelar el script
    tamanos_permutaciones = [3, 4, 5, 6, 7, 8, 9]
    tamanos_optimizados = [3, 4, 5, 6, 7, 8, 9, 10, 50, 100, 500, 1000, 5000, 10000, 50000]

    resultados = []

    print("=== FASE 1: Comparativa con Algoritmo Lento (Permutaciones O(n!)) ===")
    print("-" * 80)
    headers = f"{'Longitud (n)':>12} | {'Permutaciones':>15} | {'Fuerza Bruta (s)':>18} | {'Hash Map (s)':>15} | {'Primos (s)':>15}"
    print(headers)
    print("-" * 80)

    for n in tamanos_permutaciones:
        f = factorial(n)
        palabra1, palabra2 = generar_par_anagramas(n)

        # Medir tiempos
        # Ocultamos la salida en consola propia de las funciones para no inundar el log de benchmark
        old_stdout = sys.stdout
        sys.stdout = open(os.devnull, 'w')
        try:
            t_perm = benchmark_permutaciones(palabra1, palabra2)
        except Exception:
            t_perm = None
        finally:
            sys.stdout.close()
            sys.stdout = old_stdout

        t_hash = benchmark_hash(palabra1, palabra2)
        t_primos = benchmark_primos(palabra1, palabra2)

        print(f"{n:>12} | {f:>15,} | {t_perm:>18.7f} | {t_hash:>15.7f} | {t_primos:>15.7f}")

        resultados.append({
            'n': n,
            'factorial': f,
            'tiempo_permutaciones': t_perm,
            'tiempo_hash': t_hash,
            'tiempo_primos': t_primos
        })

    print()
    print("=== FASE 2: Escalabilidad de Algoritmos Optimizados O(n) a Gran Escala ===")
    print("-" * 80)
    print(f"{'Longitud (n)':>12} | {'Hash Map O(n) (s)':>20} | {'Primos O(n) (s)':>20} | {'Ganancia Primos vs Hash'}")
    print("-" * 80)

    for n in tamanos_optimizados:
        # Si ya se midió en la Fase 1, obtener o saltar duplicados
        if n in tamanos_permutaciones:
            # Buscar el resultado existente
            res_existente = next(r for r in resultados if r['n'] == n)
            t_hash = res_existente['tiempo_hash']
            t_primos = res_existente['tiempo_primos']
        else:
            palabra1, palabra2 = generar_par_anagramas(n)
            t_hash = benchmark_hash(palabra1, palabra2)
            t_primos = benchmark_primos(palabra1, palabra2)
            
            resultados.append({
                'n': n,
                'factorial': 'inf',
                'tiempo_permutaciones': None,
                'tiempo_hash': t_hash,
                'tiempo_primos': t_primos
            })

        factor_mejora = t_hash / t_primos if t_primos > 0 else 0
        print(f"{n:>12,} | {t_hash:>20.7f} | {t_primos:>20.7f} | {factor_mejora:.1f}x {'mas rapido' if factor_mejora >= 1 else 'mas lento'}")

    # Ordenar los resultados por longitud de palabra n
    resultados.sort(key=lambda x: x['n'])

    # Guardar en archivo CSV
    with open(csv_path, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=[
            'n', 'factorial', 'tiempo_permutaciones', 'tiempo_hash', 'tiempo_primos'
        ])
        writer.writeheader()
        for r in resultados:
            row = r.copy()
            writer.writerow(row)

    print()
    print(f"[GUARDADO] Resultados de benchmark guardados con exito en: {os.path.abspath(csv_path)}")
    print()
    print("=" * 80)
    print("  CONCLUYENDO:")
    print("  - Permutaciones O(n!) crece de forma explosiva y es inviable a partir de n=10.")
    print("  - Hash Map O(n) y Primos O(n) mantienen tiempos infimos incluso con n=50,000.")
    print("  - El algoritmo de Primos suele ser ligeramente mas rapido en palabras de tamano regular")
    print("    ya que no requiere estructurar un objeto hash map (Counter), solo hacer multiplicaciones.")
    print("=" * 80)


if __name__ == "__main__":
    main()
