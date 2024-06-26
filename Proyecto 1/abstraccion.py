from abc import ABC, abstractmethod

class Expression(ABC):
    def __init__(self, fila, columna):
        self.fila = fila
        self.columna = columna

    @abstractmethod
    def obtener_Fila(self):
        return self.fila

    @abstractmethod
    def obtener_Columna(self):
        return self.columna