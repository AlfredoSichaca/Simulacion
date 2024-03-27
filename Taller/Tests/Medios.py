
import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter import ttk
from scipy.stats import norm
import math
import numpy as np

class MediosApp(tk.Frame):
    def __init__(self, master=None ,archivo_path=None):
        super().__init__(master)
        self.master = master
        self.archivo_path = archivo_path  # Almacenar la ruta del archivo aquí
        self.create_widgets()

    def create_widgets(self):
        # Crear tabla para mostrar resultados
        self.calcular_button = tk.Button(self.master, text="Calcular Prueba de medias", command=self.calcular_resultados)
        self.calcular_button.pack()

        # Crear tabla para mostrar resultados
        self.table = ttk.Treeview(self.master, columns=("Valor", "Calculado"), show="headings")
        self.table.heading("Valor", text="Valor", anchor=tk.CENTER)
        self.table.heading("Calculado", text="Calculado", anchor=tk.CENTER)
        self.table.column("Valor", width=150, anchor=tk.CENTER)
        self.table.column("Calculado", width=150, anchor=tk.CENTER)
        self.table.pack(pady=20)

        # Configurar scrollbar para la tabla
        self.scrollbar = ttk.Scrollbar(self.master, orient="vertical", command=self.table.yview)
        self.scrollbar.pack(side="right", fill="y")
        self.table.configure(yscrollcommand=self.scrollbar.set)

    def calcular_resultados(self):
        # Verificar si se ha seleccionado un archivo
        if self.archivo_path:
            try:
                # Leer los datos del archivo y convertirlos a números
                with open(self.archivo_path, 'r') as file:
                    datos = file.read().strip().split(',')
                    datos = [float(dato) for dato in datos]
                # Realizar el análisis de los datos
                resultados = self.analizar_datos(datos)
                # Mostrar los resultados en la tabla
                self.mostrar_resultados(resultados)
            except Exception as e:
                # Mostrar error si no se puede procesar el archivo
                messagebox.showerror("Error", f"No se pudo procesar el archivo: {e}")
        else:
             # Mostrar error si no se ha seleccionado un archivo
            messagebox.showerror("Error", "Por favor, seleccione un archivo antes de calcular los resultados.")

    def analizar_datos(self, datos):
        # Definir niveles de aceptación y significancia
        aceptacion = 95 / 100
        alpha = 5 / 100

        # Calcular tamaño de la muestra y la media
        n = len(datos)
        R = np.mean(datos)

        # Calcular valor crítico de Z
        resta = (1 - (alpha / 2))
        valor_z = norm.ppf(resta)

        # Calcular límites de confianza
        li = (1 / 2) - (valor_z * (1 / (math.sqrt(12 * n))))
        ls = (1 / 2) + (valor_z * (1 / (math.sqrt(12 * n))))

        # Determinar si la media está dentro de los límites
        resultado = (R >= li) and (R <= ls)

        return {
            "Aceptacion": aceptacion,
            "Alpha": alpha,
            "N": n,
            "R": R,
            "1 - ( α /2 )": resta,
            "Li": li,
            "Ls": ls,
            "Resultado": resultado
        }

    def mostrar_resultados(self, resultados):
        # Insertar los resultados en la tabla
        for clave, valor in resultados.items():
            self.table.insert("", "end", values=(clave, valor))


