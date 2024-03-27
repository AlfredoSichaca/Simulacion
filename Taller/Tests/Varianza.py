import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from scipy.stats import chi2
import numpy as np

class VarianzaApp(tk.Frame):
    def __init__(self, master=None,archivo_path=None):
        super().__init__(master)
        self.archivo_path = archivo_path  # Almacenar la ruta del archivo aquí
        self.master = master        
        self.archivo_path = archivo_path

        self.create_widgets()

    def create_widgets(self):
        # Etiqueta de título
        self.tittle_label = ttk.Label(self.master, text="Prueba de Varianza", font=("Helvetica", 14, "bold"))
        self.tittle_label.pack()

        # Frame para el botón de cálculo
        self.calcular_frame = tk.Frame(self.master)
        self.calcular_frame.pack(pady=5)

        # Botón para calcular los resultados
        self.calcular_button = tk.Button(self.calcular_frame, text="Calcular", command=self.calcular_resultados)
        self.calcular_button.pack(side="left", padx=5)

        # Frame para la tabla
        self.table_frame = tk.Frame(self.master)
        self.table_frame.pack(pady=20)
        # Tabla para mostrar los valores calculados
        self.table = ttk.Treeview(self.table_frame, columns=("Valor", "Calculado"), show="headings", height=15)
        self.table.heading("Valor", text="Valor", anchor=tk.CENTER)
        self.table.heading("Calculado", text="Calculado", anchor=tk.CENTER)
        self.table.column("Valor", width=250, anchor=tk.CENTER)
        self.table.column("Calculado", width=250, anchor=tk.CENTER)
        self.table.pack(side="left", padx=10)
        # Barra de desplazamiento para la tabla
        self.scrollbar = ttk.Scrollbar(self.table_frame, orient="vertical", command=self.table.yview)
        self.scrollbar.pack(side="right", fill="y")
        self.table.configure(yscrollcommand=self.scrollbar.set)
    
    

    def calcular_resultados(self):
        # Verificar si se ha seleccionado un archivo
        if self.archivo_path:
            try:

                # Leer datos del archivo y convertirlos a una lista de números
                with open(self.archivo_path, 'r') as file:
                    datos = file.read().strip().split(',')
                    datos = [float(dato) for dato in datos]

                # Analizar los datos y calcular los resultados
                resultados = self.analizar_datos(datos)

                # Mostrar los resultados en la tabla
                self.mostrar_resultados(resultados)
            except Exception as e:

                # Mostrar mensaje de error si ocurre un problema al procesar el archivo
                messagebox.showerror("Error", f"No se pudo procesar el archivo: {e}")
        else:
            # Mostrar mensaje de error si no se ha seleccionado un archivo
            messagebox.showerror("Error", "Por favor, seleccione un archivo antes de calcular los resultados.")

    def analizar_datos(self, datos):
        # Definir los parámetros y cálculos necesarios para el análisis de varianza
        aceptacion = 95 / 100
        alpha = 5 / 100
        n = len(datos)
        R = np.mean(datos)
        resta = (1 - (alpha / 2))
        varianza = np.var(datos, ddof=1)
        chi2_value = chi2.ppf(alpha / 2, n - 1)
        chi2_alpha = chi2.ppf(resta, n - 1)
        lsv = chi2_value / (12 * (n - 1))
        liv = chi2_alpha / (12 * (n - 1))
        resultado = (varianza >= lsv) and (varianza <= liv)

        # Devolver un diccionario con los resultados del análisis
        return {
            "Aceptacion": aceptacion,
            "Alpha": alpha,
            "n": n,
            "R": R,
            "1 - ( α /2 )": resta,
            "( α /2 )": (alpha / 2),
            "σ^2": varianza,
            "X^2 α/2 ": chi2_value,
            "X^2 - (α/2)":chi2_alpha,
            "Limite Superior": lsv,
            "Limite Inferior": liv,
            "Resultado": resultado
        }

    def mostrar_resultados(self, resultados):
        # Mostrar los resultados en la tabla
        for clave, valor in resultados.items():
            self.table.insert("", "end", values=(clave, valor))
