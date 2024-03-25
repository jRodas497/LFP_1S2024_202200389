import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import tkinter.font as font
import json
import os

class app:
    def center_window(self, window):
        screen_width = window.winfo_screenwidth()
        screen_height = window.winfo_screenheight()
        x = (screen_width - 1350) // 2
        y = (screen_height - 850) // 2
        window.geometry(f"1350x850+{x}+{y}")
        
    def errores(self):
        self.analizador.generar_errores()
        messagebox.showinfo("Exito!", "El archivo se ha generado correctamente")

    def generar_reporte(self):
        self.analizador.generar_grafica()
        messagebox.showinfo("Exito!", "Reporte generado correctamente")

    def nombre_archivo(self, nombre):
        name = os.path.basename(nombre)
        self.variable_archivo.set(name)