import tkinter as tk
from tkinter import ttk
from Cuadrados import CuadradosApp
from Lineal import LinealApp
from Multiplicativa import MultiplicativaApp
from Uniforme import VentanaPrincipal
from Normal import VentanaPrincipalN

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Menú Principal")
        self.attributes('-fullscreen', True) # Configuración para pantalla completa
        style = ttk.Style()

        # Estilo para los botones
        style.configure('EstiloBoton.TButton', foreground='black', background='lightgreen', font=('Arial', 10), padding=5)
       
        # Panel superior con botones
        self.panel_superior = ttk.Frame(self, style='PanelSuperior.TFrame')
        self.panel_superior.place(relx=0.5, rely=0.05, anchor="center") 

        # Botones para diferentes opciones
        self.boton_cuadrados_medios = ttk.Button(self.panel_superior, text="Cuadrados Medios", command=self.mostrar_interfaz_cuadrados_medios, style='EstiloBoton.TButton')
        self.boton_cuadrados_medios.pack(side="left", padx=(5, 10))

        self.boton_lineal = ttk.Button(self.panel_superior, text="Congruencial Lineal", command=self.mostrar_interfaz_congruencial_Lineal, style='EstiloBoton.TButton')
        self.boton_lineal.pack(side="left", padx=5)

        self.boton_multiplicativa = ttk.Button(self.panel_superior, text="Congruencial Multiplicativa", command=self.mostrar_interfaz_congruencial_m, style='EstiloBoton.TButton')
        self.boton_multiplicativa.pack(side="left", padx=5)

        self.boton_uniforme = ttk.Button(self.panel_superior, text="Uniforme", command=self.mostrar_interfaz_uniforme, style='EstiloBoton.TButton')
        self.boton_uniforme.pack(side="left", padx=5)

        self.boton_normal = ttk.Button(self.panel_superior, text="Normal", command=self.mostrar_interfaz_normal, style='EstiloBoton.TButton')
        self.boton_normal.pack(side="left", padx=5)

        self.boton_salir = ttk.Button(self.panel_superior, text="Salir", command=self.quit, style='BotonAccion.TButton')
        self.boton_salir.pack(side="left", padx=5)

        # Separador horizontal
        ttk.Separator(self, orient='horizontal', style='Separador.TSeparator').place(relx=0.5, rely=0.1, anchor="center", relwidth=0.9)

        # Panel inferior donde se mostrará la interfaz seleccionada
        self.panel_inferior = ttk.Frame(self, style='PanelInferior.TFrame')
        self.panel_inferior.place(relx=0.5, rely=0.5, anchor="center")  
        
    # Funciones para mostrar las diferentes interfaces
    def mostrar_interfaz_cuadrados_medios(self):
        self.deseleccionar_botones()
        self.boton_cuadrados_medios.state(['pressed'])  
        if hasattr(self, "interfaz_actual"):
            self.interfaz_actual.destroy()
        self.interfaz_actual = CuadradosApp(self.panel_inferior)
        self.interfaz_actual.pack(fill="both", expand=True)

    def mostrar_interfaz_congruencial_Lineal(self):
        self.deseleccionar_botones()
        self.boton_lineal.state(['pressed'])  
        if hasattr(self, "interfaz_actual"):
            self.interfaz_actual.destroy()
        self.interfaz_actual = LinealApp(self.panel_inferior)
        self.interfaz_actual.pack(fill="both", expand=True)
    
    def mostrar_interfaz_congruencial_m(self):
        self.deseleccionar_botones()
        self.boton_multiplicativa.state(['pressed'])  
        if hasattr(self, "interfaz_actual"):
            self.interfaz_actual.destroy()
        self.interfaz_actual = MultiplicativaApp(self.panel_inferior)
        self.interfaz_actual.pack(fill="both", expand=True)
    
    def mostrar_interfaz_uniforme(self):
        self.deseleccionar_botones()
        self.boton_uniforme.state(['pressed']) 
        if hasattr(self, "interfaz_actual"):
            self.interfaz_actual.destroy()
        self.interfaz_actual = VentanaPrincipal(self.panel_inferior)
        self.interfaz_actual.pack(fill="both", expand=True)

    def mostrar_interfaz_normal(self):
        self.deseleccionar_botones()
        self.boton_normal.state(['pressed'])  
        if hasattr(self, "interfaz_actual"):
            self.interfaz_actual.destroy()
        self.interfaz_actual = VentanaPrincipalN(self.panel_inferior)
        self.interfaz_actual.pack(fill="both", expand=True)
    
    def deseleccionar_botones(self):
        # Desactivar el estado 'pressed' de todos los botones
        self.boton_cuadrados_medios.state(['!pressed'])
        self.boton_lineal.state(['!pressed'])
        self.boton_multiplicativa.state(['!pressed'])
        self.boton_uniforme.state(['!pressed'])
        self.boton_normal.state(['!pressed'])
#Comprobación si este script es el principal para iniciar la aplicación
if __name__ == "__main__":
    app = App()
    app.mainloop()
