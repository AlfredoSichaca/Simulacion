import tkinter as tk
from tkinter import messagebox
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

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

        tk.Label(frame_inputs, text="Mínimo:").grid(row=0, column=0, padx=5)
        self.entry_minimo = tk.Entry(frame_inputs, width=5)
        self.entry_minimo.grid(row=0, column=1, padx=5)

        tk.Label(frame_inputs, text="Máximo:").grid(row=0, column=2, padx=5)
        self.entry_maximo = tk.Entry(frame_inputs, width=5)
        self.entry_maximo.grid(row=0, column=3, padx=5)

        tk.Label(frame_inputs, text="Cantidad:").grid(row=0, column=4, padx=5)
        self.entry_cantidad = tk.Entry(frame_inputs, width=5)
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
        self.label_promedio = tk.Label(frame_results, text="")
        self.label_promedio.pack(side="left")

    def generar_datos(self):
        try:
            minimo = float(self.entry_minimo.get())
            maximo = float(self.entry_maximo.get())
            cantidad = int(self.entry_cantidad.get())
            numeros_aleatorios = np.random.uniform(minimo, maximo, cantidad)

            # Actualizar la tabla
            self.table.delete("1.0", tk.END)
            for i, valor in enumerate(numeros_aleatorios):
                self.table.insert(tk.END, f"{i + 1}\t{valor:.6f}\n")

            # Calcular promedio
            promedio = np.mean(numeros_aleatorios)
            self.label_promedio.config(text=f"{promedio:.6f}")

            # Actualizar el gráfico
            self.ax.clear()
            self.ax.hist(numeros_aleatorios, bins=20, density=True)
            x = np.linspace(minimo, maximo, 100)
            self.ax.plot(x, np.full_like(x, 1 / (maximo - minimo)), '--')
            self.ax.set_title("Distribución Uniforme")
            self.canvas.draw()

        except ValueError:
            messagebox.showwarning("Error", "Los valores ingresados no son válidos.")

if __name__ == "__main__":
    root = tk.Tk()
    app = VentanaPrincipal(master=root)
    app.pack()
    app.mainloop()
