import tkinter as tk
from tkinter import ttk
from Chi2 import ChiSquareAnalysisApp
from Ks import KSPruebaFrame
from Medios import MediosApp
from Poker import PruebaPoker
from Varianza import VarianzaApp


class MainApplication(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Análisis de Datos")
        self.attributes('-fullscreen', True)
        self.create_styles()
        self.create_widgets()

    def create_styles(self):
        self.style = ttk.Style(self)
        self.style.configure('Custom.TButton', foreground='black', background='#4CAF50', font=('Helvetica', 12))

    def create_widgets(self):
        # Panel superior para los botones de selección de archivo
        self.top_panel = tk.Frame(self)
        self.top_panel.pack(fill=tk.BOTH, expand=False)

        # Botones para cada análisis
        self.button_medios = ttk.Button(self.top_panel, text="Prueba de Medias", command=self.open_medios, style='Custom.TButton')
        self.button_medios.grid(row=0, column=0, padx=10, pady=10)

        self.button_varianza = ttk.Button(self.top_panel, text="Prueba de Varianza", command=self.open_varianza, style='Custom.TButton')
        self.button_varianza.grid(row=0, column=1, padx=10, pady=10)

        self.button_ks = ttk.Button(self.top_panel, text="Prueba de Kolmogorov-Smirnov", command=self.open_ks, style='Custom.TButton')
        self.button_ks.grid(row=0, column=2, padx=10, pady=10)

        self.button_chi2 = ttk.Button(self.top_panel, text="Prueba de Chi-Cuadrado", command=self.open_chi2, style='Custom.TButton')
        self.button_chi2.grid(row=0, column=3, padx=10, pady=10)

        self.button_poker = ttk.Button(self.top_panel, text="Prueba de Poker", command=self.open_poker, style='Custom.TButton')
        self.button_poker.grid(row=0, column=4, padx=10, pady=10)

        self.button_salir = ttk.Button(self.top_panel, text="Salir", command=self.salir, style='Custom.TButton')
        self.button_salir.grid(row=0, column=5, padx=10, pady=10)

        ttk.Separator(self, orient='horizontal').pack(fill='x')

        # Panel inferior para mostrar los análisis
        self.bottom_panel = tk.Frame(self)
        self.bottom_panel.pack(fill=tk.BOTH, expand=True)

    def limpiar_panel_inferior(self):
        # Destruir todos los widgets dentro del panel inferior
        for widget in self.bottom_panel.winfo_children():
            widget.destroy()

    def open_chi2(self):
        self.limpiar_panel_inferior()
        self.interfaz_actual = ChiSquareAnalysisApp(self.bottom_panel)
        self.interfaz_actual.place(relx=0.5, rely=0.5, anchor=tk.CENTER)  # Centrar la interfaz en el panel inferior

    def open_ks(self):
        self.limpiar_panel_inferior()
        self.interfaz_actual = KSPruebaFrame(self.bottom_panel)
        self.interfaz_actual.pack(fill="both", expand=True, anchor="center")

    def open_medios(self):
        self.limpiar_panel_inferior()
        self.interfaz_actual = MediosApp(self.bottom_panel)
        self.interfaz_actual.pack(fill="both", expand=True, anchor="center")

    def open_poker(self):
        self.limpiar_panel_inferior()
        self.interfaz_actual = PruebaPoker(self.bottom_panel)
        self.interfaz_actual.pack(fill="both", expand=True, anchor="center")

    def open_varianza(self):
        self.limpiar_panel_inferior()
        self.interfaz_actual = VarianzaApp(self.bottom_panel)
        self.interfaz_actual.pack(fill="both", expand=True, anchor="center")

    def salir(self):
        self.destroy()

if __name__ == "__main__":
    app = MainApplication()
    app.mainloop()
