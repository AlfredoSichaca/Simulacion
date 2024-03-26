import tkinter as tk
from tkinter import messagebox
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import pandas as pd

class VentanaPrincipal(tk.Frame):
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
        self.label_promedio = tk.Label(frame_results, text="")
        self.label_promedio.pack(side="left")

    def generar_datos(self):
        try:
            x0 = float(self.entry_x0.get())
            k = float(self.entry_k.get())
            c = float(self.entry_c.get())
            g = float(self.entry_g.get())
            min_val = float(self.entry_min.get())
            b = float(self.entry_max.get())
            cantidad = int(self.entry_cantidad.get())
            a = 1 + 2 * k
            m = 2 ** g
            semilla = x0

            xn_valores = []
            for _ in range(cantidad):
                semilla = (a * semilla + c) % m
                xn_valores.append(semilla)
            df = pd.DataFrame({"Xi": xn_valores})
            df["R1"] = df["Xi"] / (m - 1)
            df['Ni1'] = min_val + (b - min_val) * df['R1']
            df[" "] = " "
            df["Ri2"] = df["Xi"] / m
            df['Ni2'] = min_val + (b - min_val) * df['Ri2']

            numeros_aleatorios = df['Ni1']

            self.table.delete("1.0", tk.END)
            for i, valor in enumerate(numeros_aleatorios):
                self.table.insert(tk.END, f"{i + 1}\t{valor:.6f}\n")


            # Actualizar el gráfico
            self.ax.clear()
            self.ax.hist(numeros_aleatorios, bins=20, density=True)
            x = np.linspace(min_val, b, 100)
            self.ax.plot(x, np.full_like(x, 1 / (b - min_val)), '--')
            self.ax.set_title("Distribución Uniforme")
            self.canvas.draw()

        except ValueError:
            messagebox.showwarning("Error", "Los valores ingresados no son válidos.")
