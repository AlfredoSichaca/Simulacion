import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter import ttk
from scipy.stats import norm
import math
import numpy as np

class MediosApp(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.archivo_path = None

        self.create_widgets()

    def create_widgets(self):
        self.label = tk.Label(self.master, text="Seleccione un archivo CSV:")
        self.label.pack(pady=10)

        self.buscar_frame = tk.Frame(self.master)
        self.buscar_frame.pack(pady=5)

        self.ruta_entry = tk.Entry(self.buscar_frame, width=40)
        self.ruta_entry.pack(side="left", padx=5)

        self.buscar_button = tk.Button(self.buscar_frame, text="Buscar Archivo", command=self.buscar_archivo)
        self.buscar_button.pack(side="left", padx=5)

        self.calcular_button = tk.Button(self.master, text="Calcular", command=self.calcular_resultados)
        self.calcular_button.pack()

        self.table = ttk.Treeview(self.master, columns=("Valor", "Calculado"), show="headings")
        self.table.heading("Valor", text="Valor", anchor=tk.CENTER)
        self.table.heading("Calculado", text="Calculado", anchor=tk.CENTER)
        self.table.column("Valor", width=150, anchor=tk.CENTER)
        self.table.column("Calculado", width=150, anchor=tk.CENTER)
        self.table.pack(pady=20)

        self.scrollbar = ttk.Scrollbar(self.master, orient="vertical", command=self.table.yview)
        self.scrollbar.pack(side="right", fill="y")
        self.table.configure(yscrollcommand=self.scrollbar.set)

    def buscar_archivo(self):
        archivo_path = filedialog.askopenfilename(filetypes=[("Archivo CSV", "*.csv")])
        if archivo_path:
            self.archivo_path = archivo_path
            self.ruta_entry.delete(0, tk.END)
            self.ruta_entry.insert(0, archivo_path)

    def calcular_resultados(self):
        if self.archivo_path:
            try:
                with open(self.archivo_path, 'r') as file:
                    datos = file.read().strip().split(',')
                    datos = [float(dato) for dato in datos]
                resultados = self.analizar_datos(datos)
                self.mostrar_resultados(resultados)
            except Exception as e:
                messagebox.showerror("Error", f"No se pudo procesar el archivo: {e}")
        else:
            messagebox.showerror("Error", "Por favor, seleccione un archivo antes de calcular los resultados.")

    def analizar_datos(self, datos):
        aceptacion = 95 / 100
        alpha = 5 / 100
        n = len(datos)
        R = np.mean(datos)
        resta = (1 - (alpha / 2))
        valor_z = norm.ppf(resta)
        li = (1 / 2) - (valor_z * (1 / (math.sqrt(12 * n))))
        ls = (1 / 2) + (valor_z * (1 / (math.sqrt(12 * n))))
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
        for clave, valor in resultados.items():
            self.table.insert("", "end", values=(clave, valor))

if __name__ == "__main__":
    root = tk.Tk()
    app = MediosApp(master=root)
    app.pack()
    app.mainloop()