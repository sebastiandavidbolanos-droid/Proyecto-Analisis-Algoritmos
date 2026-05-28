"""
=============================================================
  GENERADOR DE GRÁFICAS COMPARATIVAS
  Visualización del benchmark de anagramas (3 Algoritmos)
=============================================================

Genera gráficas que muestran la diferencia radical entre
O(n!), Hashing O(n) y Producto de Primos O(n) para la
detección de anagramas.
=============================================================
"""

import os
import csv
import matplotlib
matplotlib.use('Agg')  # Backend no interactivo para entornos sin GUI
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker


def factorial(n):
    if n <= 1:
        return 1
    resultado = 1
    for i in range(2, n + 1):
        resultado *= i
    return resultado


def generar_grafica_teorica(resultados_dir):
    """
    Genera una gráfica teórica comparando las curvas de complejidad.
    """
    print("Generando grafica de complejidad teorica...")

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 7))
    fig.patch.set_facecolor('#0d1117')

    # Paleta de colores modernos (Aesthetics)
    color_factorial = '#ff6b6b'  # Rojo suave
    color_hash = '#51cf66'       # Verde suave
    color_primos = '#38bdf8'     # Celeste brillante
    color_bg = '#0d1117'
    color_text = '#c9d1d9'
    color_grid = '#21262d'

    n_values = list(range(1, 13))

    # Operaciones teóricas
    ops_factorial = [factorial(n) for n in n_values]
    ops_hash = [n for n in n_values]
    ops_primos = [n for n in n_values]  # Teóricamente ambas son lineales O(n)

    # === GRÁFICA 1: Escala logarítmica (Para ver la forma de las curvas) ===
    ax1.set_facecolor(color_bg)
    ax1.plot(n_values, ops_factorial, 'o-', color=color_factorial,
             linewidth=3, markersize=8, label='O(n!) - Permutaciones (Fuerza Bruta)', zorder=5)
    ax1.plot(n_values, ops_hash, 's-', color=color_hash,
             linewidth=3, markersize=8, label='O(n) - Hash Map (Conteo)', zorder=5)
    ax1.plot(n_values, ops_primos, '^-', color=color_primos,
             linewidth=3, markersize=6, linestyle='--', label='O(n) - Producto de Primos (Matematico)', zorder=4)

    ax1.set_yscale('log')
    ax1.set_xlabel('Tamano de entrada (n letras)', color=color_text, fontsize=12, fontweight='bold')
    ax1.set_ylabel('Operaciones teoricas (escala logaritmica)', color=color_text, fontsize=12, fontweight='bold')
    ax1.set_title('Complejidad Teorica - Escala Logaritmica',
                  color='white', fontsize=14, fontweight='bold', pad=15)
    ax1.legend(fontsize=10, loc='upper left', facecolor='#161b22',
               edgecolor='#30363d', labelcolor=color_text)
    ax1.grid(True, alpha=0.3, color=color_grid)
    ax1.tick_params(colors=color_text)
    ax1.spines['bottom'].set_color(color_grid)
    ax1.spines['left'].set_color(color_grid)
    ax1.spines['top'].set_visible(False)
    ax1.spines['right'].set_visible(False)

    # Anotación llamativa
    ax1.annotate(f'12! = {factorial(12):,}\noperaciones',
                xy=(12, factorial(12)), xytext=(8, factorial(12) * 5),
                arrowprops=dict(arrowstyle='->', color=color_factorial, lw=2),
                fontsize=10, color=color_factorial, fontweight='bold',
                bbox=dict(boxstyle='round,pad=0.3', facecolor='#161b22',
                          edgecolor=color_factorial, alpha=0.9))

    # === GRÁFICA 2: Escala lineal (Muestra la explosión combinatoria) ===
    ax2.set_facecolor(color_bg)
    n_small = list(range(1, 9))
    ops_fact_small = [factorial(n) for n in n_small]
    ops_hash_small = [n for n in n_small]
    ops_primos_small = [n for n in n_small]

    bar_width = 0.25
    ax2.bar([x - bar_width for x in n_small], ops_fact_small, bar_width,
            color=color_factorial, alpha=0.85, label='O(n!) - Permutaciones', zorder=5)
    ax2.bar([x for x in n_small], ops_hash_small, bar_width,
            color=color_hash, alpha=0.85, label='O(n) - Hash Map', zorder=5)
    ax2.bar([x + bar_width for x in n_small], ops_primos_small, bar_width,
            color=color_primos, alpha=0.85, label='O(n) - Primos', zorder=5)

    ax2.set_xlabel('Tamano de entrada (n letras)', color=color_text, fontsize=12, fontweight='bold')
    ax2.set_ylabel('Operaciones teoricas (escala lineal)', color=color_text, fontsize=12, fontweight='bold')
    ax2.set_title('Complejidad Teorica - Escala Lineal',
                  color='white', fontsize=14, fontweight='bold', pad=15)
    ax2.legend(fontsize=10, loc='upper left', facecolor='#161b22',
               edgecolor='#30363d', labelcolor=color_text)
    ax2.grid(True, alpha=0.3, color=color_grid, axis='y')
    ax2.tick_params(colors=color_text)
    ax2.spines['bottom'].set_color(color_grid)
    ax2.spines['left'].set_color(color_grid)
    ax2.spines['top'].set_visible(False)
    ax2.spines['right'].set_visible(False)

    ax2.yaxis.set_major_formatter(ticker.FuncFormatter(lambda x, p: f'{int(x):,}'))

    plt.tight_layout(pad=3)

    path = os.path.join(resultados_dir, 'grafica_teorica.png')
    plt.savefig(path, dpi=150, facecolor=color_bg,
                bbox_inches='tight', pad_inches=0.5)
    plt.close()
    print(f"   [OK] Guardada en: {os.path.abspath(path)}")
    return path


