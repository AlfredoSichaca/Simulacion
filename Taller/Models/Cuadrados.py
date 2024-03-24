import tkinter as tk
from tkinter import ttk, filedialog
import pandas as pd
from tkinter import messagebox

class CuadradosApp(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.create_widgets()

    def cuadrados_medios(self, semilla, iteraciones):
        resultados = []
        longitud_semilla = len(str(semilla))

        for _ in range(iteraciones):
            cuadrado = semilla ** 2
            cadena_cuadrado = str(cuadrado).zfill(2 * longitud_semilla)
            centro = cadena_cuadrado[(len(cadena_cuadrado) - longitud_semilla)//2 : (len(cadena_cuadrado) + longitud_semilla)//2]
            nuevo_numero = int(centro)
            numero_normalizado = nuevo_numero / (10 ** longitud_semilla)
            resultados.append(numero_normalizado)
            semilla = nuevo_numero

        return resultados

    def validar_campos(self):
        try:
            semilla_inicial = int(self.semilla_entry.get())
            iteraciones = int(self.iteraciones_entry.get())
            min_value = int(self.minimo_entry.get())
            max_value = int(self.maximo_entry.get())

            if len(str(semilla_inicial)) != 4:
                raise ValueError("La longitud de la semilla debe ser igual a 4")

            if semilla_inicial <= 0 or iteraciones <=0 or min_value < 0 or max_value < 0:
                raise ValueError("Los campos no pueden ser negativos")

            if max_value <= min_value:
                raise ValueError("El valor máximo debe ser mayor que el valor mínimo")
            
            return True

        except ValueError as e:
            messagebox.showwarning("Error", str(e))
            return False

    def generar_numeros_aleatorios(self):
        if self.validar_campos():
            semilla_inicial = int(self.semilla_entry.get())
            iteraciones = int(self.iteraciones_entry.get())
            min_value = int(self.minimo_entry.get())
            max_value = int(self.maximo_entry.get())

            resultados = self.cuadrados_medios(semilla_inicial, iteraciones)

            df = pd.DataFrame({"Ri": resultados})
            df['Ni'] = min_value + (max_value - min_value) * df['Ri']
            df["Xi"] = (df["Ri"] * 10000)

            for row in self.tree.get_children():
                self.tree.delete(row)

            for i, row in df.iterrows():
                self.tree.insert("", "end", values=(row['Ri'], row['Ni'], row['Xi']))

            return df

    def guardar_csv(self):
        df = self.generar_numeros_aleatorios()
        if df is not None:
            file_path = filedialog.asksaveasfilename(defaultextension=".csv")
        if file_path:
            with open(file_path, 'w') as f:
                f.write(','.join(map(str, df['Ri'].apply(lambda x: round(x, 5)))))
            messagebox.showinfo("Guardado exitoso", "Los números Ri se han guardado correctamente en el archivo CSV.")
            # Limpiar campos de entrada
            self.semilla_entry.delete(0, tk.END)
            self.iteraciones_entry.delete(0, tk.END)
            self.minimo_entry.delete(0, tk.END)
            self.maximo_entry.delete(0, tk.END)
            # Limpiar Treeview
            for row in self.tree.get_children():
                self.tree.delete(row)

    def create_widgets(self):
        ttk.Label(self, text="Semilla inicial (4 dígitos):").grid(row=0, column=0, padx=5, pady=5)
        self.semilla_entry = ttk.Entry(self)
        self.semilla_entry.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(self, text="Iteraciones:").grid(row=1, column=0, padx=5, pady=5)
        self.iteraciones_entry = ttk.Entry(self)
        self.iteraciones_entry.grid(row=1, column=1, padx=5, pady=5)

        ttk.Label(self, text="Mínimo:").grid(row=2, column=0, padx=5, pady=5)
        self.minimo_entry = ttk.Entry(self)
        self.minimo_entry.grid(row=2, column=1, padx=5, pady=5)

        ttk.Label(self, text="Máximo:").grid(row=3, column=0, padx=5, pady=5)
        self.maximo_entry = ttk.Entry(self)
        self.maximo_entry.grid(row=3, column=1, padx=5, pady=5)

        generar_btn = ttk.Button(self, text="Generar", command=self.generar_numeros_aleatorios)
        generar_btn.grid(row=4, column=0, columnspan=2, padx=5, pady=5)

        guardar_btn = ttk.Button(self, text="Guardar CSV", command=self.guardar_csv)
        guardar_btn.grid(row=5, column=0, columnspan=2, padx=5, pady=5)

        self.tree = ttk.Treeview(self, columns=("Ri", "Ni", "Xi"), show="headings")
        self.tree.heading("Ri", text="Ri")
        self.tree.heading("Ni", text="Ni")
        self.tree.heading("Xi", text="Xi")
        self.tree.grid(row=6, column=0, columnspan=2, padx=5, pady=5)

if __name__ == "__main__":
    root = tk.Tk()
    app = CuadradosApp(root)
    app.pack()
    root.mainloop()
