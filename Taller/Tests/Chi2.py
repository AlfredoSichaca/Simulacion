import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import pandas as pd
import numpy as np
from scipy.stats import chi2

class ChiSquareAnalysisApp(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        
        # Variables globales
        self.datos = None
        
        # Crear widgets
        self.create_widgets()
        
    def create_widgets(self):
        # Widget para cargar archivo
        self.ruta_textbox = tk.Text(self, height=1, width=40)
        self.ruta_textbox.grid(row=0, column=0, padx=10, pady=10, sticky="we")
        
        self.boton_cargar = tk.Button(self, text="Cargar CSV", command=self.cargar_archivo)
        self.boton_cargar.grid(row=0, column=1, padx=10, pady=10)
        
        # Widgets para ingresar valores y realizar análisis
        etiqueta_a = tk.Label(self, text="Valor A:")
        etiqueta_a.grid(row=1, column=0, padx=10, pady=10)
        self.entrada_a = tk.Entry(self)
        self.entrada_a.grid(row=1, column=1, padx=10, pady=10)

        etiqueta_b = tk.Label(self, text="Valor B:")
        etiqueta_b.grid(row=2, column=0, padx=10, pady=10)
        self.entrada_b = tk.Entry(self)
        self.entrada_b.grid(row=2, column=1, padx=10, pady=10)

        etiqueta_intervalo = tk.Label(self, text="Número de intervalos:")
        etiqueta_intervalo.grid(row=3, column=0, padx=10, pady=10)
        self.entrada_intervalo = tk.Entry(self)
        self.entrada_intervalo.grid(row=3, column=1, padx=10, pady=10)

        self.boton_analizar = tk.Button(self, text="Realizar Análisis", command=self.analizar)
        self.boton_analizar.grid(row=4, column=0, columnspan=2, padx=10, pady=10)

        # Widget para mostrar resultados
        self.tabla = ttk.Treeview(self)
        self.tabla['columns'] = ('Intervalo', 'Frecuencia', 'Frecuencia Esperada', 'Chi^2')
        self.tabla.heading("#0", text="", anchor='w')
        self.tabla.column("#0", anchor='w', width=0)
        self.tabla.heading("Intervalo", text="Intervalo")
        self.tabla.column("Intervalo", anchor="center", width=200)
        self.tabla.heading("Frecuencia", text="Frecuencia")
        self.tabla.column("Frecuencia", anchor="center", width=100)
        self.tabla.heading("Frecuencia Esperada", text="Frecuencia Esperada")
        self.tabla.column("Frecuencia Esperada", anchor="center", width=150)
        self.tabla.heading("Chi^2", text="Chi^2")
        self.tabla.column("Chi^2", anchor="center", width=100)
        self.tabla.grid(row=5, column=0, columnspan=2, padx=10, pady=10, sticky="nsew")

        scrollbar = ttk.Scrollbar(self, orient="vertical", command=self.tabla.yview)
        scrollbar.grid(row=5, column=2, sticky='ns')
        self.tabla.configure(yscrollcommand=scrollbar.set)

        self.resultados_label = tk.Label(self, text="", justify="left")
        self.resultados_label.grid(row=6, column=0, columnspan=2, padx=10, pady=10, sticky="w")

    def cargar_archivo(self):
        try:
            filename = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
            self.datos = pd.read_csv(filename, header=None).values.flatten().tolist()
            self.ruta_textbox.delete(1.0, tk.END)
            self.ruta_textbox.insert(tk.END, filename)
            messagebox.showinfo("Archivo cargado", "Archivo CSV cargado exitosamente.")
        except FileNotFoundError:
            messagebox.showerror("Error", "¡El archivo no existe!")

    def analizar(self):
        if self.datos is None:
            messagebox.showerror("Error", "¡Por favor, carga un archivo antes de realizar el análisis!")
            return

        try:
            a = float(self.entrada_a.get())
            b = float(self.entrada_b.get())
            interval = int(self.entrada_intervalo.get())
            df_resultado, suma, valor_critico, resultado = self.procesar_datos(a, b, interval)

            self.update_results(df_resultado, suma, valor_critico, resultado)

        except ValueError:
            messagebox.showerror("Error", "¡Por favor, introduce valores numéricos válidos!")

    def procesar_datos(self, a, b, interval):
        df = pd.DataFrame({'Ri': self.datos})
        df['Ni'] = a + (b - a) * df['Ri']

        min_valor = df['Ni'].min()
        max_valor = df['Ni'].max()

        intervalos = np.linspace(min_valor, max_valor, num=interval + 1)
        frecuencias, bordes_intervalos = np.histogram(df['Ni'], bins=intervalos)

        n = len(intervalos) - 1
        N = len(df['Ni'])
        frecuencia_esperada = N / n
        chi_2 = (((frecuencias - frecuencia_esperada) ** 2) / frecuencia_esperada)

        datos = {
            'Intervalo': [f"{bordes_intervalos[i]:.5f} - {bordes_intervalos[i + 1]:.5f}" for i in range(len(frecuencias))],
            'Frecuencia': frecuencias,
            'Frecuencia Esperada': [frecuencia_esperada] * len(frecuencias),
            'Chi^2': chi_2
        }

        df_resultado = pd.DataFrame(datos)
        suma = sum(chi_2)

        alpha = 0.05
        grados_libertad = interval - 1
        valor_critico = chi2.ppf(1 - alpha, grados_libertad)
        resultado = (suma < valor_critico)

        return df_resultado, suma, valor_critico, resultado

    def update_results(self, df_resultado, suma, valor_critico, resultado):
        self.resultados_label.config(text=f"Suma de Chi^2: {round(suma, 2)}\nValor crítico: {valor_critico}\n¿Se Aprueba?: {resultado}")

        for row in self.tabla.get_children():
            self.tabla.delete(row)

        for index, row in df_resultado.iterrows():
            self.tabla.insert("", "end", values=(row['Intervalo'], row['Frecuencia'], row['Frecuencia Esperada'], row['Chi^2']))

    

if __name__ == "__main__":
    root = tk.Tk()
    app = ChiSquareAnalysisApp(root)
    app.pack()
    root.mainloop()