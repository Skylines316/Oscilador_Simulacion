import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec
from matplotlib.widgets import Slider, Button

import numpy as np
import math as ma

# definiendo la funcion de la posicion
def position_plot(t, initial_position, initial_velocity, frecuency):
    return initial_position*np.cos(frecuency*t)+initial_velocity/frecuency*np.sin(frecuency*t)

# definieno la funcion de la velocidad
def velocity_plot(t, initial_position, initial_velocity, frecuency):
    return -initial_position*frecuency*np.sin(frecuency*t)+initial_velocity*np.cos(frecuency*t)

#funcion recta de soporte del resorte
def recta(largo ,alto):
    return largo*alto

#funcion que retorna un resorte dinamico
def spring(xo,yo,xf,yf,width,points):
    cicle=(-1,0,1)
    j=0
    x=[xo]
    y=[yo]
    spr=[(xo,yo)]
    for i in range(points):
        if j>=3:
            j=0
        spr.append((int(xo+width*cicle[j]),int(yo+(i+1)/points*(yf-yo))))
        x.append(xo+width*cicle[j])
        y.append(yo+(i+1)/points*(yf-yo))
        j+=1
    return x, y

# formateo de los ejes para que todo se vea mas bonito
def format_axes(fig):
    for i, ax in enumerate(fig.axes):
        #ax.text(0.5, 0.5, "ax%d" % (i+1), va="center", ha="center")
        graph.tick_params(labelbottom=False, labelleft=False)
        graph.set_xlim([0, 10])
        graph.set_ylim([0, 14])
        if ax==pos_ax or ax==vel_ax:
            ax.tick_params(labelbottom=False, labelleft=True)
            #para ponerle la mallita
            ax.grid(True)
            if ax==vel_ax:
                # ax.suptitle("Velocidad")
                ax.set_xlim([0, 10])
                ax.set_ylim([-23, 23])
            else:#para poner los limites
                # ax.suptitle("Posicion")
                ax.set_xlim([0, 10])
                ax.set_ylim([-7, 7])


# definiendo la variable dependiente y su dominio
t = np.linspace(0, 10, 200)

# valores inciales de las constantes
initial_position = 2
initial_velocity = 1
initial_frequency = 6

# Creando la figura
fig = plt.figure(constrained_layout=False)

'''
poniendo cada plot en un Grid o malla, y es de la siguiente manera
gs[pos_x:posy,filas:columnas] o algo asi, sale probando xd
'''
gs = GridSpec(2, 2, figure=fig)
graph = fig.add_subplot(gs[0:2, 0:1])
pos_ax = fig.add_subplot(gs[0, 1:])
vel_ax = fig.add_subplot(gs[1, 1:])


# ingreso de las constantes, por ahora mediante la terminal
# k = float(input("Ingrese el valor de la constante de elasticidad: "))
# m = float(input("Ingrese el valor de la masa: "))
#o talvez es mejor solo manejar la constante w
#w=float(input("Ingrese el valor de la frecuencia: "))


# yo=float(input("Ingrese la posición inicial: "))
# vo=float(input("Ingrese la velocidad inicial: "))

#w = (k/m)**(0.5)

'''
Grafico del resorte con la masa
'''
#grafico de recta
ancho_de_soporte=np.linspace(2,8,3)
graph.plot(ancho_de_soporte, recta(np.ones(len(ancho_de_soporte)),12), color='black')

#grafico de resorte
x, y = spring(5,12,5,7,0.5,26)
graph.plot(x,y, color='black')

#grafico de la masa
masa = plt.Circle((5,7),0.3, color='black')
graph.add_patch(masa)

'''
grafico de la posicion vs la velocidad
'''
pos_ax.plot(t, position_plot(t, initial_position, initial_velocity, initial_frequency))
vel_ax.plot(t, velocity_plot(t, initial_position, initial_velocity, initial_frequency))

# adjust the main plot to make room for the sliders
plt.subplots_adjust(left=0.01, right=0.99, bottom=0.03, top=0.94, wspace=0.4)
axcolor = 'lightgoldenrodyellow'

#slider posicion
axpos = plt.axes([0.54, 0.05, 0.012, 0.85], facecolor=axcolor)
pos_slider = Slider(
    ax=axpos,
    label='Pos [cm]',
    valmin=-5,
    valmax=5,
    valinit=initial_position,
    orientation="vertical"
)

#slider velocidad
axvel = plt.axes([0.49, 0.05, 0.012, 0.85], facecolor=axcolor)
vel_slider = Slider(
    ax=axvel,
    label="Vel [cm/s]",
    valmin=-5,
    valmax=5,
    valinit=initial_velocity,
    orientation="vertical"
)

#slider frecuencia
axfeq = plt.axes([0.44, 0.05, 0.012, 0.85], facecolor=axcolor)
feq_slider = Slider(
    ax=axfeq,
    label="Freq [$s^{-1}$]",
    valmin=1,
    valmax=10,
    valinit=initial_frequency,
    orientation="vertical"
)

#funcion que actualiza los datos y por consiguiente la gráfica
def update_graphs(val):
    pos_ax.clear()
    vel_ax.clear()
    pos_ax.plot(t, position_plot(t, pos_slider.val, vel_slider.val, feq_slider.val))
    vel_ax.plot(t, velocity_plot(t, pos_slider.val, vel_slider.val, feq_slider.val))
    format_axes(fig)
    fig.canvas.draw_idle()


#registro de los cambios en los sliders
pos_slider.on_changed(update_graphs)
vel_slider.on_changed(update_graphs)
feq_slider.on_changed(update_graphs)

fig.suptitle("Oscilador Armónico Simple")
format_axes(fig)

plt.show()
