import re
import json
import os
from lexema import Lexema
from error import Error

class analizador:
    def __init__(self):
        self.reservadas = [
            'Inicio', 
            'Encabezado', 
            'Cuerpo', 
            'Titulo', 
            'Fondo', 
            'Parrafo', 
            'Texto', 
            'Codigo', 
            'Negrita','Subrayado', 
            'Tachado', 
            'Cursiva', 
            'Salto', 
            'Tabla', 
            'elemento', 
            'filas', 
            'columnas', 
            'elemento','TituloPagina', 
            'texto', 
            'posicion', 
            'tamaño', 
            'color', 
            'fuente', 
            'cantidad'
        ]
    
    def instruccion0(self, cadena):
        estado0 = 0
        TOKEN = 1
        NUM = 2
        CAD = 3
        
        tokensLexemas = []
        noPermitidos = []
        textos = ''
        lexActual = ''
        estadoActual = estado0
        posActual = 0
        linea = 1
        columna = 1
        
        while posActual < len(cadena):
            char = cadena[posActual]
        
            if char == '\n':
                linea += 1
                columna = 0
            else:
                columna += 1
            if estadoActual == estado0:
                if char.isspace():
                    pass
                elif char == '{':
                    tokensLexemas.append(('Llave de apertura', char, linea, columna))
                elif char == '}':
                    tokensLexemas.append(('Llave de cerrar', char, linea, columna))
                elif char == ':':
                    tokensLexemas.append(('Dos puntos', char, linea, columna))
                elif char == ';':
                    tokensLexemas.append(('Punto y coma', char, linea, columna))
                elif char == ',':
                    tokensLexemas.append(('Coma', char, linea, columna))
                elif char == '[':
                    tokensLexemas.append(('Corchete de apertura', char, linea, columna))
                elif char == ']':
                    tokensLexemas.append(('Llave de cerrar', char, linea, columna))
                elif char == '=':
                    tokensLexemas.append(('Signo igual', char, linea, columna))
                elif char == '"':
                    lexActual += char
                    estadoActual = CAD
                elif char.isalpha():
                    lexActual += char
                    estadoActual = TOKEN
                elif char.isdigit():
                    lexActual += char
                    estadoActual = NUM
                else:
                    noPermitidos.append((char, linea, columna))
            elif estadoActual == TOKEN:
                if char.isalpha() or char.isdigit() or char == '_':
                    lexActual += char
                else:
                    if lexActual in self.reservadas:
                        tokensLexemas.append(('Palabra reservada', lexActual, linea, columna))
                    else:
                        noPermitidos.append((lexActual, linea, columna))
                    lexActual = ''
                    estadoActual = estado0
                    continue
            elif estadoActual == NUM:
                if char.isdigit():
                    lexActual += char
                else:
                    tokensLexemas.append(('Numero', lexActual, linea, columna))
                    lexActual = ''
                    estadoActual = estado0
                    continue
            elif estadoActual == CAD:
                if char == '"':
                    lexActual += char
                    lexActual = lexActual.replace('"', '')
                    
                    tokensLexemas.append(('Cadena', lexActual, linea, columna))            
                    
                    a = re.sub(r'[^\w\s]', '', lexActual)
                    b = re.sub(r'\d+', '', a)
                    c = re.sub(r'[\d\n]+', '', b)
                    
                    textos += c + '\n'

                    lexActual = ''
                    estadoActual = estado0
                else:
                    lexActual += char
                    
            posActual += 1
        return tokensLexemas, noPermitidos, textos
                
    def validar_cadena(self, cadena):
        patron = r'^[a-zA-Z]+$'
        return bool(re.match(patron, cadena))
            
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