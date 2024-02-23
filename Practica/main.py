import tkinter as tkin
from tkinter import filedialog
from School import School
    
def main():
    print("------------------------------------------------------")
    print("***PRACTICA 1 -- LENGUAJES FORMALES DE PROGRAMACIÓN***")
    print("------------------------------------------------------")
    menu()

def menu():
    print("")
    print("-------------------------------------------------------")
    print("#############        MENÚ PRINCIPAL       #############")
    print("#############      GOTITAS DEL SABER      #############")
    print("-------------------------------------------------------")

    print("-------------------------------------------------------")
    print("| 1. SALIR                                            |")
    print("| 2. DATOS DEL ALUMNO                                 |")
    print("| 2. CARGAR ALUMNOS                                   |")
    print("| 4. AGREGAR CALIFICACIONES                           |")
    print("| 5. REPORTE DE ALUMNOS                               |")
    print("| 6. REPORTE DE APROBADOS                             |")
    print("| 7. TOP 3 ALUMNOS                                    |")
    print("-------------------------------------------------------")
    
    print("")
    print("##     INGRESE UNA OPCION:     ##")
    opcion = input()
    print("")
    
    if opcion == '1':
        print('+++  Adios, esperamos volver a verte :)  +++')
    elif opcion == '2':
        data()
    elif opcion == '3':
        menu()
    elif opcion == '4':
        menu()
    elif opcion == '5':
        menu()
    elif opcion == '6':
        menu()
    elif opcion == '7':
        menu()
    else:
        print('Opción no valida :( \n Vuelve a intentarlo')
        menu()
    
def data():
    print("-------------------------------------------------------")
    print("#############     DATOS DEL ESTUDIANTE    #############")
    print("-------------------------------------------------------")
    print("-> JUAN JOSÉ RODAS MANSILLA                           |")
    print("-> 202200389                                          |")
    print("LFP Sección A-                                        |")
    print("-> Ingenieria en Ciencias y Sistemas                  |")
    
    menu()
main()