def generar_grafica_benchmark(resultados_dir):
    """
    Genera gráfica con los datos reales del benchmark.
    """
    csv_path = os.path.join(resultados_dir, 'tiempos.csv')

    if not os.path.exists(csv_path):
        print("   [!] No se encontro tiempos.csv. Ejecuta primero benchmark.py")
        return None

    print("Generando grafica de benchmark real...")

    datos = []
    with open(csv_path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            datos.append(row)

    # Separar datos
    n_perm = []
    t_perm = []
    n_hash = []
    t_hash = []
    n_primos = []
    t_primos = []

    for d in datos:
        n = int(d['n'])
        if d.get('tiempo_permutaciones') and d['tiempo_permutaciones'] != 'None' and d['tiempo_permutaciones'] != '':
            n_perm.append(n)
            t_perm.append(float(d['tiempo_permutaciones']))
        if d.get('tiempo_hash') and d['tiempo_hash'] != 'None' and d['tiempo_hash'] != '':
            n_hash.append(n)
            t_hash.append(float(d['tiempo_hash']))
        if d.get('tiempo_primos') and d['tiempo_primos'] != 'None' and d['tiempo_primos'] != '':
            n_primos.append(n)
            t_primos.append(float(d['tiempo_primos']))

    fig, ax = plt.subplots(figsize=(12, 7))
    fig.patch.set_facecolor('#0d1117')
    ax.set_facecolor('#0d1117')

    color_text = '#c9d1d9'
    color_grid = '#21262d'

    if t_perm:
        ax.plot(n_perm, t_perm, 'o-', color='#ff6b6b', linewidth=3,
                markersize=10, label='Fuerza Bruta O(n!)', zorder=5)
    if t_hash:
        ax.plot(n_hash, t_hash, 's-', color='#51cf66', linewidth=3,
                markersize=8, label='Hash Map O(n)', zorder=5)
    if t_primos:
        ax.plot(n_primos, t_primos, '^-', color='#38bdf8', linewidth=2.5,
                markersize=8, label='Producto Primos O(n)', zorder=5)

    ax.set_xlabel('Tamano de entrada (n letras)', color=color_text,
                  fontsize=13, fontweight='bold')
    ax.set_ylabel('Tiempo de ejecucion (segundos)', color=color_text,
                  fontsize=13, fontweight='bold')
    ax.set_title('Benchmark Real - Comparativa de los 3 Algoritmos',
                 color='white', fontsize=16, fontweight='bold', pad=20)
    ax.legend(fontsize=11, facecolor='#161b22', edgecolor='#30363d',
              labelcolor=color_text, loc='upper left')
    ax.grid(True, alpha=0.3, color=color_grid)
    ax.tick_params(colors=color_text)
    ax.spines['bottom'].set_color(color_grid)
    ax.spines['left'].set_color(color_grid)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)

    # Escala logarítmica si la diferencia es masiva
    if t_perm and max(t_perm) / min(t_hash) > 100:
        ax.set_yscale('log')
        ax.set_ylabel('Tiempo de ejecucion (segundos, escala logaritmica)',
                      color=color_text, fontsize=13, fontweight='bold')

    plt.tight_layout(pad=2)

    path = os.path.join(resultados_dir, 'grafica_benchmark.png')
    plt.savefig(path, dpi=150, facecolor='#0d1117',
                bbox_inches='tight', pad_inches=0.5)
    plt.close()
    print(f"   [OK] Guardada en: {os.path.abspath(path)}")
    return path


