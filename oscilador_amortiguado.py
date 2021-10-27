import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec
from matplotlib.widgets import Slider, Button
import matplotlib.animation as animation
from matplotlib.animation import FuncAnimation

import pymunk

import numpy as np
import math as ma

#funcion recta de soporte del resorte
def recta(largo ,alto):
    return largo*alto

#funcion que retorna un resorte dinamico
def spring(xo,yo,xf,yf,width,points):
    cicle=(-1,1)
    j=0
    i=1
    total_points=points+4
    x=np.array([xo,xo])
    y=np.array([yo,yo+i/total_points*(yf-yo)])
    while i<total_points:
        if total_points-i<=2:
            x=np.append(x,xf)
        else:
            x=np.append(x,xo+(i%2*2-1)*width)
        y=np.append(y,yo+i/total_points*(yf-yo))
        i+=1
    return x, y

# formateo de los ejes para que todo se vea mas bonito
def format_axes(fig):
    for i, ax in enumerate(fig.axes):
        #ax.text(0.5, 0.5, "ax%d" % (i+1), va="center", ha="center")
        graph.tick_params(labelbottom=False, labelleft=False)
        graph.set_xlim([0, 10])
        graph.set_ylim([-10, 17])
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


'''
funciones para la animacion
'''
def position(t, frecuency):
    return initial_position*np.cos(frecuency*t)+initial_velocity/frecuency*np.sin(frecuency*t)

# valores inciales de las constantes
initial_position = 2
initial_velocity = 0
initial_frequency = 6

# definiendo la variable dependiente y su dominio
time = np.array([0])

#Creando el espacio y las particulas con pymunk
space = pymunk.Space()
# space.gravity = 0, -9.81
b0 = space.static_body
body = pymunk.Body(mass=5, moment=1)
body.position = (5, initial_position)
body.velocity = (0, initial_velocity)
FPS = 10               # Funciona diferente, a menos FPS mas rapida es la animacion

joint = pymunk.constraints.DampedSpring(b0, body, (5,16), (0, 0), 16, 20, 0)
space.add(body, joint)

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


'''
Grafico del resorte con la masa y descripciones en los graficos
'''
#grafico de recta
ancho_de_soporte=np.linspace(2,8,3)
recta, = graph.plot(ancho_de_soporte, recta(np.ones(len(ancho_de_soporte)),16), color='black')

#grafico de resorte
x, y = spring(5,16,5,initial_position,0.3,50)
resorte, = graph.plot(x,y, color='black')

#grafico de la masa
masa, = graph.plot(5,initial_position,marker="o", markersize=15, color='black')
masa_pos, = pos_ax.plot(0, initial_position,marker="o", markersize=6, color='red')
masa_vel, = vel_ax.plot(0, initial_velocity,marker="o", markersize=6, color='red')

'''
grafico de la posicion vs la velocidad
'''
pos_graf = np.array([initial_position])
vel_graf = np.array([initial_velocity])
pos, = pos_ax.plot(time, pos_graf)
vel, = vel_ax.plot(time, vel_graf)

# adjust the main plot to make room for the sliders
plt.subplots_adjust(left=0.01, right=0.99, bottom=0.03, top=0.94, wspace=0.4)
axcolor = 'lightgoldenrodyellow'

'''
animacion
'''
# Animation controls
is_manual = False # True if user has taken control of the animation
interval = 100 # ms, time between animation frames
loop_len = 1.0 # seconds per loop
scale = interval / 1000 / loop_len
# ani = animation.FuncAnimation(fig, run, position_plot(t,2,1,6))

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

def animation(t):
    global time, pos_graf, vel_graf
    x_pos, y_pos = body.position
    x_vel, y_vel = body.velocity
    time = np.append(time, t)
    pos_graf = np.append(pos_graf, y_pos)
    vel_graf = np.append(vel_graf, y_vel)
    pos_ax.plot(time, pos_graf, color='blue')
    vel_ax.plot(time, vel_graf, color='blue')
    masa.set_ydata(y_pos)
    masa_pos.set_data(t,y_pos)
    masa_vel.set_data(t,y_vel)
    x, y = spring(5,16,5,y_pos,0.3,50)
    resorte.set_data(x, y)
    space.step(1/FPS)

#funcion que actualiza los datos y por consiguiente la gráfica
def update_graphs(val):
    pos.set_ydata(np.array([pos_slider.val]))
    vel.set_ydata(np.array([vel_slider.val]))
    x, y = spring(5,16,5,pos_slider.val,0.3,50)
    resorte.set_data(x, y)
    #grafico de la masa
    masa.set_ydata(pos_slider.val)
    masa_pos.set_ydata(pos_slider.val)
    masa_vel.set_ydata(vel_slider.val)
    body.position = (5, pos_slider.val)
    body.velocity = (0, vel_slider.val)
    format_axes(fig)
    fig.canvas.draw_idle()
    return pos, vel, spring, masa, 

anim_running = False
def onClick(event):
    global a
    global anim_running
    if anim_running:
        a.event_source.stop()
        anim_running = False
    else:
        a.event_source.start()
        anim_running = True

def restart(event):
    a.frame_seq = a.new_frame_seq()
    init_anim()
    a.event_source.start()

def init_anim():
    pos_ax.clear()
    vel_ax.clear()
    global time, pos_graf, vel_graf, masa_pos, masa_vel
    time = np.array([0])
    body.position = (5, pos_slider.val)
    body.velocity = (0, vel_slider.val)
    pos_graf = np.array([pos_slider.val])
    vel_graf = np.array([vel_slider.val])
    masa_pos, = pos_ax.plot(0, pos_slider.val,marker="o", markersize=6, color='red')
    masa_vel, = vel_ax.plot(0, vel_slider.val,marker="o", markersize=6, color='red')
    format_axes(fig)

#registro de los cambios en los sliders
pos_slider.on_changed(update_graphs)
vel_slider.on_changed(update_graphs)
feq_slider.on_changed(update_graphs)

#play pause button
axplay = fig.add_axes([0.03, 0.04,0.05, 0.03])
bnplay = Button(axplay, 'Play / Pause')

#restart button
axres = fig.add_axes([0.1, 0.04,0.03, 0.03])
bnres = Button(axres, 'Restart')

a = FuncAnimation(fig, animation , frames=np.arange(0,10,1/FPS),init_func=init_anim, interval=1, repeat=True)
bnplay.on_clicked(onClick)
bnres.on_clicked(restart)

#fig.canvas.mpl_connect('button_press_event', onClick)

fig.suptitle("Oscilador Armónico Simple")
format_axes(fig)

plt.show()
