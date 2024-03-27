import numpy as np
import pandas as pd
from scipy.stats import ksone
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from tkinter import messagebox

class KSPruebaFrame(tk.Frame):
    def __init__(self, master=None,archivo_path=None):
        super().__init__(master)
        self.master = master
        self.create_widgets()
        self.archivo_path = archivo_path  # Almacenar la ruta del archivo aquí

    def create_widgets(self):
        # Crear etiqueta del título
        self.tittle_label = ttk.Label(self.master, text="Prueba de Kolmogorov-Smirnov", font=("Helvetica", 14, "bold"))
        self.tittle_label.pack()

        # Etiqueta y entrada para el número de intervalos
        self.interval_label = ttk.Label(self, text="Número de intervalos:")
        self.interval_label.grid(row=1, column=0, padx=5, pady=5, sticky="e")

        self.interval_entry = ttk.Entry(self)
        self.interval_entry.grid(row=1, column=1, padx=5, pady=5, sticky="we")

        # Botón para calcular la prueba
        self.calculate_button = ttk.Button(self, text="Calcular", command=self.calcular_prueba_ks)
        self.calculate_button.grid(row=1, column=2, padx=5, pady=5)

        # Etiqueta para mostrar la máxima diferencia
        self.maximo_dif_label = ttk.Label(self, text="")
        self.maximo_dif_label.grid(row=2, column=0, columnspan=3, padx=5, pady=5)

        # Etiqueta para mostrar el valor crítico
        self.critical_value_label = ttk.Label(self, text="")
        self.critical_value_label.grid(row=3, column=0, columnspan=3, padx=5, pady=5)

        # Etiqueta para mostrar el resultado de la prueba
        self.resultado_label = ttk.Label(self, text="")
        self.resultado_label.grid(row=4, column=0, columnspan=3, padx=5, pady=5)

        # Configuración de la tabla de frecuencias
        self.tabla_frecuencias = ttk.Treeview(self, columns=("Intervalo", "Frecuencia", "Frecuencia Acumulada",
                                                          "Probabilidad Acumulada", "Frecuencia Esperada Acumulada",
                                                          "Probabilidad Esperada Acumulada", "Diferencia"))

    # Configurar la tabla de frecuencias
        self.tabla_frecuencias.heading("#0", text="Índice")
        for col in self.tabla_frecuencias['columns']:
            self.tabla_frecuencias.heading(col, text=col)
        self.tabla_frecuencias.column("#0", stretch=tk.NO, width=0)
        for col in self.tabla_frecuencias['columns']:
            self.tabla_frecuencias.column(col, anchor=tk.CENTER)

        # Mostrar la tabla en la interfaz
        self.tabla_frecuencias.grid(row=5, column=0, columnspan=3, padx=5, pady=5)

   
    def calcular_prueba_ks(self):
        # Obtener el nombre del archivo CSV desde la entrada del usuario
        nombre_archivo = self.archivo_path

        # Leer los datos desde el archivo CSV
        datos = self.leer_datos_desde_csv(nombre_archivo)
        if datos is None:
            return

        # Obtener el número de intervalos desde la entrada del usuario
        try:
            interval = int(self.interval_entry.get())
        except ValueError:
            messagebox.showerror("Error", "Por favor, introduzca un número válido de intervalos.")
            return

        # Realizar los cálculos
        n = len(datos)
        minimo = min(datos)
        maximo = max(datos)
        intervalos = np.linspace(minimo, maximo, num=interval + 1)
        frecuencias, bordes_intervalos = np.histogram(datos, bins=intervalos)
        frecuencia_acumulada = np.cumsum(frecuencias)
        probabilidad_acumulada = frecuencia_acumulada / n
        frecuencia_esperada_acumulada = np.arange(1, interval + 1) * n / interval
        probabilidad_esperada_acumulada = frecuencia_esperada_acumulada / n
        dif = abs(probabilidad_esperada_acumulada - probabilidad_acumulada)
        maximo_dif = round(max(dif), 2)

        # Calcular el valor crítico para la prueba de Kolmogorov-Smirnov
        alpha = 0.05  # Nivel de significancia
        critical_value = round(ksone.ppf(1 - alpha / 2, n), 5)

        # Evaluar el resultado de la prueba
        resultado = maximo_dif < critical_value

        # Crear un DataFrame con los resultados
        data = {
            "Intervalo": [f"{bordes_intervalos[i]:.5f} - {bordes_intervalos[i + 1]:.5f}" for i in range(len(frecuencias))],
            "Frecuencia": frecuencias,
            "Frecuencia Acumulada": frecuencia_acumulada,
            "Probabilidad Acumulada": probabilidad_acumulada,
            "Frecuencia Esperada Acumulada": frecuencia_esperada_acumulada,
            "Probabilidad Esperada Acumulada": probabilidad_esperada_acumulada,
            "Diferencia": dif
        }

        # Mostrar los resultados en la interfaz gráfica
        self.maximo_dif_label.config(text=f"Maxima diferencia = {maximo_dif}")
        self.critical_value_label.config(text=f"Valor crítico para alpha={alpha} y n={n}: {critical_value}")
        self.resultado_label.config(text=f"Resultado de la prueba: {'Aceptado' if resultado else 'Rechazado'}")

        # Limpiar la tabla antes de agregar nuevos datos
        self.tabla_frecuencias.delete(*self.tabla_frecuencias.get_children())

        # Agregar los datos a la tabla
        for i in range(len(frecuencias)):
            self.tabla_frecuencias.insert("", "end", values=(
                f"{bordes_intervalos[i]:.5f} - {bordes_intervalos[i + 1]:.5f}",
                frecuencias[i],
                frecuencia_acumulada[i],
                probabilidad_acumulada[i],
                frecuencia_esperada_acumulada[i],
                probabilidad_esperada_acumulada[i],
                dif[i]
            ))

    def leer_datos_desde_csv(self, nombre_archivo):
        try:
            # Leer el archivo CSV
            df = pd.read_csv(nombre_archivo, header=None)

            # Convertir los datos a una lista
            datos = df.values.flatten().tolist()

            return datos

        except FileNotFoundError:
            messagebox.showerror("Error", f"El archivo '{nombre_archivo}' no fue encontrado.")
            return None
        except Exception as e:
            messagebox.showerror("Error", f"Ocurrió un error al leer el archivo CSV: {e}")
            return None


