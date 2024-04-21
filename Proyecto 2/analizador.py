import re
import json
import os

class analizador:
    def __init__(self):
        self.reservadas = [
            'ER',
            'CADENAS',
            'ID'
        ]
        
    def analize(self, cadena):
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
                elif char == '+':
                    tokensLexemas.append(('1 o más ocurrencias de R', char, linea, columna))
                elif char == '*':
                    tokensLexemas.append(('0 o más ocurrencias de R', char, linea, columna))
                elif char == '?':
                    tokensLexemas.append(('0 o 1 ocurrencia de R', char, linea, columna))
                elif char == '|':
                    tokensLexemas.append(('Alterna entre R1 y R2', char, linea, columna))
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