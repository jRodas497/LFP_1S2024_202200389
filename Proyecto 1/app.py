import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import tkinter.font as font
import json
import os
from analizador import analizador

class app:
    def __init__(self, raiz):        
        self.archivo = ""
        self.txt = ''

        self.variable_archivo = tk.StringVar()
        self.variable_archivo.set("")
        self.analizador = analizador()

        self.raiz = raiz
        self.cantidad_lineas = 1
        self.raiz.config(bg="#fdf9c4")
        self.raiz.title("Analizador lexico")
        self.raiz.resizable(0,0)
        #CABECERA
        self.menu_frame = tk.Frame(self.raiz, width="1350", height="60", bg="#FDF9DF")
        self.menu_frame.pack_propagate(False)
        self.menu_frame.grid_propagate(False)
        self.menu_frame.pack()
        self.menu_frame.columnconfigure(0, weight=1)
        self.menu_frame.columnconfigure(1, weight=1)
        self.menu_frame.columnconfigure(2, weight=1)
        self.menu_frame.columnconfigure(3, weight=1)
        self.fuente = font.Font(weight="bold")
        # BOTON 
        self.abrir = tk.Button(self.menu_frame, text="Abrir Archivo", padx=20, height=1, bg="#fdf9c4", activebackground="#ffda9e", command=self.abrir_archivo)
        self.abrir.grid(row=0, column=1, padx=10, pady=10)
        self.abrir['font'] = self.fuente
        self.traducir = tk.Button(self.menu_frame, text="TRADUCIR", padx=20, height=1, bg="#fdf9c4", activebackground="#ffda9e", command = self.traducir)
        self.traducir.grid(row=0, column=2, padx=10, pady=20)
        self.traducir['font'] = self.fuente
        # TEXTO INDICADOR DE TEXTOS
        self.texto_frame = tk.Frame(self.raiz, width="1350", height="60", bg="#FDF9DF")
        self.texto_frame.pack_propagate(False)
        self.texto_frame.grid_propagate(False)
        self.texto_frame.pack()    
        self.textoEntrada = tk.Label(self.texto_frame, pady = 15, font = ('Arial', 12), bg = '#FDF9DF', text='Texto de entrada:')
        self.textoEntrada.grid(row = 0, column = 1, padx=150)
        self.textoTraduccion = tk.Label(self.texto_frame, pady = 15, font = ('Arial', 12), bg = '#FDF9DF', text='Texto de entrada:')
        self.textoTraduccion.grid(row = 0, column = 3, padx=300)        
        # CUADROS DE TEXTO 
        ### Frame de Cuadros
        self.editor_frame = tk.Frame(self.raiz, width="1350", height="60", bg="gray")
        self.editor_frame.config(width="600", height="700", bg="#fdf9c4")
        self.editor_frame.pack()
        # Cuadro del TXT
        self.editor = tk.Text(self.editor_frame, width="50", height="30", padx=35, pady=20, font=('Arial', 12), bg='lightgray')
        self.editor.grid(row=0, column=1, padx=10, pady=25)
        # ScrollBar
        self.scroll_editor = tk.Scrollbar(self.editor_frame, command=self.editor.yview)
        self.scroll_editor.grid(row=0, column=2, pady=25, sticky="nse")
        self.editor.config(yscrollcommand=self.scroll_editor.set)     
        #Cuadro Traducido
        self.traducido = tk.Text(self.editor_frame, width="50", height="30", padx=35, pady=20, font=('Arial', 12), bg='lightgray', state='disabled')
        self.traducido.grid(row=0, column=3, padx=10, pady=25)
        
    def abrir_archivo(self):
        self.analizador.limpiar_listas()
        self.archivo = filedialog.askopenfilename(filetypes=[("Archivo TXT", "*.txt")])
        if self.archivo:
            with open(self.archivo, 'r') as file:
                self.txt = file.read()
                self.editor.delete("1.0", tk.END)
                self.editor.insert(tk.END, self.txt)            
            
    def traducir(self):
        self.analizador.limpiar_listas()
        editorTXT = self.txt
        
        if len(editorTXT) != 0:
            self.analizador.instruccion0(editorTXT)
        else:
            messagebox.showinfo("Error!", "La entrada no es valida")
    
    def center_window(self, window):
        screen_width = window.winfo_screenwidth()
        screen_height = window.winfo_screenheight()
        x = (screen_width - 1350) // 2
        y = (screen_height - 950) // 2
        window.geometry(f"1350x850+{x}+{y}")
        
    def errores(self):
        self.analizador.generar_errores()
        messagebox.showinfo("Exito!", "El archivo se ha generado correctamente")
        
raiz = tk.Tk()
ventana = app(raiz)
ventana.center_window(raiz)

raiz.mainloop()