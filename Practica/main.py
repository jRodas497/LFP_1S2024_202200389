import tkinter as tkin
from tkinter import filedialog
from School import School
    
def main():
    print("------------------------------------------------------")
    print("***PRACTICA 1 -- LENGUAJES FORMALES DE PROGRAMACIÓN***")
    print("------------------------------------------------------")
    menu()

def menu():
    program = School()
    while True:
        print("")
        print("-------------------------------------------------------")
        print("#############        MENÚ PRINCIPAL       #############")
        print("#############      GOTITAS DEL SABER      #############")
        print("-------------------------------------------------------")

        print("-------------------------------------------------------")
        print("| 1. SALIR                                            |")
        print("| 2. DATOS DEL ALUMNO                                 |")
        print("| 3. CARGAR ALUMNOS                                   |")
        print("| 4. AGREGAR CALIFICACIONES                           |")
        print("| 5. REPORTE ALUMNOS                                  |")
        print("| 6. REPORTE APROBADOS                                |")
        print("| 7. TOP 3 ALUMNOS                                    |")
        print("-------------------------------------------------------")
        
        print("")
        print("##     INGRESE UNA OPCION:     ##")
        opcion = input()
        print("")
        
        if opcion == '1':
            print('+++  Adios, esperamos volver a verte :)  +++')
            break
        elif opcion == '2':
            data()
        elif opcion == '3':
            name = loadDocument('est')
            if name:
                program.load_students(name)
                
        elif opcion == '4':
            name = loadDocument('cal')
            if name:
                program.add_ratings(name)
        elif opcion == '5':
            program.report()
            
        elif opcion == '6':
            program.approved()
            
        elif opcion == '7':
            program.top3()
            
        else:
            print('Opción no valida :( \n Vuelve a intentarlo')
            print('')
    
def data():
    print("-------------------------------------------------------")
    print("#############     DATOS DEL ESTUDIANTE    #############")
    print("-------------------------------------------------------")
    print("-> JUAN JOSÉ RODAS MANSILLA                           |")
    print("-> 202200389                                          |")
    print("-> LFP Sección A-                                     |")
    print("-> Ingenieria en Ciencias y Sistemas                  |")
    
    
def loadDocument(ext):
    root = tkin.Tk(); root.attributes('-alpha',0.01)
    root.attributes('-topmost',True)
    root.tk.eval(f'tk::PlaceWindow {root._w} center')
    root.withdraw()
    name = filedialog.askopenfilename(initialdir = "/", title = "Select a File", filetypes=[(f"{ext} files", f"*.{ext}")])
    
    if not name:
        root.destroy()
        print('Se ha cancelado')
        return None
    
    root.destroy()
    return name