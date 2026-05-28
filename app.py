"""
=============================================================
  APLICACIÓN GRÁFICA PARA EXPOSICIÓN — PROYECTO ANAGRAMAS
=============================================================
Esta interfaz permite ejecutar los diferentes algoritmos y
observar en tiempo real su comportamiento interno y progreso.
=============================================================
"""

import tkinter as tk
from tkinter import ttk
import time
import sys

# Importar algoritmos
from version_lenta.anagrama_permutaciones import son_anagramas_permutaciones
from version_optimizada.anagrama_hash import son_anagramas_hash
from version_optimizada.anagrama_primos import son_anagramas_primos
from utils import normalizar_texto

class AnagramApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Proyecto Anagramas - Demostración en Vivo")
        self.root.geometry("800x650")
        self.root.configure(padx=20, pady=20)
        
        # Variables de control
        self.palabra1_var = tk.StringVar(value="Enrique")
        self.palabra2_var = tk.StringVar(value="quieren")
        self.algoritmo_var = tk.StringVar(value="primos")
        self.progress_var = tk.DoubleVar(value=0.0)
        self.estado_var = tk.StringVar(value="Esperando...")

        self.crear_interfaz()

    def crear_interfaz(self):
        # Título
        titulo = ttk.Label(self.root, text="Detección de Anagramas - Análisis de Complejidad", font=("Segoe UI", 16, "bold"))
        titulo.pack(pady=(0, 20))

        # Marco de Entradas
        frame_inputs = ttk.LabelFrame(self.root, text=" 1. Ingrese las palabras ", padding=15)
        frame_inputs.pack(fill="x", pady=10)

        ttk.Label(frame_inputs, text="Palabra 1:", font=("Segoe UI", 10)).grid(row=0, column=0, padx=5, pady=5)
        ttk.Entry(frame_inputs, textvariable=self.palabra1_var, font=("Segoe UI", 10), width=30).grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(frame_inputs, text="Palabra 2:", font=("Segoe UI", 10)).grid(row=0, column=2, padx=15, pady=5)
        ttk.Entry(frame_inputs, textvariable=self.palabra2_var, font=("Segoe UI", 10), width=30).grid(row=0, column=3, padx=5, pady=5)

        # Marco de Algoritmo
        frame_algo = ttk.LabelFrame(self.root, text=" 2. Seleccione el algoritmo ", padding=15)
        frame_algo.pack(fill="x", pady=10)

        ttk.Radiobutton(frame_algo, text="Fuerza Bruta O(n!) [Permutaciones]", variable=self.algoritmo_var, value="permutaciones").pack(side="left", padx=10)
        ttk.Radiobutton(frame_algo, text="Hash Map O(n) [Conteo Frecuencias]", variable=self.algoritmo_var, value="hash").pack(side="left", padx=10)
        ttk.Radiobutton(frame_algo, text="Ingenio Matemático O(n) [Prod. Primos]", variable=self.algoritmo_var, value="primos").pack(side="left", padx=10)

        # Botón Ejecutar
        btn_ejecutar = ttk.Button(self.root, text="▶ EJECUTAR ANÁLISIS", command=self.ejecutar_analisis)
        btn_ejecutar.pack(pady=20)

        # Marco de Progreso
        frame_progreso = ttk.LabelFrame(self.root, text=" 3. Estado Interno en Vivo ", padding=15)
        frame_progreso.pack(fill="x", pady=10)

        self.lbl_estado = ttk.Label(frame_progreso, textvariable=self.estado_var, font=("Consolas", 10), foreground="#005a9e")
        self.lbl_estado.pack(anchor="w", pady=(0, 10))

        self.progressbar = ttk.Progressbar(frame_progreso, variable=self.progress_var, maximum=100)
        self.progressbar.pack(fill="x")

        # Marco de Consola
        frame_consola = ttk.LabelFrame(self.root, text=" 4. Consola de Logs ", padding=10)
        frame_consola.pack(fill="both", expand=True, pady=10)

        self.consola = tk.Text(frame_consola, height=10, font=("Consolas", 10), bg="#1e1e1e", fg="#cccccc", state="disabled")
        self.consola.pack(fill="both", expand=True)

    def log(self, mensaje):
        """Escribe un mensaje en la consola integrada."""
        self.consola.config(state="normal")
        self.consola.insert("end", mensaje + "\n")
        self.consola.see("end")
        self.consola.config(state="disabled")
        self.root.update_idletasks()

    def callback_handler(self, *args):
        """Maneja las actualizaciones de progreso enviadas por los algoritmos."""
        algoritmo = self.algoritmo_var.get()

        try:
            if algoritmo == "permutaciones":
                tipo, contador, total, texto = args
                pct = (contador / total) * 100
                self.progress_var.set(pct)
                if tipo == "progreso" or tipo == "exito":
                    self.estado_var.set(f"Permutación evaluada ({contador:,}/{total:,}): '{texto}'")

            elif algoritmo == "hash":
                tipo, contador, total, char = args[:4]
                if tipo == "palabra1":
                    pct = (contador / total) * 50
                    diccionario = args[4]
                    self.estado_var.set(f"Analizando P1 | Letra: '{char}' | Frecuencias: {diccionario}")
                elif tipo == "palabra2":
                    pct = 50 + (contador / total) * 50
                    diccionario = args[4]
                    self.estado_var.set(f"Analizando P2 | Letra: '{char}' | Frecuencias: {diccionario}")
                elif tipo == "error":
                    pct = 100
                    self.estado_var.set(f"Error: {char}")
                elif tipo == "resultado":
                    pct = 100
                    self.estado_var.set("Conteo finalizado. Comparando diccionarios...")
                self.progress_var.set(pct)

            elif algoritmo == "primos":
                tipo, contador, total, char = args[:4]
                if tipo == "palabra1":
                    primo, producto = args[4], args[5]
                    pct = (contador / total) * 50
                    self.estado_var.set(f"P1 | Letra '{char}' -> Primo ({primo}) | Producto Acumulado = {producto:,}")
                elif tipo == "palabra2":
                    primo, producto = args[4], args[5]
                    pct = 50 + (contador / total) * 50
                    self.estado_var.set(f"P2 | Letra '{char}' -> Primo ({primo}) | Producto Acumulado = {producto:,}")
                elif tipo == "error":
                    pct = 100
                    self.estado_var.set(f"Error: {char}")
                elif tipo == "resultado":
                    pct = 100
                    self.estado_var.set("Multiplicación finalizada. Comparando productos únicos...")
                self.progress_var.set(pct)

            # Refrescar UI sin pausas artificiales
            self.root.update_idletasks()
        except Exception as e:
            pass

    def ejecutar_analisis(self):
        p1 = self.palabra1_var.get()
        p2 = self.palabra2_var.get()
        alg = self.algoritmo_var.get()

        self.progress_var.set(0)
        self.consola.config(state="normal")
        self.consola.delete("1.0", "end")
        self.consola.config(state="disabled")

        self.log("==================================================")
        self.log(f" INICIANDO ANÁLISIS")
        self.log(f" Palabra 1: '{p1}' (Normalizada: '{normalizar_texto(p1)}')")
        self.log(f" Palabra 2: '{p2}' (Normalizada: '{normalizar_texto(p2)}')")
        self.log(f" Algoritmo seleccionado: {alg.upper()}")
        self.log("==================================================")

        inicio = time.perf_counter()
        resultado = False

        try:
            if alg == "permutaciones":
                # Advertencia si la palabra es muy grande
                if len(normalizar_texto(p1)) > 9:
                    self.log("[!] ADVERTENCIA: Has introducido una palabra larga.")
                    self.log("    El algoritmo O(n!) podría congelar la aplicación por horas.")
                
                resultado = son_anagramas_permutaciones(p1, p2, progress_callback=self.callback_handler)
                
            elif alg == "hash":
                resultado = son_anagramas_hash(p1, p2, progress_callback=self.callback_handler)
                
            elif alg == "primos":
                resultado = son_anagramas_primos(p1, p2, progress_callback=self.callback_handler)

        except Exception as e:
            self.log(f"[ERROR] Ocurrió una excepción: {str(e)}")

        fin = time.perf_counter()
        tiempo = fin - inicio

        self.progress_var.set(100)
        self.estado_var.set("Finalizado")

        self.log("\n--- RESULTADO FINAL ---")
        if resultado:
            self.log("[OK] SÍ SON ANAGRAMAS.")
        else:
            self.log("[X] NO SON ANAGRAMAS.")
        self.log(f"Tiempo de ejecución: {tiempo:.7f} segundos.")
        self.log("==================================================\n")

if __name__ == "__main__":
    # Configuración de estilos visuales
    root = tk.Tk()
    style = ttk.Style(root)
    # Intentar usar un tema nativo limpio si está disponible
    if "clam" in style.theme_names():
        style.theme_use("clam")
        
    app = AnagramApp(root)
    root.mainloop()
