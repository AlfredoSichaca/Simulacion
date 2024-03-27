import tkinter as tk
from tkinter import filedialog, ttk, messagebox
import pandas as pd
from scipy.stats import chi2

class PruebaPoker(tk.Frame):
    def __init__(self, master=None,archivo_path=None):
        super().__init__(master)
        self.master = master
        self.archivo_path = archivo_path  # Almacenar la ruta del archivo aquí
        self.create_widgets()

    def create_widgets(self):
        # Crear un marco para contener los widgets
        self.frame = tk.Frame(self.master)
        self.frame.pack(padx=10, pady=10)
    
        # Etiqueta del título de la prueba
        self.tittle_label = ttk.Label(self.frame, text="Prueba de Póker", font=("Helvetica", 14, "bold"))
        self.tittle_label.grid(row=0, column=0, columnspan=3, pady=5)

        # Botón para calcular el resultado de la prueba
        self.calcular_button = tk.Button(self.frame, text="Calcular", command=self.calcular_resultado)
        self.calcular_button.grid(row=1, column=0, columnspan=3, pady=5)

        # Tabla para mostrar los resultados de la prueba
        self.tree = ttk.Treeview(self.frame)
        self.tree["columns"] = ("Categoria", "Cantidad", "Probabilidad", "Ei", "(Ei - Oi)^2 / Ei")
        self.tree.heading("#0", text="", anchor=tk.W)
        self.tree.heading("Categoria", text="Categoría", anchor=tk.W)
        self.tree.heading("Cantidad", text="Cantidad", anchor=tk.W)
        self.tree.heading("Probabilidad", text="Probabilidad", anchor=tk.W)
        self.tree.heading("Ei", text="Ei", anchor=tk.W)
        self.tree.heading("(Ei - Oi)^2 / Ei", text="(Ei - Oi)^2 / Ei", anchor=tk.W)
        self.tree.grid(row=2, column=0, columnspan=3, padx=5, pady=5, sticky="nsew")

        # Etiqueta para mostrar la suma de los valores calculados
        self.suma_label = tk.Label(self.frame, text="")
        self.suma_label.grid(row=3, column=0, columnspan=3)

        # Etiqueta para mostrar el valor de Chi-cuadrado calculado
        self.chi_cuadrado_label = tk.Label(self.frame, text="")
        self.chi_cuadrado_label.grid(row=4, column=0, columnspan=3)

        # Etiqueta para mostrar el resultado de la prueba
        self.resultado_label = tk.Label(self.frame, text="")
        self.resultado_label.grid(row=5, column=0, columnspan=3)


    def calcular_resultado(self):
        # Verificar si se ha seleccionado un archivo
        ruta_archivo = self.archivo_path
        if ruta_archivo:
            try:
                # Leer los números del archivo CSV
                numeros = self.leer_csv(ruta_archivo)
                if numeros:

                    # Definir las probabilidades teóricas de cada categoría
                    probabilidades = [0.3024, 0.5040, 0.1080, 0.0720, 0.0090, 0.0045, 0.0001]

                    # Contar la cantidad de ocurrencias de cada categoría en los números
                    resultado = self.contar_cantidad_categorias(numeros)

                    # Crear un DataFrame para mostrar los resultados
                    df_resultado = pd.DataFrame.from_dict(resultado, orient='index', columns=['cantidad'])
                    categorias_ordenadas = ["aleatorio", "par", "dos_pares", "tercia", "tercia_y_par", "poker", "quintilla"]
                    df_resultado = df_resultado.reindex(categorias_ordenadas)

                    # Calcular valores teóricos y Chi-cuadrado
                    df_resultado['probabilidad'] = probabilidades
                    df_resultado['Ei'] = df_resultado['probabilidad'] * len(numeros)
                    df_resultado['(Ei - Oi)^2 / Ei'] = (df_resultado['Ei'] - df_resultado['cantidad'])**2 / df_resultado['Ei']

                    suma = sum(df_resultado['(Ei - Oi)^2 / Ei'])

                    nivel_de_significancia = 0.05
                    grados_de_libertad = 6
                    inverso_chi_cuadrado = chi2.ppf(1 - nivel_de_significancia, grados_de_libertad)

                    # Evaluar el resultado de la prueba
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
        # Inicializar un diccionario para almacenar la cantidad de ocurrencias de cada categoría
        categorias = {
            "aleatorio": 0,
            "par": 0,
            "dos_pares": 0,
            "tercia": 0,
            "tercia_y_par": 0,
            "poker": 0,
            "quintilla": 0
        }

        # Iterar sobre cada número y determinar su categoría
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
            # Leer los números del archivo CSV y convertirlos a una lista de números flotantes
            with open(ruta, 'r') as file:
                numeros = []
                for line in file:
                    numeros.extend([float(num) for num in line.strip().split(',')])
            return numeros
        except Exception as e:

            # Manejar cualquier error que ocurra durante la lectura del archivo CSV
            print("Error al leer el archivo CSV:", e)
            return []

