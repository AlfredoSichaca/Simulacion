import tkinter as tk
from tkinter import filedialog, ttk, messagebox
import pandas as pd
from scipy.stats import chi2

class PruebaPoker(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.create_widgets()

    def create_widgets(self):
        self.frame = tk.Frame(self.master)
        self.frame.pack(padx=10, pady=10)

        self.ruta_label = tk.Label(self.frame, text="Ruta del archivo:")
        self.ruta_label.grid(row=0, column=0, sticky="w")

        self.ruta_textbox = tk.Entry(self.frame, width=40)
        self.ruta_textbox.grid(row=0, column=1, padx=5, pady=5)

        self.buscar_button = tk.Button(self.frame, text="Buscar archivo", command=self.buscar_archivo)
        self.buscar_button.grid(row=0, column=2, padx=5, pady=5)

        self.calcular_button = tk.Button(self.frame, text="Calcular", command=self.calcular_resultado)
        self.calcular_button.grid(row=1, column=0, columnspan=3, pady=5)

        self.tree = ttk.Treeview(self.frame)
        self.tree["columns"] = ("Categoria", "Cantidad", "Probabilidad", "Ei", "(Ei - Oi)^2 / Ei")
        self.tree.heading("#0", text="", anchor=tk.W)
        self.tree.heading("Categoria", text="Categoría", anchor=tk.W)
        self.tree.heading("Cantidad", text="Cantidad", anchor=tk.W)
        self.tree.heading("Probabilidad", text="Probabilidad", anchor=tk.W)
        self.tree.heading("Ei", text="Ei", anchor=tk.W)
        self.tree.heading("(Ei - Oi)^2 / Ei", text="(Ei - Oi)^2 / Ei", anchor=tk.W)
        self.tree.grid(row=2, column=0, columnspan=3, padx=5, pady=5, sticky="nsew")

        self.suma_label = tk.Label(self.frame, text="")
        self.suma_label.grid(row=3, column=0, columnspan=3)

        self.chi_cuadrado_label = tk.Label(self.frame, text="")
        self.chi_cuadrado_label.grid(row=4, column=0, columnspan=3)

        self.resultado_label = tk.Label(self.frame, text="")
        self.resultado_label.grid(row=5, column=0, columnspan=3)

    def buscar_archivo(self):
        ruta_archivo = filedialog.askopenfilename(filetypes=[("Archivos CSV", "*.csv")])
        if ruta_archivo:
            self.ruta_textbox.delete(0, tk.END)
            self.ruta_textbox.insert(0, ruta_archivo)

    def calcular_resultado(self):
        ruta_archivo = self.ruta_textbox.get()
        if ruta_archivo:
            try:
                numeros = self.leer_csv(ruta_archivo)
                if numeros:
                    probabilidades = [0.3024, 0.5040, 0.1080, 0.0720, 0.0090, 0.0045, 0.0001]
                    resultado = self.contar_cantidad_categorias(numeros)

                    df_resultado = pd.DataFrame.from_dict(resultado, orient='index', columns=['cantidad'])
                    categorias_ordenadas = ["aleatorio", "par", "dos_pares", "tercia", "tercia_y_par", "poker", "quintilla"]
                    df_resultado = df_resultado.reindex(categorias_ordenadas)

                    df_resultado['probabilidad'] = probabilidades
                    df_resultado['Ei'] = df_resultado['probabilidad'] * len(numeros)
                    df_resultado['(Ei - Oi)^2 / Ei'] = (df_resultado['Ei'] - df_resultado['cantidad'])**2 / df_resultado['Ei']

                    suma = sum(df_resultado['(Ei - Oi)^2 / Ei'])

                    nivel_de_significancia = 0.05
                    grados_de_libertad = 6
                    inverso_chi_cuadrado = chi2.ppf(1 - nivel_de_significancia, grados_de_libertad)

                    resultado_prueba = suma < inverso_chi_cuadrado

                    # Mostrar resultado en la tabla
                    self.tree.delete(*self.tree.get_children())
                    for index, row in df_resultado.iterrows():
                        self.tree.insert("", tk.END, values=(index, row['cantidad'], row['probabilidad'], row['Ei'], row['(Ei - Oi)^2 / Ei']))

                    self.suma_label.config(text=f"Suma de (Ei - Oi)^2 / Ei: {suma}")
                    self.chi_cuadrado_label.config(text=f"Valor de Chi^2: {inverso_chi_cuadrado}")
                    self.resultado_label.config(text=f"RESULTADO: {'Aprobada' if resultado_prueba else 'No Aprobada'}")
                else:
                    self.resultado_label.config(text="Error al leer el archivo CSV.")
            except Exception as e:
                messagebox.showerror("Error", f"No se pudo procesar el archivo: {e}")
        else:
            messagebox.showerror("Error", "Por favor, seleccione un archivo antes de calcular los resultados.")

    def contar_cantidad_categorias(self, numeros):
        categorias = {
            "aleatorio": 0,
            "par": 0,
            "dos_pares": 0,
            "tercia": 0,
            "tercia_y_par": 0,
            "poker": 0,
            "quintilla": 0
        }

        for numero in numeros:
            digitos = [int(d) for d in str(format(numero, '.5f')[1:]).replace('.', '')]
            conteo_digitos = {i: digitos.count(i) for i in digitos}

            if 5 in conteo_digitos.values():
                categorias["quintilla"] += 1
            elif 4 in conteo_digitos.values():
                categorias["poker"] += 1
            elif 3 in conteo_digitos.values():
                if 2 in conteo_digitos.values():
                    categorias["tercia_y_par"] += 1
                else:
                    categorias["tercia"] += 1
            elif 2 in conteo_digitos.values():
                if list(conteo_digitos.values()).count(2) == 2:
                    categorias["dos_pares"] += 1
                else:
                    categorias["par"] += 1
            else:
                categorias["aleatorio"] += 1

        return categorias

    def leer_csv(self, ruta):
        try:
            with open(ruta, 'r') as file:
                numeros = []
                for line in file:
                    numeros.extend([float(num) for num in line.strip().split(',')])
            return numeros
        except Exception as e:
            print("Error al leer el archivo CSV:", e)
            return []

if __name__ == "__main__":
    root = tk.Tk()
    app = PruebaPoker(master=root)
    app.pack()
    app.mainloop()