import tkinter as tk
from tkinter import ttk
import pandas as pd
from tkinter import messagebox
from tkinter import filedialog

class MultiplicativaApp(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.semilla_entry = None
        self.t_entry = None
        self.g_entry = None
        self.minimo_entry = None
        self.maximo_entry = None
        self.iteraciones_entry = None
        self.tree = None
        self.create_widgets()

    def validar_campos(self):
        try:
            #obtener los valores para la validacion 
            semilla = int(self.semilla_entry.get())
            t = int(self.t_entry.get())
            g = int(self.g_entry.get())
            min_value = int(self.minimo_entry.get())
            max_value = int(self.maximo_entry.get())
            iteraciones = int(self.iteraciones_entry.get())

            if semilla < 0 or t < 0 or g < 0 or min_value < 0 or max_value < 0 or iteraciones < 0:
                raise ValueError("Los campos no pueden ser negativos")
            
            if max_value <= min_value:
                raise ValueError("El valor máximo debe ser mayor que el valor mínimo")
            
            return True
        
        except ValueError as e:
            messagebox.showwarning("Error", str(e))
            return False

    def generar_numeros_aleatorios(self):
        if self.validar_campos():
            semilla = int(self.semilla_entry.get()) # Obtener la semilla
            t = int(self.t_entry.get()) # Obtener el valor t
            g = int(self.g_entry.get()) # Obtener el valor g
            min_value = int(self.minimo_entry.get()) # Obtener el valor mínimo
            max_value = int(self.maximo_entry.get())  # Obtener el valor máximo
            a = 8 * t + 5  # Calcular el valor 'a'
            a = 8 * t + 5 # Calcular el valor 'a'
            m = 2 ** g # Calcular el valor 'm'

            # Instanciar el generador congruencial multiplicativo
            generador = self.CongruencialM(a, m, semilla)

            # Generar números pseudoaleatorios
            xn_valores = [generador.generar_numero() for _ in range(int(self.iteraciones_entry.get()))]

            # Crear un DataFrame para almacenar los resultados
            df = pd.DataFrame({"Xi": xn_valores})
            df["R1"] = (df["Xi"] / (m - 1))
            df['Ni1'] = min_value + (max_value - min_value) * df['R1']
            df["Ri2"] = df["Xi"] / m
            df['Ni2'] = min_value + (max_value - min_value) * df['Ri2']

             # Insertar los resultados en el Treeview
            for i, row in df.iterrows():
                self.tree.insert("", "end", values=(row['Xi'], row['R1'], row['Ni1'], row['Ri2'], row['Ni2']))

            return df

    class CongruencialM:
        def __init__(self, a, m, semilla):
            self.a = a
            self.m = m
            self.xn = semilla

        def generar_numero(self):
            self.xn = (self.a * self.xn) % self.m # Generar el siguiente número pseudoaleatorio
            return self.xn

    def guardar_csv(self):
        df = self.generar_numeros_aleatorios()
        if df is not None:
            file_path = filedialog.asksaveasfilename(defaultextension=".csv")# Obtener la ruta de archivo para guardar
            if file_path:
                df['R1'] = df['R1'].apply(lambda x: round(x, 5))  # Truncar a 5 decimales
                df['R1'].to_csv(file_path, index=False, header=False) # Guardar en archivo CSV
                messagebox.showinfo("Guardado exitoso", "Los números Ri se han guardado correctamente en el archivo CSV.")
                # Limpiar campos de entrada
                self.semilla_entry.delete(0, tk.END)
                self.iteraciones_entry.delete(0, tk.END)
                self.minimo_entry.delete(0, tk.END)
                self.maximo_entry.delete(0, tk.END)
                self.g_entry.delete(0, tk.END)
                self.t_entry.delete(0, tk.END)
                    # Limpiar Treeview
                for row in self.tree.get_children():
                    self.tree.delete(row)

    def create_widgets(self):

        # Etiquetas y entradas para los parámetros
        ttk.Label(self, text="Semilla (x0):").grid(row=0, column=0, padx=5, pady=5)
        self.semilla_entry = ttk.Entry(self)
        self.semilla_entry.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(self, text="Valor t:").grid(row=1, column=0, padx=5, pady=5)
        self.t_entry = ttk.Entry(self)
        self.t_entry.grid(row=1, column=1, padx=5, pady=5)

        ttk.Label(self, text="Valor g:").grid(row=2, column=0, padx=5, pady=5)
        self.g_entry = ttk.Entry(self)
        self.g_entry.grid(row=2, column=1, padx=5, pady=5)

        ttk.Label(self, text="Mínimo:").grid(row=3, column=0, padx=5, pady=5)
        self.minimo_entry = ttk.Entry(self)
        self.minimo_entry.grid(row=3, column=1, padx=5, pady=5)

        ttk.Label(self, text="Máximo:").grid(row=4, column=0, padx=5, pady=5)
        self.maximo_entry = ttk.Entry(self)
        self.maximo_entry.grid(row=4, column=1, padx=5, pady=5)

        ttk.Label(self, text="Iteraciones:").grid(row=5, column=0, padx=5, pady=5)
        self.iteraciones_entry = ttk.Entry(self)
        self.iteraciones_entry.grid(row=5, column=1, padx=5, pady=5)

        # Botones para generar números y guardar en CSV
        generar_btn = ttk.Button(self, text="Generar", command=self.generar_numeros_aleatorios)
        generar_btn.grid(row=6, column=0, columnspan=2, padx=5, pady=5)

        guardar_btn = ttk.Button(self, text="Guardar CSV", command=self.guardar_csv)
        guardar_btn.grid(row=7, column=0, columnspan=2, padx=5, pady=5)

        # Treeview para mostrar los resultados
        self.tree = ttk.Treeview(self, columns=("Xi", "R1", "Ni1", "Ri2", "Ni2"), show="headings")
        self.tree.heading("Xi", text="Xi")
        self.tree.heading("R1", text="R1")
        self.tree.heading("Ni1", text="Ni1")
        self.tree.heading("Ri2", text="Ri2")
        self.tree.heading("Ni2", text="Ni2")
        self.tree.grid(row=8, column=0, columnspan=2, padx=5, pady=5)

