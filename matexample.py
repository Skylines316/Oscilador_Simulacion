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

# formateo de los ejes para que todo se vea mas bonito


def format_axes(fig):
    for i, ax in enumerate(fig.axes):
        #ax.text(0.5, 0.5, "ax%d" % (i+1), va="center", ha="center")
        ax.tick_params(labelbottom=False, labelleft=True)
        if ax==pos_ax or ax==vel_ax:
            #para ponerle la mallita
            ax.grid(True)
            if ax==vel_ax:
                ax.set_xlim([0, 10])
                ax.set_ylim([-23, 23])
            else:#para poner los limites
                ax.set_xlim([0, 10])
                ax.set_ylim([-7, 7])


# definiendo la variable dependiente y su dominio
t = np.linspace(0, 10, 200)

# valores inciales de las constantes
initial_position = 0
initial_velocity = 0

# Creando la figura
fig = plt.figure(constrained_layout=True)

'''
poniendo cada plot en un Grid o malla, y es de la siguiente manera
gs[pos_x:posy,filas:columnas] o algo asi, sale probando xd
'''
gs = GridSpec(2, 2, figure=fig)
ax1 = fig.add_subplot(gs[0:2, 0:1])
pos_ax = fig.add_subplot(gs[0, 1:])
vel_ax = fig.add_subplot(gs[1, 1:])


# ingreso de las constantes, por ahora mediante la terminal
# k = float(input("Ingrese el valor de la constante de elasticidad: "))
# m = float(input("Ingrese el valor de la masa: "))
#o talvez es mejor solo manejar la constante w
w=float(input("Ingrese el valor de la frecuencia: "))


# yo=float(input("Ingrese la posición inicial: "))
# vo=float(input("Ingrese la velocidad inicial: "))

#w = (k/m)**(0.5)


pos_ax.plot(t, position_plot(t, initial_position, initial_velocity, w))
vel_ax.plot(t, velocity_plot(t, initial_position, initial_velocity, w))

# adjust the main plot to make room for the sliders
#plt.subplots_adjust(left=0.25, bottom=0.25)
axcolor = 'lightgoldenrodyellow'

#slider posicion
axpos = plt.axes([0.25, 0.1, 0.03, 0.65], facecolor=axcolor)
pos_slider = Slider(
    ax=axpos,
    label='Position [cm]',
    valmin=-5,
    valmax=5,
    valinit=initial_position,
    orientation="vertical"
)

#slider velocidad
axvel = plt.axes([0.1, 0.25, 0.0225, 0.63], facecolor=axcolor)
vel_slider = Slider(
    ax=axvel,
    label="Velocity [cm/s]",
    valmin=-5,
    valmax=5,
    valinit=initial_velocity,
    orientation="vertical"
)

#funcion que actualiza los datos y por consiguiente la gráfica
def update_graphs(val):
    pos_ax.clear()
    vel_ax.clear()
    pos_ax.plot(t, position_plot(t, pos_slider.val, vel_slider.val, w))
    vel_ax.plot(t, velocity_plot(t, pos_slider.val, vel_slider.val, w))
    format_axes(fig)
    fig.canvas.draw_idle()


#registro de los cambios en los sliders
pos_slider.on_changed(update_graphs)
vel_slider.on_changed(update_graphs)

fig.suptitle("GridSpec")
format_axes(fig)

plt.show()
