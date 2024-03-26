import tkinter as tk
from tkinter import messagebox
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import pandas as pd
from scipy.stats import norm
import seaborn as sns

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

        # Primera fila
        tk.Label(frame_inputs, text="X0:").grid(row=0, column=0, padx=5)
        self.entry_x0 = tk.Entry(frame_inputs, width=10)
        self.entry_x0.grid(row=0, column=1, padx=5)

        tk.Label(frame_inputs, text="k:").grid(row=0, column=2, padx=5)
        self.entry_k = tk.Entry(frame_inputs, width=10)
        self.entry_k.grid(row=0, column=3, padx=5)

        tk.Label(frame_inputs, text="c:").grid(row=0, column=4, padx=5)
        self.entry_c = tk.Entry(frame_inputs, width=10)
        self.entry_c.grid(row=0, column=5, padx=5)

        tk.Label(frame_inputs, text="g:").grid(row=0, column=6, padx=5)
        self.entry_g = tk.Entry(frame_inputs, width=10)
        self.entry_g.grid(row=0, column=7, padx=5)

        # Segunda fila
        tk.Label(frame_inputs, text="Mínimo:").grid(row=1, column=0, padx=5)
        self.entry_min = tk.Entry(frame_inputs, width=10)
        self.entry_min.grid(row=1, column=1, padx=5)

        tk.Label(frame_inputs, text="Máximo:").grid(row=1, column=2, padx=5)
        self.entry_max = tk.Entry(frame_inputs, width=10)
        self.entry_max.grid(row=1, column=3, padx=5)

        tk.Label(frame_inputs, text="Cantidad:").grid(row=1, column=4, padx=5)
        self.entry_cantidad = tk.Entry(frame_inputs, width=10)
        self.entry_cantidad.grid(row=1, column=5, padx=5)

        tk.Button(frame_inputs, text="Generar", command=self.generar_datos).grid(row=1, column=6, padx=5, pady=10, columnspan=2)

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
            x0 = float(self.entry_x0.get())
            k = float(self.entry_k.get())
            c = float(self.entry_c.get())
            g = float(self.entry_g.get())
            min_val = float(self.entry_min.get())
            max_val = float(self.entry_max.get())
            cantidad = int(self.entry_cantidad.get())
            a = 1 + 2 * k
            m = 2 ** g
            semilla = x0

            xn_valores = []
            for _ in range(cantidad):
                semilla = (a * semilla + c) % m
                xn_valores.append(semilla)

            std_dev = np.std(xn_valores, ddof=1)
            promedio = np.mean(xn_valores)

            df = pd.DataFrame({"Xi": xn_valores})
            df["R1"] = df["Xi"] / (m - 1)
            df['Ni1'] = norm.ppf(df['R1'], loc=promedio, scale=std_dev)
            df[" "] = " "
            df["Ri2"] = df["Xi"] / m
            df['Ni2'] = norm.ppf(df['Ri2'], loc=promedio, scale=std_dev)

            numeros_aleatorios = df['Ni2']

            # Actualizar la tabla
            self.table.delete("1.0", tk.END)
            for i, valor in enumerate(numeros_aleatorios):
                self.table.insert(tk.END, f"{i + 1}\t{valor:.6f}\n")

            # Calcular promedio y desviación estándar
            self.resultado_promedio.config(text=f"{promedio:.6f}")
            self.resultado_desviacion.config(text=f"{std_dev:.6f}")

            # Actualizar el gráfico
            self.ax.clear()
            self.ax.hist(numeros_aleatorios, bins=20, density=True, alpha=0.5, color='blue')
            sns.kdeplot(numeros_aleatorios, color='orange', label='Densidad de probabilidad')
            self.ax.set_title("Distribución Normal")
            self.canvas.draw()

        except ValueError:
            messagebox.showwarning("Error", "Los valores ingresados no son válidos.")