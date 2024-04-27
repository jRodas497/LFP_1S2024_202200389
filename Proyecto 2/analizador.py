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
        errores = []
        textos = ''
        lexActual = ''
        estadoActual = estado0
        posActual = 0
        self.contador_comillas = 6
        self.comillas_abre = False
        self.linea = 1
        self.columna = 1
        
        while posActual < len(cadena):
            char = cadena[posActual]
            
            if char == '\n':
                self.linea += 1
                self.columna = 0
            else:
                self.columna += 1
            if estadoActual == estado0:
                if char.isspace():
                    pass
                elif char == '{':
                    tokensLexemas.append(('tk_llaveA', char, self.linea, self.columna))
                elif char == '}':
                    tokensLexemas.append(('tk_llaveC', char, self.linea, self.columna))
                elif char == ':':
                    tokensLexemas.append(('tk_DP', char, self.linea, self.columna))
                elif char == ';':
                    tokensLexemas.append(('tk_PyC', char, self.linea, self.columna))
                elif char == ',':
                    tokensLexemas.append(('tk_C', char, self.linea, self.columna))
                elif char == '(':
                    tokensLexemas.append(('tk_ParI', char, self.linea, self.columna))
                elif char == ')':
                    tokensLexemas.append(('tk_ParD', char, self.linea, self.columna))
                elif char == '+':
                    tokensLexemas.append(('tk_Mas', char, self.linea, self.columna))
                elif char == '*':
                    tokensLexemas.append(('tk_Ast', char, self.linea, self.columna))
                elif char == '"':
                    tokensLexemas.append(('tk_CD', char, self.linea, self.columna))
                elif char == '?':
                    tokensLexemas.append(('tk_Int', char, self.linea, self.columna))
                elif char == '|':
                    tokensLexemas.append(('tk_Or', char, self.linea, self.columna))
                elif char == '#':                    
                    comentario = self.armar_comentario(cadena[posActual:])
                    comentario = comentario[1:]
                    tokensLexemas.append(('tk_CDUL', comentario, self.linea +1, self.columna -1))
                elif char == '\'':
                    self.contador_comillas -= 1
                    if self.contador_comillas == 3:
                        self.comillas_abre = True
                        
                        print(cadena[posActual:])
                        comentario = self.comentario_multilinea(cadena[posActual:])        
                    
                    tokensLexemas.append(('tk_CM', comentario, self.linea, self.columna))     
                elif char == '.':
                    tokensLexemas.append(('tk_PD', char,self.linea, self.columna))
                elif char.isalpha():
                    lexActual += char
                    estadoActual = TOKEN
                elif char.isdigit():
                    lexActual += char
                    estadoActual = NUM
                else:
                    noPermitidos.append((char, self.linea, self.columna))
            elif estadoActual == TOKEN:
                if char.isalpha() or char.isdigit() or char == '_':
                    lexActual += char
                else:
                    if lexActual in self.reservadas:
                        if lexActual == 'ER':
                            tokensLexemas.append(('Palabra Reservada para ER', lexActual, self.linea, self.columna))
                            if char == ':':
                                exR, bool = self.er(cadena[posActual +1:])
                                if bool:
                                    tokensLexemas.append(('Expresión Regular', exR, self.linea, self.columna))
                                    self.columna = 0
                                else:
                                    errores.append(('ERROR! Se esperaba ";"', self.linea, self.columna + 4))
                                    self.columna = 0
                            else:
                                errores.append(('ERROR! Se esperaba ":"', self.linea, self.columna + 3))
                        elif lexActual == 'ID':
                            tokensLexemas.append(('Palabra Reservada para ID', lexActual, self.linea, self.columna))
                            if char == ':':
                                pass
                            else:
                                errores.append(('ERROR! Se esperaba ":"', self.linea, self.columna + 3))
                        elif lexActual == 'CADENAS':
                            tokensLexemas.append(('Palabra Reservada para CADENAS', lexActual, self.linea, self.columna))
                    elif not '#':
                        noPermitidos.append((lexActual, self.linea, self.columna))
                    lexActual = ''
                    estadoActual = estado0
                    continue
            elif estadoActual == NUM:
                if char.isdigit():
                    lexActual += char
                else:
                    tokensLexemas.append(('Numero', lexActual, self.linea, self.columna))
                    lexActual = ''
                    estadoActual = estado0
                    continue
            elif estadoActual == CAD:
                if char == '"':
                    lexActual += char
                    lexActual = lexActual.replace('"', '')
                    
                    tokensLexemas.append(('Cadena', lexActual, self.linea, self.columna))            

                    lexActual = ''
                    estadoActual = estado0
                else:
                    lexActual += char
                    
            posActual += 1
        return tokensLexemas, errores, textos
    
    def armar_comentario(self, cadena):
        token = ''
        for char in cadena:
            if char == '\n':
                self.linea -= 1
                return token                
            else:
                token += char
        return token
    
    def er(self, cadena):
        ER = ''
        dp : False
        for char in cadena:
            if char == ';':
                dp = True
                return ER, dp
            elif char == '\n':
                dp = False
                return ER, dp
            elif char != ' ':
                self.columna += 1
                ER += char
        
    
    def comentario_multilinea(self, cadena):
        print(cadena)
        token = ''
        comillas = 0
        saltos = 0
        
        for char in cadena:
            if char == '\'':
                comillas += 1           
                if comillas == 3:
                    self.contador_comillas = 6
                    self.comillas_abre = False
                    return token, saltos                 
        
            elif char == '\n':
                saltos += 1
                token += ' '
            else:
                token += char