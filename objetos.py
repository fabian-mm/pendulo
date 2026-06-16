import numpy as np
from scipy.integrate import solve_ivp
from scipy.interpolate import interp1d
import matplotlib.pyplot as plt
import time
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
        
        fps =60
        duracion = self.sistema.t_final - self.sistema.t_inicial
        t_anim = np.linspace(self.sistema.t_inicial, self.sistema.t_final, int(duracion * fps))
        
        interp = interp1d(solucion.t, solucion.y[0])
        angulo_anim = interp(t_anim)

        
        longitud = self.sistema.longitud
        pos_y =  -longitud*np.cos(angulo_anim)
        pos_x =  longitud*np.sin(angulo_anim)
        return t_anim , pos_x , pos_y
    

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

        
    def actualizar(self, frame):
        import time
        if not hasattr(self, 't_inicio_real') or self.t_inicio_real is None:
            self.t_inicio_real = time.time()

        t_transcurrido = time.time() - self.t_inicio_real
        t_sim = self.tiempo[0] + t_transcurrido

        if t_sim >= self.tiempo[-1]:
            idx = len(self.tiempo) - 1
        else:
            idx = np.searchsorted(self.tiempo, t_sim)
            idx = min(idx, len(self.tiempo) - 1)

        self.linea.set_data([0, self.pos_x[idx]], [0, self.pos_y[idx]])
        self.conteo_tiempo.set_text(f'Tiempo = {self.tiempo[idx]:.2f} s')
        return self.linea, self.conteo_tiempo

    def reinicio(self):
        self.t_inicio_real = None
        self.linea.set_data([], [])
        self.conteo_tiempo.set_text('')
        return self.linea, self.conteo_tiempo

    def animar(self):
        self.animacion = FuncAnimation(
            self.figura,
            self.actualizar,
            frames=len(self.tiempo),
            init_func=self.reinicio,
            blit=True,
            interval=1000/60
        )
        plt.show()
        

            
            


            



        
                




        
        

