"""
=============================================================
  PRUEBAS UNITARIAS DE DETECCIÓN DE ANAGRAMAS
=============================================================
Este script valida la exactitud de los tres algoritmos:
1. Permutaciones (Fuerza Bruta)
2. Hash Map (Conteo de Frecuencias)
3. Producto de Primos (Enfoque Matemático)

Verifica el comportamiento con mayúsculas, espacios, signos
de puntuación, caracteres con acentos en español y casos límite.
=============================================================
"""

import unittest
import os
import sys

# Agregar el directorio raíz al path para importar los módulos
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from version_lenta.anagrama_permutaciones import son_anagramas_permutaciones
from version_optimizada.anagrama_hash import son_anagramas_hash
from version_optimizada.anagrama_primos import son_anagramas_primos


class TestDeteccionAnagramas(unittest.TestCase):
    
    def setUp(self):
        # Lista de funciones a probar para correr los mismos tests en todas
        self.algoritmos = [
            ("Fuerza Bruta (Permutaciones)", son_anagramas_permutaciones),
            ("Hash Map (Conteo)", son_anagramas_hash),
            ("Producto de Primos (Matemático)", son_anagramas_primos)
        ]

    def test_anagramas_basicos(self):
        """Prueba anagramas estándar sencillos en minúsculas."""
        casos = [
            ("roma", "amor"),
            ("gato", "toga"),
            ("saca", "casa"),
            ("hola", "aloh")
        ]
        for nombre, func in self.algoritmos:
            with self.subTest(algoritmo=nombre):
                for p1, p2 in casos:
                    self.assertTrue(func(p1, p2), f"Falló {nombre} con '{p1}' y '{p2}'")

    def test_no_anagramas_mismo_tamano(self):
        """Prueba palabras del mismo tamaño que no son anagramas."""
        casos = [
            ("gato", "pato"),
            ("hola", "pelo"),
            ("casa", "cama"),
            ("perro", "cerro")
        ]
        for nombre, func in self.algoritmos:
            with self.subTest(algoritmo=nombre):
                for p1, p2 in casos:
                    self.assertFalse(func(p1, p2), f"Falló {nombre} con '{p1}' y '{p2}'")

    def test_diferente_longitud(self):
        """Prueba palabras de diferente longitud (debe retornar False inmediatamente)."""
        casos = [
            ("gato", "gatito"),
            ("roma", "romano"),
            ("espectador", "respetado"), # Diferente longitud
            ("hola", "h")
        ]
        for nombre, func in self.algoritmos:
            with self.subTest(algoritmo=nombre):
                for p1, p2 in casos:
                    self.assertFalse(func(p1, p2), f"Falló {nombre} con '{p1}' y '{p2}'")

    def test_normalizacion_mayusculas_y_espacios(self):
        """Prueba el manejo correcto de mayúsculas y espacios en blanco."""
        casos = [
            ("Roma", "amor "),
            (" gato ", "TOGA"),
            ("Enrique", "quieren"),      # "Enrique" y "quieren" son anagramas exactos (e:2, i:1, n:1, q:1, r:1, u:1)
            ("  hoLa  ", "aLOh")
        ]
        for nombre, func in self.algoritmos:
            with self.subTest(algoritmo=nombre):
                for p1, p2 in casos:
                    self.assertTrue(func(p1, p2), f"Falló {nombre} con '{p1}' y '{p2}'")

    def test_normalizacion_acentos_y_signos(self):
        """Prueba la remoción de acentos, diéresis y signos de puntuación del español."""
        casos = [
            ("Álvaro", "valora"),         # Á -> a
            ("atención", "no te inca"),   # ó -> o, espacios eliminados
            ("¡Roma!", "¿Amor?"),        # Puntuación eliminada
            ("pingüino", "un pingio")     # ü -> u
        ]
        for nombre, func in self.algoritmos:
            with self.subTest(algoritmo=nombre):
                for p1, p2 in casos:
                    self.assertTrue(func(p1, p2), f"Falló {nombre} con '{p1}' y '{p2}'")

    def test_letra_enie(self):
        """Prueba que la letra 'ñ' se diferencie de la 'n' correctamente."""
        # 'ñ' vs 'n' no debe ser considerado anagrama
        for nombre, func in self.algoritmos:
            with self.subTest(algoritmo=nombre):
                self.assertFalse(func("nana", "ñaña"), f"Falló {nombre} diferenciando n de ñ")
                self.assertTrue(func("caña", "añac"), f"Falló {nombre} con anagrama conteniendo ñ")

    def test_casos_vacios_y_limites(self):
        """Prueba cadenas vacías o de un solo carácter."""
        for nombre, func in self.algoritmos:
            with self.subTest(algoritmo=nombre):
                # Dos cadenas vacías
                self.assertTrue(func("", ""), f"Falló {nombre} con dos cadenas vacías")
                # Un solo carácter igual
                self.assertTrue(func("a", "a"), f"Falló {nombre} con un carácter igual")
                # Un carácter diferente
                self.assertFalse(func("a", "b"), f"Falló {nombre} con un carácter diferente")


if __name__ == '__main__':
    unittest.main()
