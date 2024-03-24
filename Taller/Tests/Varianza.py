import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from scipy.stats import chi2
import numpy as np

class VarianzaApp(tk.Frame):
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

        self.ruta_entry = tk.Entry(self.buscar_frame, width=50)
        self.ruta_entry.pack(side="left", padx=5)

        self.button = tk.Button(self.buscar_frame, text="Buscar Archivo", command=self.buscar_archivo)
        self.button.pack(side="left", padx=5)

        self.calcular_frame = tk.Frame(self.master)
        self.calcular_frame.pack(pady=5)

        self.calcular_button = tk.Button(self.calcular_frame, text="Calcular", command=self.calcular_resultados)
        self.calcular_button.pack(side="left", padx=5)

        self.table_frame = tk.Frame(self.master)
        self.table_frame.pack(pady=20)

        self.table = ttk.Treeview(self.table_frame, columns=("Valor", "Calculado"), show="headings", height=15)
        self.table.heading("Valor", text="Valor", anchor=tk.CENTER)
        self.table.heading("Calculado", text="Calculado", anchor=tk.CENTER)
        self.table.column("Valor", width=250, anchor=tk.CENTER)
        self.table.column("Calculado", width=250, anchor=tk.CENTER)
        self.table.pack(side="left", padx=10)

        self.scrollbar = ttk.Scrollbar(self.table_frame, orient="vertical", command=self.table.yview)
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
        varianza = np.var(datos, ddof=1)
        chi2_value = chi2.ppf(alpha / 2, n - 1)
        chi2_alpha = chi2.ppf(resta, n - 1)
        lsv = chi2_value / (12 * (n - 1))
        liv = chi2_alpha / (12 * (n - 1))
        resultado = (varianza >= lsv) and (varianza <= liv)
        
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
        for clave, valor in resultados.items():
            self.table.insert("", "end", values=(clave, valor))

if __name__ == "__main__":
    root = tk.Tk()
    app = VarianzaApp(master=root)
    app.pack()
    app.mainloop()
