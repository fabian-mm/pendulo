import numpy as np
from scipy.integrate import solve_ivp
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from utils import leer_flotante,leer_angulo,leer_entero


class Pendulo:
    def __init__(self):
        self.longitud = None
        self.gravedad = 9.8 
        self.valores_iniciales = None
        self.t_inicial = None
        self.t_final = None

    def ecuacion(self,t,y):
        Posicion,velocidad = y
        factor = (self.gravedad/self.longitud)
        return  [velocidad , -factor*np.sin(Posicion)]
        
    def add_l(self):
        longitud=leer_flotante("ingrese la longitud :",False)
        self.longitud = longitud

    def add_val_iniciales(self):
        angulo =leer_angulo()
        vel_grados = leer_flotante("ingrese grados por segundo :",True)
        vel_rad = np.deg2rad(vel_grados)
        self.valores_iniciales = [angulo,vel_rad]

    def add_tiempo(self):
        t_inicio = leer_flotante("ingrese segundo de inicio para la simulacion :",False)
        while True :
            t_finall = leer_flotante("ingrese segundo de finalizacion para la simulacion :",False)
            if t_finall <= t_inicio :
                print("tiempo de finalizacion debe ser mayor al de inicio")
            else:
                self.t_inicial  = t_inicio
                self.t_final    = t_finall
                break

class Solucion:
    def __init__(self,sistema):
        self.metodo   = "RK23"
        self.n_puntos = None 
        self.sistema  = sistema

    def add_puntos(self):
        puntos = leer_entero("ingrese el numero de puntos de la simulacion :",False)
        self.n_puntos= puntos

    def calcular(self):
        tiempos = np.linspace(self.sistema.t_inicial, self.sistema.t_final , self.n_puntos)
        solucion =solve_ivp(
            self.sistema.ecuacion,
            [self.sistema.t_inicial  , self.sistema.t_final], 
            self.sistema.valores_iniciales,
            t_eval=tiempos ,
            method=self.metodo
            )
        
        angulo = solucion.y[0]
        longitud = self.sistema.longitud
        pos_y =  -longitud*np.cos(angulo)
        pos_x =  longitud*np.sin(angulo)
        return solucion.t , pos_x , pos_y
    

class Visualizacion:
    def __init__(self, pos_x , pos_y ,tiempo,escala):
        self.tiempo = tiempo
        self.pos_x= pos_x
        self.pos_y = pos_y

        self.figura , self.ejes = plt.subplots()

        self.ejes.set_xlim(-1.2*escala, 1.2*escala)
        self.ejes.set_ylim(-1.2*escala, 1.2*escala)

        self.ejes.set_aspect('equal')

        self.linea ,= self.ejes.plot([],[], 'o-' ,lw =2) 
        self.conteo_tiempo = self.ejes.text(0.05, 0.09, '', transform = self.ejes.transAxes) 

    def reinicio(self):
        self.linea.set_data([], [])
        self.conteo_tiempo.set_text('')
        return self.linea,  self.conteo_tiempo
    
    def actualizar(self,frame):
        pos_x = self.pos_x[frame]
        pos_y = self.pos_y[frame]
        
        self.linea.set_data([0, pos_x], [0, pos_y])

        self.conteo_tiempo.set_text(f'Tiempo = {self.tiempo[frame]:.2f} s')

        return self.linea,  self.conteo_tiempo

    def animar(self, intervalo=30):
        self.animacion = FuncAnimation(
            self.figura ,
            self.actualizar ,
            frames = len(self.tiempo)  ,
            init_func= self.reinicio ,
            blit = True ,
            interval = intervalo
        )
        plt.show()
        

    

        
        


         



        
                




        
        

