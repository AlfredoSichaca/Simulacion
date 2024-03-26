import tkinter as tk
from tkinter import messagebox
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class VentanaPrincipalN(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master

        # Configuración de la interfaz
        self.create_widgets()

    def create_widgets(self):
        self.create_input_widgets()
        self.create_table_widget()
        self.create_plot_widget()
        self.create_results_widget()

    def create_input_widgets(self):
        # Entradas
        frame_inputs = tk.Frame(self)
        frame_inputs.pack(pady=5)

        tk.Label(frame_inputs, text="Media:").grid(row=0, column=0, padx=5)
        self.entry_media = tk.Entry(frame_inputs, width=10)
        self.entry_media.grid(row=0, column=1, padx=5)

        tk.Label(frame_inputs, text="Desviación estándar:").grid(row=0, column=2, padx=5)
        self.entry_desviacion = tk.Entry(frame_inputs, width=10)
        self.entry_desviacion.grid(row=0, column=3, padx=5)

        tk.Label(frame_inputs, text="Cantidad:").grid(row=0, column=4, padx=5)
        self.entry_cantidad = tk.Entry(frame_inputs, width=10)
        self.entry_cantidad.grid(row=0, column=5, padx=5)

        tk.Button(frame_inputs, text="Generar", command=self.generar_datos).grid(row=0, column=6, padx=5)

    def create_table_widget(self):
        # Tabla
        self.table_frame = tk.Frame(self)
        self.table_frame.pack(pady=5)
        self.table = tk.Text(self.table_frame, height=10, width=40)
        self.table.pack()

    def create_plot_widget(self):
        # Gráfico
        self.figure, self.ax = plt.subplots(figsize=(5, 3))
        self.canvas = FigureCanvasTkAgg(self.figure, master=self)
        self.canvas.get_tk_widget().pack()

    def create_results_widget(self):
        # Resultados
        frame_results = tk.Frame(self)
        frame_results.pack(pady=5)

        tk.Label(frame_results, text="Promedio:").pack(side="left")
        self.resultado_promedio = tk.Label(frame_results, text="")
        self.resultado_promedio.pack(side="left")

        tk.Label(frame_results, text="Desviación estándar:").pack(side="left")
        self.resultado_desviacion = tk.Label(frame_results, text="")
        self.resultado_desviacion.pack(side="left")

    def generar_datos(self):
        try:
            media = float(self.entry_media.get())
            desviacion = float(self.entry_desviacion.get())
            cantidad = int(self.entry_cantidad.get())
            numeros_aleatorios = np.random.normal(media, desviacion, cantidad)

            # Actualizar la tabla
            self.table.delete("1.0", tk.END)
            for i, valor in enumerate(numeros_aleatorios):
                self.table.insert(tk.END, f"{i + 1}\t{valor:.6f}\n")

            # Calcular promedio y desviación estándar
            promedio = np.mean(numeros_aleatorios)
            desviacion_estandar = np.std(numeros_aleatorios)
            self.resultado_promedio.config(text=f"{promedio:.6f}")
            self.resultado_desviacion.config(text=f"{desviacion_estandar:.6f}")

            # Actualizar el gráfico
            self.ax.clear()
            self.ax.hist(numeros_aleatorios, bins=20, density=True)
            x = np.linspace(min(numeros_aleatorios), max(numeros_aleatorios), 100)
            self.ax.plot(x, np.exp(-(x - media)**2 / (2 * desviacion**2)) / (np.sqrt(2 * np.pi) * desviacion))
            self.ax.set_title("Distribución Normal")
            self.canvas.draw()

        except ValueError:
            messagebox.showwarning("Error", "Los valores ingresados no son válidos.")
