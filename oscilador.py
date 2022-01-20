# import matplotlib.pyplot as plt
# from matplotlib.gridspec import GridSpec
# from matplotlib.widgets import Slider, Button
# import matplotlib.animation as animation
# from matplotlib.animation import FuncAnimation

import pygame
from pygame.locals import *

import pymunk
import pymunk.pygame_util

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

# definiendo la variable dependiente y su dominio
t = np.linspace(0, 10, 400)

# valores inciales de las constantes
initial_position = 0.5
initial_velocity = 1
initial_frequency = 6

# # Creando la figura
# fig = plt.figure(constrained_layout=False)

# '''
# poniendo cada plot en un Grid o malla, y es de la siguiente manera
# gs[pos_x:posy,filas:columnas] o algo asi, sale probando xd
# '''
# gs = GridSpec(2, 2, figure=fig)
# graph = fig.add_subplot(gs[0:2, 0:1])
# pos_ax = fig.add_subplot(gs[0, 1:])
# vel_ax = fig.add_subplot(gs[1, 1:])


# '''
# Grafico del resorte con la masa y descripciones en los graficos
# '''
# #grafico de recta
# ancho_de_soporte=np.linspace(2,8,3)
# recta, = graph.plot(ancho_de_soporte, recta(np.ones(len(ancho_de_soporte)),16), color='black')

# #grafico de resorte
# x, y = spring(5,16,5,initial_position,0.3,50)
# resorte, = graph.plot(x,y, color='black')

# #grafico de la masa
# masa, = graph.plot(5,initial_position,marker="o", markersize=15, color='black')
# masa_pos, = pos_ax.plot(0, initial_position,marker="o", markersize=6, color='red')
# masa_vel, = vel_ax.plot(0, initial_velocity,marker="o", markersize=6, color='red')

# '''
# grafico de la posicion vs la velocidad
# '''
# pos, = pos_ax.plot(t, position_plot(t, initial_position, initial_velocity, initial_frequency))
# vel, = vel_ax.plot(t, velocity_plot(t, initial_position, initial_velocity, initial_frequency))

# # adjust the main plot to make room for the sliders
# plt.subplots_adjust(left=0.01, right=0.99, bottom=0.03, top=0.94, wspace=0.4)
# axcolor = 'lightgoldenrodyellow'

# '''
# animacion
# '''
# # Animation controls
# is_manual = False # True if user has taken control of the animation
# interval = 100 # ms, time between animation frames
# loop_len = 1.0 # seconds per loop
# scale = interval / 1000 / loop_len
# # ani = animation.FuncAnimation(fig, run, position_plot(t,2,1,6))

# #slider posicion
# axpos = plt.axes([0.54, 0.05, 0.012, 0.85], facecolor=axcolor)
# pos_slider = Slider(
#     ax=axpos,
#     label='Pos [cm]',
#     valmin=-5,
#     valmax=5,
#     valinit=initial_position,
#     orientation="vertical"
# )

# #slider velocidad
# axvel = plt.axes([0.49, 0.05, 0.012, 0.85], facecolor=axcolor)
# vel_slider = Slider(
#     ax=axvel,
#     label="Vel [cm/s]",
#     valmin=-5,
#     valmax=5,
#     valinit=initial_velocity,
#     orientation="vertical"
# )

# #slider frecuencia
# axfeq = plt.axes([0.44, 0.05, 0.012, 0.85], facecolor=axcolor)
# feq_slider = Slider(
#     ax=axfeq,
#     label="Freq [$s^{-1}$]",
#     valmin=1,
#     valmax=10,
#     valinit=initial_frequency,
#     orientation="vertical"
# )

# def animation(t, initial_position, initial_velocity, frecuency):
#     pos = initial_position*np.cos(frecuency*t)+initial_velocity/frecuency*np.sin(frecuency*t)
#     vel = -initial_position*frecuency*np.sin(frecuency*t)+initial_velocity*np.cos(frecuency*t)
#     masa.set_ydata(pos)
#     masa_pos.set_data(t,pos)
#     masa_vel.set_data(t,vel)
#     x, y = spring(5,16,5,pos,0.3,50)
#     resorte.set_data(x, y)

# #funcion que actualiza los datos y por consiguiente la gráfica
# def update_graphs(val):
#     #Graficar en esos ejes
#     pos.set_data(t, position_plot(t, pos_slider.val, vel_slider.val, feq_slider.val))
#     vel.set_data(t, velocity_plot(t, pos_slider.val, vel_slider.val, feq_slider.val))
#     #grafico de resorte
#     x, y = spring(5,16,5,pos_slider.val,0.3,50)
#     resorte.set_data(x, y)
#     #grafico de la masa
#     masa.set_ydata(pos_slider.val)
#     masa_pos.set_data(0, pos_slider.val)
#     masa_vel.set_data(0, vel_slider.val)
#     format_axes(fig)
#     fig.canvas.draw_idle()
#     return pos, vel, spring, masa,

# def animate_button(self):
#     initial_position = pos_slider.val
#     initial_velocity = vel_slider.val
#     initial_frequency = feq_slider.val
#     a = FuncAnimation(fig, animation , fargs=(initial_position, initial_velocity, initial_frequency), frames=t,interval=50, repeat=True)
#     fig.canvas.draw()


# #registro de los cambios en los sliders
# pos_slider.on_changed(update_graphs)
# vel_slider.on_changed(update_graphs)
# feq_slider.on_changed(update_graphs)

# #animation button
# axnext = fig.add_axes([0.03, 0.04,0.1, 0.075])
# bnext = Button(axnext, 'Correr Simulacion!')
# bnext.on_clicked(animate_button)

# fig.suptitle("Oscilador Armónico Simple")
# format_axes(fig)

# plt.show()
pygame.init()

display = pygame.display.set_mode((1120,630))
clock = pygame.time.Clock()
space = pymunk.Space()
FPS = 80

def game():
    while True:
        for event in pygame.event.get():
            if (
                event.type == pygame.QUIT
                or event.type == pygame.KEYDOWN
                and event.key == pygame.K_ESCAPE
            ):
                exit()
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_p:
                pygame.image.save(screen, "planet.png")
            if event.type == pygame.MOUSEBUTTONDOWN:
                coordinates = pygame.mouse.get_pos()
                print(coordinates)
        display.fill((0,0,0))
        # x, y = body.position
        # print(x,y)
        # pygame.draw.line(display,(255,255,255),(50,20),(150,20),width=1)
        # pygame.draw.lines(display,(255,255,255),False,spring(100,20,int(x),int(y),10,17))
        # pygame.draw.circle(display,(255,255,255),(int(x),int(y)),10)

        
        pygame.display.update()
        space.step(1/FPS)
        clock.tick(FPS)
        #pygame.display.set_caption(coordinates)


game()
pygame.quit()