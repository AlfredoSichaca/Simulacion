import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import pandas as pd

class LinealApp(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.create_widgets()


    #Valida los campos de entrada para garantizar que sean valores numéricos válidos y positivos.
    def validar_campos(self):
        try:
        # Obtener los valores de los campos de entrada
            x0 = int(self.semilla_entry.get())
            k = int(self.k_entry.get())
            c = int(self.c_entry.get())
            g = int(self.g_entry.get())
            min_value = int(self.minimo_entry.get())
            max_value = int(self.maximo_entry.get())
            iteraciones = int(self.iteraciones_entry.get())

            # Validar que los valores sean positivos y no iguales a cero
            if x0 <= 0 or k <= 0 or c <= 0 or g <= 0 or min_value < 0 or max_value < 0 or iteraciones <= 0:
                raise ValueError("Los campos no pueden ser negativos o 0")
            
            # Validar que el valor máximo sea mayor que el valor mínimo        
            if max_value <= min_value:
                raise ValueError("El valor máximo debe ser mayor que el valor mínimo")
            
            return True
        
        except ValueError as e:
        # Mostrar mensaje de error si ocurre una excepción ValueError
            messagebox.showwarning("Error", str(e))
            return False

    def generar_numeros_aleatorios(self):
        # Verificar si los campos de entrada son válidos
        if self.validar_campos():

            # Obtener los valores de los campos de entrada
            x0 = int(self.semilla_entry.get())
            k = int(self.k_entry.get())
            c = int(self.c_entry.get())
            g = int(self.g_entry.get())
            min_value = int(self.minimo_entry.get())
            max_value = int(self.maximo_entry.get())

            # Calcular valores adicionales para el generador
            a = 1 + 2 * k
            m = 2 ** g
            semilla = x0

            # Generar números pseudoaleatorios utilizando el método congruencial lineal
            xn_valores = []
            for _ in range(int(self.iteraciones_entry.get())):
                semilla = (a * semilla + c) % m
                xn_valores.append(semilla)

            # Crear un DataFrame para almacenar los números generados 
            df = pd.DataFrame({"Xi": xn_valores})
            df["R1"] = df["Xi"] / (m - 1)
            df['Ni1'] = min_value + (max_value - min_value) * df['R1']
            df["Ri2"] = df["Xi"] / m
            df['Ni2'] = min_value + (max_value - min_value) * df['Ri2']

            # Limpiar Treeview antes de insertar nuevos datos
            for row in self.tree.get_children():
                self.tree.delete(row)
            # Insertar datos en el Treeview para visualización
            for i, row in df.iterrows():
                self.tree.insert("", "end", values=(row['Xi'], row['R1'], row['Ni1'], row['Ri2'], row['Ni2']))

            return df  # Devuelve el DataFrame con los números generados

    def guardar_csv(self):
        df = self.generar_numeros_aleatorios()
        if df is not None:

            # Solicitar al usuario la ubicación para guardar el archivo CSV
            file_path = filedialog.asksaveasfilename(defaultextension=".csv")
        if file_path:

            # Redondear los valores de la columna 'R1' a 5 decimales
            df['R1'] = df['R1'].apply(lambda x: round(x, 5))  

            # Escribir los valores de la columna 'Ri2' en el archivo CSV
            with open(file_path, 'w') as f:
                f.write(','.join(map(str, df['Ri2'])))

            # Mostrar mensaje de éxito
            messagebox.showinfo("Guardado exitoso", "Los números Ri se han guardado correctamente en el archivo CSV.")
            # Limpiar campos de entrada
            self.semilla_entry.delete(0, tk.END)
            self.iteraciones_entry.delete(0, tk.END)
            self.minimo_entry.delete(0, tk.END)
            self.maximo_entry.delete(0, tk.END)
            self.g_entry.delete(0, tk.END)
            self.c_entry.delete(0, tk.END)
            self.k_entry.delete(0, tk.END)
            # Limpiar Treeview
            for row in self.tree.get_children():
                self.tree.delete(row)


    def create_widgets(self):
        
        # Etiquetas y campos de entrada para los parámetros del generador
        ttk.Label(self, text="Semilla (x0):").grid(row=0, column=0, padx=5, pady=5)
        self.semilla_entry = ttk.Entry(self)
        self.semilla_entry.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(self, text="k:").grid(row=1, column=0, padx=5, pady=5)
        self.k_entry = ttk.Entry(self)
        self.k_entry.grid(row=1, column=1, padx=5, pady=5)

        ttk.Label(self, text="c:").grid(row=2, column=0, padx=5, pady=5)
        self.c_entry = ttk.Entry(self)
        self.c_entry.grid(row=2, column=1, padx=5, pady=5)

        ttk.Label(self, text="g:").grid(row=3, column=0, padx=5, pady=5)
        self.g_entry = ttk.Entry(self)
        self.g_entry.grid(row=3, column=1, padx=5, pady=5)

        # Etiquetas y campos de entrada para los valores mínimo y máximo y el número de iteraciones

        ttk.Label(self, text="Mínimo:").grid(row=4, column=0, padx=5, pady=5)
        self.minimo_entry = ttk.Entry(self)
        self.minimo_entry.grid(row=4, column=1, padx=5, pady=5)

        ttk.Label(self, text="Máximo:").grid(row=5, column=0, padx=5, pady=5)
        self.maximo_entry = ttk.Entry(self)
        self.maximo_entry.grid(row=5, column=1, padx=5, pady=5)

        ttk.Label(self, text="Iteraciones:").grid(row=6, column=0, padx=5, pady=5)
        self.iteraciones_entry = ttk.Entry(self)
        self.iteraciones_entry.grid(row=6, column=1, padx=5, pady=5)

        # Botones para generar números aleatorios y guardar en CSV
        generar_btn = ttk.Button(self, text="Generar", command=self.generar_numeros_aleatorios)
        generar_btn.grid(row=7, column=0, columnspan=2, padx=5, pady=5)

        guardar_btn = ttk.Button(self, text="Guardar CSV", command=self.guardar_csv)
        guardar_btn.grid(row=8, column=0, columnspan=2, padx=5, pady=5)

        # Treeview para mostrar los números generados y transformados
        self.tree = ttk.Treeview(self, columns=("Xi", "R1", "Ni1", "Ri2", "Ni2"), show="headings")
        self.tree.heading("Xi", text="Xi")
        self.tree.heading("R1", text="R1")
        self.tree.heading("Ni1", text="Ni1")
        self.tree.heading("Ri2", text="Ri2")
        self.tree.heading("Ni2", text="Ni2")
        self.tree.grid(row=9, column=0, columnspan=2, padx=5, pady=5)

