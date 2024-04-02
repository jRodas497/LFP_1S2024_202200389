class Error():
    def __init__(self, lexema, palabra, type, fila, columna):
        self.lexema = lexema
        self.palabra = palabra
        self.type = type
        self.fila = fila
        self.columna = columna