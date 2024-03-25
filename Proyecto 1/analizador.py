import json
import os
from lexema import *

class analizador:
    def __init__(self):

        self.numero_linea = 1
        self.numero_columna = 1

        self.lista_lexema = []
        self.lista_instrucciones = []
        self.lista_errores = []

        # CONFIGURACIONES
        self.fondo = ''
        self.texto = ''
        self.fuente = ''
        self.forma = ''
        
        self.palabras_reservadas = {
            'INICIO':'Inicio',
            'ENCABEZADO':'Encabezado',
            'CUERPO':'Cuerpo',
            'TITULOPAGINA':'TituloPagina',
            'TITULO':'Titulo',
            'TEXTO':'texto',
            'POSICION':'posicion',
            'TAMAÑO':'tamaño',
            'COLOR':'color',
            'FONDO':'Fondo',
            'PARRAFO':'Parrafo',
            'POSICION':'posicion',
            'FUENTE':'fuente',
            'TEXTO':'Texto',
            'CODIGO':'Codigo',
            'NEGRITA':'Negrita',
            'SUBRAYADO':'Subrayado',
            'TACHADO':'Tachado',
            'CURSIVA':'Cursiva',
            'SALTO':'Salto',
            'CANTIDAD':'cantidad',
            'TABLA':'Tabla',
            'FILAS':'filas',
            'COLUMNAS':'columnas',
            'ELEMENTO':'elemento'
        }
        
        self.lexemas = list(self.palabras_reservadas.values())
        
    def instruccion(self, cadena):
        lexema = ''
        puntero = 0

        while cadena:
            char = cadena[puntero]
            puntero += 1
            
            if char == '\"':
                lexema, cadena = self.grupo_lexema(cadena[puntero:])
                if lexema and cadena:
                    self.numero_columna += 1
                    lex = Lexema(lexema, self.numero_linea, self.numero_columna)

                    self.lista_lexema.append(lex)
                    self.numero_columna += len(lexema) + 1
                    puntero = 0
            else:
                pass
            
    def grupo_lexema(self, cadena):
        lexema = ''
        puntero = ''

        for char in cadena:
            puntero += char
            if char == '\"':
                return lexema, cadena[len(puntero):]
            else :
                lexema += char
        return None, None
    
    def generar_errores(self):
        datos = {}

        datos["errores"] = []
        for error in self.lista_errores:
            datos["errores"].append({
                "No": int(error.numero),
                "descripcion": {
                    "lexema": error.lexema,
                    "tipo": error.tipo,
                    "columna": int(error.columna),
                    "fila": int(error.fila)
                }
            })
        
        try:
            with open('RESULTADOS_202201444.json', 'w') as file:
                json.dump(datos, file, indent = 4)
        except Exception as e:
            print(e)
            
    def limpiar_listas(self):
        self.lista_lexema.clear()
        self.lista_instrucciones.clear()
        self.lista_errores.clear()


        self.numero_linea = 1
        self.numero_columna = 1
        # CONFIGURACIONES
        self.fondo = ''
        self.texto = ''
        self.fuente = ''
        self.forma = ''