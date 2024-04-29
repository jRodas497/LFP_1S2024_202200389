import os
import tkinter as tk
import tkinter.font as font
from tkinter import ttk, filedialog, messagebox
from analizador import analizador
from Token import Token

datos = ''

class app:
    def __init__(self, raiz):
        self.txt = ''
        self.variable_archivo = tk.StringVar()
        self.variable_archivo.set("")
        self.analizador = analizador()
        self.raiz = raiz
        self.raiz.config(bg="#fdf9c4")
        self.raiz.title("Analizador lexico")
        self.raiz.resizable(0,0)
        self.menu_frame = tk.Frame(self.raiz, width="1450", height="120", bg="#FDF9DF")
        self.menu_frame.pack_propagate(False)
        self.menu_frame.grid_propagate(False)
        self.menu_frame.pack()
        self.screen_width = self.raiz.winfo_screenwidth()
        self.screen_height = self.raiz.winfo_screenheight()
        x = (self.screen_width - 1450) // 2
        y = (self.screen_height - 700) // 2
        self.raiz.geometry(f"1450x700+{x}+{y}")

        self.menu_frame.columnconfigure(0, weight=10)  # Columna vacía
        self.menu_frame.columnconfigure(1, weight=10)  # Columna para el botón "Analizar"
        self.menu_frame.columnconfigure(2, weight=10)  # Columna para el botón "Errores"
        self.menu_frame.columnconfigure(3, weight=10) 

        self.editor_frame = tk.Frame()

        self.editor_frame.pack()
        self.editor_frame.config(width="1450", height="600", bg="#fdf9c4")
        #EDITOR
        self.editor = tk.Text(self.editor_frame, width="50", height="27", padx=35, pady=20, font=('Arial', 12), bg='lightgray')
        self.editor.grid(row=0, column=0, padx=10, pady=25)
        self.editor.bind("<KeyRelease>", self.guardar_contenido)
        #SCROLL EDITOR
        self.scroll_editor = tk.Scrollbar(self.editor_frame, command=self.editor.yview)
        self.scroll_editor.grid(row=0, column=1, pady=25, sticky="nse")
        self.editor.config(yscrollcommand=self.scroll_editor.set) 
        #LISTADO
        self.tabla = ttk.Treeview(self.editor_frame, height='25')
        self.tabla["columns"] = ("Expresión Regular", "Cadena", "Cumple")
        #HACER TABLA Y LIMPIARLA
        self.tabla.column("#0", width=0, stretch=tk.NO) 
        self.tabla.column("Expresión Regular", anchor=tk.W, width=350)
        self.tabla.column("Cadena", anchor=tk.W, width=350)
        self.tabla.column("Cumple", anchor=tk.W, width=150)
        #HEADERS DE TABLA
        self.tabla.heading('#0', text='', anchor=tk.W)
        self.tabla.heading('Expresión Regular', text='Expresión Regular', anchor=tk.W)
        self.tabla.heading('Cadena', text='Cadena', anchor=tk.W)
        self.tabla.heading('Cumple', text='Cumple', anchor=tk.W)

        self.tabla.grid(row=0, column=2, padx=10, pady=25)
        #SCROLL LISTADO
        scroll_tabla = tk.Scrollbar(self.editor_frame, command=self.tabla.yview)
        scroll_tabla.grid(row=0, column=3, pady=25, sticky="nse")
        self.tabla.config(yscrollcommand=scroll_tabla.set) 
        
        fuente = font.Font(weight="bold")
    #ABRIR ARCHIVO
        self.abrir = tk.Button(self.menu_frame, text="Abrir Archivo", padx=20, height=1, bg="#fdf9c4", activebackground="#ffda9e", command=self.abrir_archivo)
        self.abrir.grid(row=0, column=0, padx=10, pady=10)
        self.abrir['font'] = fuente
    #GUARDAR ARCHIVO
        self.guardar = tk.Button(self.menu_frame, text="Guardar Archivo", padx=20, height=1, bg="#fdf9c4", activebackground="#ffda9e", command=self.guardar_archivo)
        self.guardar.grid(row=0, column=1, padx=10, pady=10)
        self.guardar['font'] = fuente
    #GUARDAR ARCHIVO COMO
        self.guardarcomo = tk.Button(self.menu_frame, text="Guardar Como Archivo", padx=20, height=1, bg="#fdf9c4", activebackground="#ffda9e", command=self.guardar_como)
        self.guardarcomo.grid(row=0, column=2, padx=10, pady=10)
        self.guardarcomo['font'] = fuente
    #REPORTES TOKENS
        self.tokens = tk.Button(self.menu_frame, text='Reporte Tokens', padx=20, height=1, bg="#fdf9c4", activebackground="#ffda9e", command=self.tokens)
        self.tokens.grid(row=1, column=0, padx=10, pady=10)
        self.tokens['font'] = fuente
    #REPORTES ERRORES
        self.error = tk.Button(self.menu_frame, text='Reporte de Errores', padx=20, height=1, bg="#fdf9c4", activebackground="#ffda9e", command=self.errores)
        self.error.grid(row=1, column=1, padx=10, pady=10)
        self.error['font'] = fuente
    #EMPEZAR ANALIZADO DE AFD
        self.execute = tk.Button(self.menu_frame, text='Ejecutar', padx=20, height=1, bg="#fdf9c4", activebackground="#ffda9e", command=self.analizado)
        self.execute.grid(row=1, column=2, padx=10, pady=10)
        self.execute['font'] = fuente
        
        self.raiz.mainloop()

    def guardar_contenido(self, event = None):
        self.txt = self.editor.get("1.0", "end-1c")  # Obtener todo el texto del widget
        print(self.txt)
    
    def actualizar_variable(self, event=None):
        self.txt = self.editor.get("1.0", 'end-1c')

    def abrir_archivo(self):
        self.archivo = filedialog.askopenfilename(filetypes=[("Archivo TXT", "*.txt")])
        if self.archivo:
            with open(self.archivo, 'r', encoding='latin-1') as file:
                self.txt = file.read()
                self.editor.delete("1.0", tk.END)
                self.editor.insert(tk.END, self.txt)

    def guardar_archivo(self):
        if self.editor and self.archivo:
            try:
                self.datos_json = self.editor.get("1.0", tk.END)
                with open(self.archivo, 'w') as file:
                    file.write(self.editor.get("1.0", tk.END))
                messagebox.showinfo("Exito!", "El archivo se ha guardado correctamente")
            except Exception as e:
                messagebox.showinfo("Error!", "Error al guardar el archivo "+ str(e))

    def guardar_como(self):
        if self.editor:
            self.archivo = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Archivo TXT", "*.txt")])
            self.nombre_archivo(self.archivo)
            self.datos_json = self.editor.get("1.0", tk.END)
            if self.archivo:
                with open(self.archivo, "w") as file:
                    file.write(self.editor.get("1.0", tk.END))
            messagebox.showinfo("Exito!", "El archivo se ha guardado correctamente")

    def nombre_archivo(self, nombre):
        name = os.path.basename(nombre)
        self.variable_archivo.set(name)
        
    def analizado(self):
        count = 0
        editorTXT = self.txt
        if len(editorTXT) != 0:
            tokens_lexemas, no_permitidos, textos, tabla = self.analizador.analize(editorTXT)
            self.analizador.analize(editorTXT)
            
            if tabla:
                self.tabla.delete(*self.tabla.get_children())
                for t in tabla:    
                    count += 1
                    if count % 2 == 0:
                        self.tabla.insert('', 'end',text=count, values=(t[1], t[0], 'pendiente'))
                    
            self.tabla.tag_configure("f1", background="lightgray")
        
            for i, fila in enumerate(self.tabla.get_children()):
                if i % 2 == 0:
                    self.tabla.item(fila, tags=("f1",))
            
            # TOKENS LEXEMAS
            with open('TokensLexemas.html', 'w') as file:
                file.write('<html><head><style>')
                file.write('table {  margin: 15px;  padding: 15px;}')
                file.write('</style></head><body><h1>Tokens Lexemas</h1><table>')
                file.write('<thead><tr><th>Token</th><th>Lexema</th><th>Linea</th><th>Columna</th></tr></thead><tbody>')
                for tokens in tokens_lexemas:
                    file.write(f'<tr><td>{tokens[0]}</td><td>{tokens[1]}</td><td>{tokens[2]}</td><td>{tokens[3]}</td></tr>')
                    
                file.write('</tbody></table></body></html>')
            
            # NO PERMITIDOS
            with open('ListadoDeNoPermitidos.html', 'w') as file:
                file.write('<html><head><style> tr {  margin: 15px;  padding: 15px;}')
                file.write('table {  margin: 15px;  padding: 15px;}')
                file.write('</style></head><body><h1>Caracteres no permitidos</h1><table>')
                file.write('<thead><tr><th>Carácter</th><th>Linea</th><th>Columna</th></tr></thead><tbody>')
                for np in no_permitidos:
                    file.write(f'<tr><td>{np[0]}</td><td>{np[1]}</td><td>{np[2]}</td></tr>')
                    
                file.write('</tbody></table></body></html>')            
        else:
            messagebox.showinfo('Error!', 'La entrada no es valida')
        
    def tokens(self):
        if os.name == 'nt':
            os.system('start ' + 'TokensLexemas.html')
        
    def errores(self):
        if os.name == 'nt':
            os.system('start ' + 'ListadoDeNoPermitidos.html')
        
raiz = tk.Tk()
ventana = app(raiz)
