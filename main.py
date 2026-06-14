from objetos import Pendulo ,Solucion,Visualizacion


pen= Pendulo()


pen.add_l()
pen.add_tiempo()
pen.add_val_iniciales()

sol = Solucion(pen)

sol.add_puntos()

tiempo , xval , yval  =sol.calcular()

animacion = Visualizacion(xval , yval , tiempo,pen.longitud)

animacion.animar()


