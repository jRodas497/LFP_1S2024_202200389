import json
import os
from lexema import Lexema
from error import Error

class analizador:
    def __init__(self):

        self.numero_linea = 1
        self.numero_columna = 1

        self.lista_lexema = []
        self.lista_instrucciones = []
        self.lista_errores = []
        
        self.palabras_reservadas = {
            'Inicio':'Inicio documento',
            'Encabezado':'Encabezado documento',
            'Cuerpo':'Cuerpo documento',
            'TituloPagina':'Titulo de Encabezado',
            'Titulo':'Titulo Cuerpo',
            'texto':'Texto',
            'posicion':'Posición',
            'tamaño':'Tamaño del texto',
            'color':'Color del texto',
            'Fondo':'Color del fondo',
            'Parrafo':'Parrafo del Cuerpo',
            'POSICION':'posicion',
            'fuente':'Fuente del texto',
            'Texto':'Texto del Cuerpo',
            'Codigo':'Fuente de código de ordenador',
            'Negrita':'Texto en Negrita',
            'Subrayado':'Texto Subrayado',
            'Tachado':'Texto Tachado',
            'Cursiva':'Texto en Cursiva',
            'Salto':'Salto de linea <p></p>',
            'cantidad':'Cantidad de Saltos de linea',
            'Tabla':'Tabla con formato',
            'elemento':'Contenido de la tabla y posición de F y C'
        }
        
        self.lexemas = list(self.palabras_reservadas.values())
        
    def simbolosValidos(self, char):
        return char in [":", "{", "}", ";", ",", "[", "]"]
    
    def instruccion0(self, cadena):
        print(cadena)
        lexema = ''
        puntero = 0
        while cadena:
            char = cadena[puntero]
            puntero += 1
            
            lexema += char
            print(lexema)
            if char == ':':
                print(lexema)
                puntero += 1
                if cadena[puntero] == '{':
                    self.instruccion1(cadena)
                    lexema, cadena = self.grupo_lexema(cadena[puntero:])
                    if lexema and cadena:
                        lexema[:-1]
                        if lexema not in self.lexemas:
                            e = Error((len(self.lista_errores)+1),lexema, "Error lexico", self.numero_linea, self.numero_columna)
                            self.lista_errores.append(e)
                            self.numero_columna += len(lexema) +1
                            puntero = 0
                        else:
                            lex = Lexema(lexema, self.numero_linea, self.numero_columna)
                            if lex:
                                self.lista_lexema.append(lex)
                                self.numero_columna += len(lexema) + 1
                                puntero = 0
                    
    def instruccion1(self, cadena):
        print('Instruccion 1')
    
            
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