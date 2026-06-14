import numpy as np


def leer_flotante(mensaje,negativos):
    while True:
        try:
            numero = float(input(mensaje))
            if negativos == True :
                return numero 
            else:
                if numero <= 0 :
                    print("numero debe ser posituivo")
                else:
                    return numero
        except:
            print("debe ser un numero")


def leer_angulo():
    while True :
        try:
            grados = float(input("ingrese el angulo engrados :"))
            if grados < -360 or grados >360 :
                print("angulo debe estar entra -360 y 360")
            else:
                angulo = np.deg2rad(grados)
                return angulo
        except:
            print("debe ser un numero")


def leer_entero(mensaje,negativos):
    while True:
        try:
            numero = int(input(mensaje))
            if negativos == True :
                return numero 
            else:
                if numero <= 0 :
                    print("numero debe ser positivo")
                else:
                    return numero
        except:
            print("debe ser un numero entero")




