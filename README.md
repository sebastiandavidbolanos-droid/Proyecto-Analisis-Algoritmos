# Proyecto Anagramas: Comparación de Complejidad Algorítmica y Optimización

Este repositorio contiene un estudio comparativo y práctico de algoritmos para resolver el problema de la **detección de anagramas**, diseñado para fines de **exposición académica o profesional**.

El objetivo es demostrar cómo el ingenio matemático y el diseño de estructuras de datos permiten reducir una complejidad temporal exponencial a una lineal, logrando una escalabilidad masiva.

---

## 🚀 Guía Rápida para la Exposición

### 1. Ejecutar las Pruebas Unitarias
Para demostrar que los tres algoritmos funcionan de manera idéntica y correcta en todos los casos de prueba (incluyendo mayúsculas, espacios y acentos en español):
```bash
python -m unittest pruebas/test_anagramas.py
```

### 2. Ejecutar el Benchmark
Para medir el rendimiento de los tres algoritmos con diferentes longitudes de palabras en tiempo real:
```bash
python pruebas/benchmark.py
```
*   *Nota:* Observa en la consola cómo a partir de 10 letras el algoritmo de Fuerza Bruta se omite debido al tiempo de espera, mientras que los enfoques optimizados responden instantáneamente.

### 3. Generar Gráficas y Tablas Comparativas
Para regenerar los gráficos visuales de las curvas de complejidad teórica y real de los algoritmos:
```bash
python pruebas/generar_grafica.py
```
*   Los resultados visuales se guardan automáticamente en la carpeta `resultados/`.

---

## 📁 Estructura del Repositorio

```text
proyecto-anagramas/
│
├── version_lenta/
│   └── anagrama_permutaciones.py  <-- Algoritmo O(n!) por Fuerza Bruta
│
├── version_optimizada/
│   ├── anagrama_hash.py          <-- Algoritmo O(n) usando Hash Maps (Counter)
│   └── anagrama_primos.py        <-- Algoritmo O(n) matemático (Producto de Primos)
│
├── pruebas/
│   ├── test_anagramas.py         <-- Suite de pruebas unitarias robustas
│   ├── benchmark.py              <-- Script de análisis de desempeño
│   └── generar_grafica.py        <-- Generador de gráficos comparativos
│
├── resultados/                   <-- Datos y assets visuales generados
│   ├── tiempos.csv
│   ├── grafica_teorica.png
│   ├── grafica_benchmark.png
│   └── tabla_resumen.png
│
├── docs/
│   └── explicacion.md            <-- Documentación teórica completa del proyecto
│
├── utils.py                      <-- Normalización de acentos y caracteres para español
└── README.md                     <-- Esta guía
```

---

## 💡 Puntos Clave a Destacar en la Exposición

1.  **El Problema de Fuerza Bruta $O(n!)$:**
    *   Explicar la explosión combinatoria. Con 15 letras, probar todas las combinaciones tomaría semanas. El algoritmo se ahoga a partir de las 10 letras.
2.  **La Solución Estándar con Hash Map $O(n)$:**
    *   En lugar de reordenar letras, las contamos. Esto reduce el problema a recorrer las palabras una única vez.
3.  **El Ingenio Matemático - Producto de Primos $O(n)$:**
    *   *El Teorema Fundamental de la Aritmética* garantiza que la multiplicación de primos es única para cada conjunto de letras.
    *   Evita usar estructuras de datos en memoria (diccionarios/tablas hash) reduciendo el problema a operaciones aritméticas puras de bajo nivel.
    *   En palabras humanas cortas ($\le 20$ letras), el algoritmo matemático es hasta **6 veces más rápido** que el método Hash debido a que no tiene el overhead de instanciar objetos complejos.
4.  **El Límite del Enfoque Matemático (Bignums):**
    *   Mencionar que para cadenas de texto extremadamente largas (como secuencias de ADN con $n > 10,000$), la tabla Hash recupera la ventaja.
    *   Esto se debe a que el producto de 10,000 primos es un número de miles de dígitos y su multiplicación se vuelve más lenta en Python que el simple incremento de contadores en un diccionario.
