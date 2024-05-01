from listas.lexema import *
import re

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
        tabla = []
        errores = []
        self.expresiones = []
        self.registros = []
        textos = ''
        lexActual = ''
        estadoActual = estado0
        posActual = 0
        self.contador_comillas = 0
        self.comillas_abre = False
        self.linea = 1
        self.columna = 1
        
        last = cadena[-1]
        first = cadena[0]
        
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
                    tokensLexemas.append(('TOKEN_llaveA', char, self.linea, self.columna))
                    opt, linea, columna = self.verificar_llave(cadena[posActual +1:])
                    if opt == 'coma':
                        errores.append(('ERROR! Coma faltante', linea, columna))
                    else:
                        self.registros.append((opt))
                    
                elif last == ',' or first == ',':
                    last = ''
                    first = ''
                    errores.append(('Coma no reconocida', 'Last', 1))
                elif char == '}':
                    tokensLexemas.append(('TOKEN_llaveC', char, self.linea, self.columna))
                elif char == ':':
                    tokensLexemas.append(('TOKEN_DP', char, self.linea, self.columna))
                elif char == ';':
                    tokensLexemas.append(('TOKEN_PyC', char, self.linea, self.columna))
                elif char == ',':
                    tokensLexemas.append(('TOKEN_C', char, self.linea, self.columna))
                elif char == '(':
                    tokensLexemas.append(('TOKEN_ParI', char, self.linea, self.columna))
                elif char == ')':
                    tokensLexemas.append(('TOKEN_ParD', char, self.linea, self.columna))
                elif char == '+':
                    tokensLexemas.append(('TOKEN_Mas', char, self.linea, self.columna))
                elif char == '*':
                    tokensLexemas.append(('TOKEN_Ast', char, self.linea, self.columna))
                elif char == '"':
                    tokensLexemas.append(('TOKEN_CD', char, self.linea, self.columna))
                elif char == '?':
                    tokensLexemas.append(('TOKEN_Int', char, self.linea, self.columna))
                elif char == '|':
                    tokensLexemas.append(('TOKEN_Or', char, self.linea, self.columna))
                elif char == '#':                    
                    comentario = self.armar_comentario(cadena[posActual:])
                    comentario = comentario[1:]
                    tokensLexemas.append(('TOKEN_CDUL', comentario, self.linea +1, self.columna -1))
                elif char == '\'':
                    self.contador_comillas += 1
                    if self.contador_comillas == 3:
                        cadena, espacios_encontrados = self.comentario_multilinea(cadena[1:])
                        self.linea += espacios_encontrados
                        self.columna = 1
                        self.contador_comillas = 0                        
                        posActual = 0                    
                        tokensLexemas.append(('TOKEN_CM', cadena, self.linea, self.columna))     
                    else:
                        cadena = cadena[1:]
                    posActual = 0
                elif char == '.':
                    tokensLexemas.append(('TOKEN_PD', char,self.linea, self.columna))
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
                                self.exR, bool = self.er(cadena[posActual +1:])
                                if bool:
                                    tokensLexemas.append(('Expresión Regular', self.exR, self.linea, self.columna))
                                    self.columna = 0
                                else:
                                    errores.append(('ERROR! Se esperaba ";"', self.linea, self.columna + 4))
                                    self.columna = 0
                            else:
                                errores.append(('ERROR! Se esperaba ":"', self.linea, self.columna + 3))
                        
                        elif lexActual == 'ID':
                            tokensLexemas.append(('Palabra Reservada para ID', lexActual, self.linea, self.columna))
                            if char == ':':
                                ret = self.digit(cadena[posActual +1:])
                                number, pyc, car = ret
                                num = self.numeros(cadena[posActual +1:])
                                if num:
                                    if pyc:
                                        tokensLexemas.append(('Numeración', num, self.linea, self.columna))
                                        self.columna = 0
                                        
                                    else:
                                        errores.append(('ERROR! Se esperaba ";"', self.linea, self.columna + 3))
                                elif car != '':
                                    errores.append((f'ERROR! Carácter no valido "{car}"', self.linea, self.columna + 3))
                            else:
                                errores.append(('ERROR! Se esperaba ":"', self.linea, self.columna + 3))
                                
                        elif lexActual == 'CADENAS':
                            tokensLexemas.append(('Palabra Reservada para CADENAS', lexActual, self.linea, self.columna))
                            if char == ':':
                                ret = self.chains(cadena[posActual +1:])
                                CAD, pyc = ret    
                                print(CAD)
                                expresion = self.exR
                                
                                a = self.separate_chains(CAD, expresion)
                                cadenas, error = a
                                
                                for i in cadenas:
                                    for j in cadenas:
                                        if j == i:
                                            print('Registro repetido')
                                        else:
                                            if error:
                                                errores.append(('ERRROR! Sintaxis de cadenas mal realizada', self.linea, self.columna))
                                            else:
                                                tabla.append((i, self.exR))
                                if pyc:
                                    tokensLexemas.append(('Conjunto de Cadenas a comprobar', CAD, self.linea, self.columna))
                                    self.columna = 0
                                else:
                                    errores.append(('ERROR! Se esperaba ";"', self.linea, self.columna + 4))
                                    self.columna = 0
                            else:
                                errores.append(('ERROR! Se esperaba ":"', self.linea, self.columna + 3))
                                
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
        self.analizador_sintactico()
        return tokensLexemas, errores, textos, tabla
    
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
        dp = False
        for char in cadena:
            if char == ';':
                dp = True
                return ER, dp
            elif char == '\n':
                dp = False
                return ER, dp
            else:
                self.columna += 1
                ER += char
        
    def digit(self, cadena):
        pyc = False
        number = ''
        
        for char in cadena:            
            if char.isdigit():
                number += char
            else:
                if char == ';':
                    char = ''
                    pyc = True
                    return number, pyc, char
                if char == '\n':
                    char = ''
                    return number, pyc, char               
                if char == ' ' :
                    continue
                else:
                    print(char)
                    return number, pyc, char
                    
    def chains(self, cadena):
        CAD = ''
        pyc = False
        
        for char in cadena:
            if char == ';':
                pyc = True
                return CAD, pyc
            elif char == '\n':
                return CAD, pyc
            else:
                self.columna += 1
                CAD += char
    
    def separate_chains(self, cadena, expresion):
        self.find = False
        error = False
        for e in self.expresiones:
            if e == expresion:
                self.find = True
        
        if not self.find:
            self.expresiones.append((expresion))
            
            # Definir el patrón de búsqueda para encontrar las cadenas entre comillas
            patron = r'"([^"]*)"'
            # Buscar todas las coincidencias del patrón en la cadena
            coincidencias = re.findall(patron, cadena)
            
            # Verificar si las cadenas están correctamente formadas
            for coincidencia in coincidencias:
                if coincidencia == '':
                    error = True
                    print("¡Error! Las comillas dobles faltan o están mal colocadas.")
                                
            # Formatear cada coincidencia con comillas dobles y separarlas por comas
            registros = [ coincidencia for coincidencia in coincidencias ]
            
            return registros, error
        
    def numeros(self, cadena):
        numero = ''
        puntero = ''
        es_decimal = False
        for char in cadena:
            puntero += char
            if char == '.':
                es_decimal = True
            if char == '\"' or char == ' ' or char == '\n' or char == '\t' or char == ',' or char == '}' or char == ')':
                if es_decimal:
                    return numero
                else:
                    return numero
            else:
                numero += char
        return None
        
    def comentario_multilinea(self, cadena):
        print(cadena)
        comillas = 0
        puntero = 0
        no_enters = 0
        
        for char in cadena:
            puntero += 1
            if comillas < 3:
                if char == '\'':
                    comillas += 1
                elif char == '\n':
                    no_enters +=1
                    comillas = 0
                else:
                    comillas = 0
            else:
                return cadena[(puntero+1):], no_enters
        return None, None
        
    def verificar_llave(self, cadena):
        cad = ''    
        columna = 0
        linea = 0
        for char in cadena:
            if char == ' ' or char == '\r':
                cad += char
                cadena = cadena[1:]
                columna += 1
            elif char == '\n':
                cad += char
                cadena = cadena[1:]
                linea += 1
                columna = 1
            elif char == '\t':
                cad += char
                columna += 4
                cadena = cadena[4:]
            elif char == '}':
                return cad, None, None
            elif char == '{':
                #Falta una coma
                return 'coma', linea, columna
            else:
                cad += char
                
    def analizador_sintactico(self):
        cad = ''
        for r in self.registros:
            for char in r:
                cad += char
                if cad == 'ID':
                    pass
                elif cad == 'ER':
                    pass
                elif cad == 'CADENAS':
                    pass