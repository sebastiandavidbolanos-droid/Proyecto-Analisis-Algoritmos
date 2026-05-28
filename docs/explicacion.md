# Explicación Teórica — Detección de Anagramas

Este documento sirve como guía teórica y de apoyo para la exposición del proyecto de detección de anagramas. Explica los tres enfoques implementados, sus complejidades computacionales y el ingenio matemático detrás de la optimización lineal.

---

## 📌 Definición del Problema

Un **Anagrama** es una palabra o frase obtenida mediante la transposición (reorganización) de las letras de otra palabra o frase.

*   **Ejemplos:**
    *   `"roma"` $\leftrightarrow$ `"amor"` (Anagramas exactos)
    *   `"Álvaro"` $\leftrightarrow$ `"valora"` (Requiere normalizar el acento `Á` y las mayúsculas)
    *   `"atención"` $\leftrightarrow$ `"no te inca"` (Requiere ignorar espacios y acentos)

---

## 🐌 Algoritmo 1: Fuerza Bruta — Permutaciones

### Idea Clave
Generar **todas** las ordenaciones (permutaciones) posibles de las letras de la primera palabra y verificar si la segunda palabra coincide con alguna de ellas.

### Análisis de Complejidad
*   **Complejidad Temporal:** $\mathcal{O}(n!)$ donde $n$ es la longitud de la palabra.
*   **Complejidad Espacial:** $\mathcal{O}(n!)$ si se almacenan todas las permutaciones en memoria, o $\mathcal{O}(n)$ de forma incremental.

### La Explosión Combinatoria
El crecimiento factorial es el más rápido de las complejidades algorítmicas, haciendo inutilizable el programa para palabras medianas o largas:

| $n$ (Letras útiles) | $n!$ (Permutaciones) | Tiempo de ejecución estimado |
| :---: | :---: | :---: |
| 5 | 120 | < 0.0001 segundos |
| 8 | 40,320 | 0.004 segundos |
| 10 | 3,628,800 | ~3 segundos |
| 12 | 479,001,600 | ~6 minutos |
| 15 | 1.3 billones | ~15 días |

---

## ⚡ Algoritmo 2: Tabla Hash (Conteo de Frecuencias)

### Idea Clave
Dos palabras son anagramas si y solo si contienen **las mismas letras** con **la misma frecuencia de aparición**. En lugar de permutar, contamos.

### Análisis de Complejidad
*   **Complejidad Temporal:** $\mathcal{O}(n)$ donde $n$ es la longitud de la palabra. Recorrer la palabra e insertar en la tabla hash toma tiempo lineal.
*   **Complejidad Espacial:** $\mathcal{O}(k)$ donde $k$ es el tamaño del alfabeto. Al estar acotado el alfabeto español ($k = 27$ letras), el espacio auxiliar es considerado $\mathcal{O}(1)$ (constante).

---

## 🧮 Algoritmo 3: Producto de Números Primos (Ingenio Matemático)

### Fundamento Teórico: Teorema Fundamental de la Aritmética
> "Todo número entero positivo mayor que 1 puede ser representado de forma única como un producto de números primos."

### Implementación del Ingenio
Asignamos un número primo único a cada una de las 27 letras del alfabeto español:

$$\begin{aligned}
\text{'a'} \rightarrow 2, \quad \text{'b'} \rightarrow 3, \quad \text{'c'} \rightarrow 5, \quad \text{'d'} \rightarrow 7, \quad \dots \quad \text{'ñ'} \rightarrow 47, \quad \dots \quad \text{'z'} \rightarrow 103
\end{aligned}$$

Al procesar una palabra, multiplicamos los primos asociados a cada letra. 

*   **Propiedad Conmutativa:** Como la multiplicación es conmutativa ($a \times b = b \times a$), el orden de las letras no altera el producto final.
*   **Propiedad de Unicidad:** Dos palabras tendrán exactamente el mismo producto si y solo si están compuestas por las mismas letras con las mismas frecuencias (es decir, si son anagramas).
*   **Ausencia de Colisiones:** No existe la posibilidad de falsos positivos debido a la unicidad de la factorización prima.

### Ejemplo Práctico (Exposición)
Comparemos `"roma"` y `"amor"`:

*   Asignaciones: `a=2`, `m=41`, `o=53`, `r=67`.
*   Producto de `"roma"` ($r \times o \times m \times a$):
    $$67 \times 53 \times 41 \times 2 = 291,182$$
*   Producto de `"amor"` ($a \times m \times o \times r$):
    $$2 \times 41 \times 53 \times 67 = 291,182$$

Como $291,182 = 291,182$, determinamos de inmediato que **son anagramas** en tiempo lineal y sin usar estructuras complejas de tablas hash en memoria.

---

## 📊 Comparación y Decisiones de Diseño

### Cuadro Comparativo de los 3 Enfoques

| Aspecto | Permutaciones | Hash Map (Counter) | Producto de Primos |
| :--- | :--- | :--- | :--- |
| **Complejidad Temporal** | $\mathcal{O}(n!)$ | $\mathcal{O}(n)$ | $\mathcal{O}(n)$ |
| **Complejidad Espacial** | $\mathcal{O}(n)$ (pila de recursión) | $\mathcal{O}(k) \approx \mathcal{O}(1)$ | $\mathcal{O}(1)$ (un único entero) |
| **Límite de Escalabilidad** | ~9-10 letras | Millones de letras | Decenas de miles de letras |
| **Ventaja Principal** | Intuitivo conceptualmente | Sencillo y estándar | Extremadamente rápido en palabras normales |
| **Desventaja Principal** | Explosión combinatoria | Requiere instanciar objetos Hash Map | Desbordamiento numérico / Aritmética de números grandes |

### El Trade-Off de la Aritmética Arbitraria (Punto Fuerte de la Exposición)
Al realizar benchmarks con palabras extremadamente largas ($n > 10,000$), se observa que el algoritmo de **Hash Map es más rápido que el de Primos**. 

**¿Por qué ocurre esto si ambos son O(n)?**
*   El producto de $50,000$ números primos genera un número entero con miles de dígitos.
*   Python maneja enteros de precisión arbitraria (bignums) de forma automática, pero multiplicar números de miles de dígitos tiene un costo computacional no despreciable.
*   En contraste, la tabla Hash incrementa contadores pequeños, lo que mantiene el tiempo constante por operación.
*   **Conclusión:** Para palabras humanas convencionales (longitud $\le 30$), el Producto de Primos es hasta **6 veces más rápido** debido a que evita el overhead de crear un diccionario en memoria. Para secuencias genómicas u objetos gigantes, la Tabla Hash es superior.

---

## 🌎 Aplicaciones en el Mundo Real

1.  **Sistemas de Búsqueda y SEO:** Agrupar palabras que contienen las mismas letras pero en diferente orden para sugerencias ortográficas.
2.  **Criptografía Histórica:** Los cifrados por transposición (como el anagrama) sentaron las bases del cifrado de datos moderno.
3.  **Procesamiento de Lenguaje Natural (PLN):** Normalización de tokens para búsquedas basadas en raíces léxicas.