def generar_tabla_resumen(resultados_dir):
    """
    Genera una imagen con la tabla resumen de complejidades.
    """
    print("Generando tabla resumen...")

    fig, ax = plt.subplots(figsize=(11, 5.5))
    fig.patch.set_facecolor('#0d1117')
    ax.set_facecolor('#0d1117')
    ax.axis('off')

    columnas = ['Letras (n)', 'Permutaciones\nO(n!)', 'Hash Map\nO(n)', 'Primos\nO(n)', 'Reduccion de Ops']
    datos_tabla = []
    for n in [3, 5, 7, 8, 10, 12, 15]:
        f = factorial(n)
        datos_tabla.append([
            str(n),
            f'{f:,}',
            str(n),
            str(n),
            f'{f // n:,}x menos ops'
        ])

    tabla = ax.table(
        cellText=datos_tabla,
        colLabels=columnas,
        cellLoc='center',
        loc='center',
        colWidths=[0.12, 0.22, 0.15, 0.15, 0.32],
    )

    tabla.auto_set_font_size(False)
    tabla.set_fontsize(11)

    for (row, col), cell in tabla.get_celld().items():
        cell.set_edgecolor('#30363d')
        if row == 0:
            cell.set_facecolor('#238636')  # Encabezado verde Github
            cell.set_text_props(color='white', fontweight='bold', fontsize=10)
            cell.set_height(0.12)
        else:
            cell.set_facecolor('#161b22')
            cell.set_text_props(color='#c9d1d9')
            cell.set_height(0.1)
            # Colorear Permutaciones
            if col == 1:
                valor = factorial(int(datos_tabla[row - 1][0]))
                if valor > 1000000:
                    cell.set_text_props(color='#ff6b6b', fontweight='bold')
            # Colorear Hash
            if col == 2:
                cell.set_text_props(color='#51cf66', fontweight='bold')
            # Colorear Primos
            if col == 3:
                cell.set_text_props(color='#38bdf8', fontweight='bold')
            # Colorear Reducción
            if col == 4:
                cell.set_text_props(color='#ffd43b')

    ax.set_title('Tabla Comparativa Teorica: Complejidades',
                 color='white', fontsize=16, fontweight='bold', pad=20, y=0.95)

    path = os.path.join(resultados_dir, 'tabla_resumen.png')
    plt.savefig(path, dpi=150, facecolor='#0d1117',
                bbox_inches='tight', pad_inches=0.5)
    plt.close()
    print(f"   [OK] Guardada en: {os.path.abspath(path)}")
    return path


def main():
    print("=" * 60)
    print("  GENERANDO GRÁFICAS - Proyecto Anagramas")
    print("=" * 60)
    print()

    resultados_dir = os.path.join(os.path.dirname(__file__), '..', 'resultados')
    os.makedirs(resultados_dir, exist_ok=True)

    generar_grafica_teorica(resultados_dir)
    print()
    generar_grafica_benchmark(resultados_dir)
    print()
    generar_tabla_resumen(resultados_dir)

    print()
    print("=" * 60)
    print("  [OK] Todas las graficas y tablas actualizadas con exito!")
    print(f"  [DIR] Directorio: {os.path.abspath(resultados_dir)}")
    print("=" * 60)


if __name__ == "__main__":
    main()
