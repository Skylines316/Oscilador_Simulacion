# import matplotlib.pyplot as plt
# from matplotlib.gridspec import GridSpec
# from matplotlib.widgets import Slider, Button
# import matplotlib.animation as animation
# from matplotlib.animation import FuncAnimation
import random

import pygame
from pygame.locals import *
import sys

import pymunk

import numpy as np
import math as ma

#* Limpiar el codigo
#? agregar un setter a la spring para cambiar su longitud
#! revisar errores

#funcion recta de soporte del resorte
def recta(largo ,alto):
    return largo*alto

#funcion que retorna un resorte dinamico
def spring(xo,yo,xf,yf,width,points):
    cicle=(-1,1)
    j=0
    i=1
    total_points=points+4
    r=[(xo,yo),(xo,int(yo+i/total_points*(yf-yo)))]
    # x=np.array([xo,xo])
    # y=np.array([yo,int(yo+i/total_points*(yf-yo))])
    while i<=total_points:
        if total_points-i<=2:
            r.append((int(xf),int(yo+i/total_points*(yf-yo))))
            # x=np.append(x,int(xf))
        else:
            r.append((int(xo+(i%2*2-1)*width),int(yo+i/total_points*(yf-yo))))
            # x=np.append(x,int(xo+(i%2*2-1)*width))
            # y=np.append(y,int(yo+i/total_points*(yf-yo)))
        i+=1
    # return x, y
    return r

# formateo de los ejes para que todo se vea mas bonito
# def format_axes(fig):
#     for i, ax in enumerate(fig.axes):
#         #ax.text(0.5, 0.5, "ax%d" % (i+1), va="center", ha="center")
#         graph.tick_params(labelbottom=False, labelleft=False)
#         graph.set_xlim([0, 10])
#         graph.set_ylim([-10, 17])
#         if ax==pos_ax or ax==vel_ax:
#             ax.tick_params(labelbottom=False, labelleft=True)
#             #para ponerle la mallita
#             ax.grid(True)
#             if ax==vel_ax:
#                 # ax.suptitle("Velocidad")
#                 ax.set_xlim([0, 20])
#                 ax.set_ylim([-23, 23])
#             else:#para poner los limites
#                 # ax.suptitle("Posicion")
#                 ax.set_xlim([0, 20])
#                 ax.set_ylim([-7, 7])



'''
funciones para la animacion
'''
def position_at_axes(x):
    x1=int((x-36)/(594-36)*(278-36))+36
    return x1

def velocity_at_axes(y):
    y1=int((y+400)/(800)*(592-350))+350
    return y1

pygame.init()

# valores inciales de las constantes
initial_position = 340
initial_velocity = -120
initial_stiffness = 20
initial_mass = 5
initial_damping = 0

# definiendo la variable dependiente y su dominio
time = np.array([0])

#Creando el espacio y las particulas con pymunk
space = pymunk.Space()
# space.gravity = 0, -9.81
b0 = space.static_body
b0.position = (185, 36)
body = pymunk.Body(mass=initial_mass, moment=1)
body.position = (185, initial_position)
body.velocity = (0, initial_velocity)
# FPS = 10               # Funciona diferente, a menos FPS mas rapida es la animacion

joint = pymunk.constraints.DampedSpring(b0, body, (0,0), (0, 0), 279, initial_stiffness, initial_damping)
space.add(body, joint)

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
# pos_graf = np.array([initial_position])
# vel_graf = np.array([initial_velocity])
# pos, = pos_ax.plot(time, pos_graf)
# vel, = vel_ax.plot(time, vel_graf)

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
# axpos = plt.axes([0.54, 0.52, 0.012, 0.4], facecolor=axcolor)
# pos_slider = Slider(
#     ax=axpos,
#     label='Pos [cm]',
#     valmin=-5,
#     valmax=5,
#     valinit=initial_position,
#     orientation="vertical"
# )

# #slider velocidad
# axvel = plt.axes([0.49, 0.52, 0.012, 0.4], facecolor=axcolor)
# vel_slider = Slider(
#     ax=axvel,
#     label="Vel [cm/s]",
#     valmin=-5,
#     valmax=5,
#     valinit=initial_velocity,
#     orientation="vertical"
# )

# #slider stiffness
# axstiff = plt.axes([0.44, 0.52, 0.012, 0.4], facecolor=axcolor)
# stiff_slider = Slider(
#     ax=axstiff,
#     label="Stiff [$s^{-1}$]",
#     valmin=1,
#     valmax=30,
#     valinit=initial_stiffness,
#     orientation="vertical"
# )

# #slider masa
# axmas = plt.axes([0.44, 0.04, 0.012, 0.4], facecolor=axcolor)
# mass_slider = Slider(
#     ax=axmas,
#     label="mas[kg]",
#     valmin=1,
#     valmax=10,
#     valinit=initial_mass,
#     orientation="vertical"
# )

# #slider damping
# axdamp = plt.axes([0.49, 0.04, 0.012, 0.4], facecolor=axcolor)
# damp_slider = Slider(
#     ax=axdamp,
#     label="dump[$s^{-1}$]",
#     valmin=0,
#     valmax=10,
#     valinit=initial_damping,
#     orientation="vertical"
# )


# def animation(t):
#     global time, pos_graf, vel_graf
#     x_pos, y_pos = body.position
#     x_vel, y_vel = body.velocity
#     time = np.append(time, t)
#     pos_graf = np.append(pos_graf, y_pos)
#     vel_graf = np.append(vel_graf, y_vel)
#     pos_ax.plot(time, pos_graf, color='blue')
#     vel_ax.plot(time, vel_graf, color='blue')
#     masa.set_ydata(y_pos)
#     masa_pos.set_data(t,y_pos)
#     masa_vel.set_data(t,y_vel)
#     x, y = spring(5,16,5,y_pos,0.3,50)
#     resorte.set_data(x, y)
#     space.step(1/FPS)

# #funcion que actualiza los datos y por consiguiente la gráfica
# def update_graphs(val):
#     pos.set_ydata(np.array([pos_slider.val]))
#     vel.set_ydata(np.array([vel_slider.val]))
#     x, y = spring(5,16,5,pos_slider.val,0.3,50)
#     resorte.set_data(x, y)
#     #grafico de la masa
#     masa.set_ydata(pos_slider.val)
#     masa_pos.set_ydata(pos_slider.val)
#     masa_vel.set_ydata(vel_slider.val)
#     body.position = (5, pos_slider.val)
#     body.velocity = (0, vel_slider.val)
#     body.mass = mass_slider.val
#     joint._set_damping(damp_slider.val)
#     joint._set_stiffness(stiff_slider.val)
#     format_axes(fig)
#     fig.canvas.draw_idle()
#     restart(val)
#     return pos, vel, spring, masa, 

# anim_running = False
# def onClick(event):
#     global a
#     global anim_running
#     if anim_running:
#         a.event_source.stop()
#         anim_running = False
#     else:
#         a.event_source.start()
#         anim_running = True

# def restart(event):
#     a.frame_seq = a.new_frame_seq()
#     init_anim()
#     a.event_source.start()

# def init_anim():
#     pos_ax.clear()
#     vel_ax.clear()
#     global time, pos_graf, vel_graf, masa_pos, masa_vel
#     time = np.array([0])
#     body.position = (5, pos_slider.val)
#     body.velocity = (0, vel_slider.val)
#     body.mass = mass_slider.val
#     pos_graf = np.array([pos_slider.val])
#     vel_graf = np.array([vel_slider.val])
#     masa_pos, = pos_ax.plot(0, pos_slider.val,marker="o", markersize=6, color='red')
#     masa_vel, = vel_ax.plot(0, vel_slider.val,marker="o", markersize=6, color='red')
#     format_axes(fig)

# #registro de los cambios en los sliders
# pos_slider.on_changed(update_graphs)
# vel_slider.on_changed(update_graphs)
# stiff_slider.on_changed(update_graphs)
# mass_slider.on_changed(update_graphs)
# damp_slider.on_changed(update_graphs)


# #play pause button
# axplay = fig.add_axes([0.03, 0.04,0.05, 0.03])
# bnplay = Button(axplay, 'Play / Pause')

# #restart button
# axres = fig.add_axes([0.1, 0.04,0.03, 0.03])
# bnres = Button(axres, 'Restart')

# a = FuncAnimation(fig, animation , frames=np.arange(0,20,1/FPS),init_func=init_anim, interval=1, repeat=True)
# bnplay.on_clicked(onClick)
# bnres.on_clicked(restart)

# #fig.canvas.mpl_connect('button_press_event', onClick)

# fig.suptitle("Oscilador Armónico Simple")
# format_axes(fig)

# plt.show()
pygame.display.set_caption('Oscilador Armónico Amortiguado')

programIcon = pygame.image.load('logo-unsaac-nav.png')

pygame.display.set_icon(programIcon)

clock = pygame.time.Clock()
FPS = 80

font1 = pygame.font.SysFont("firacode", 30)
font2 = pygame.font.SysFont("firacode", 20)
font3 = pygame.font.SysFont("arial",20)

textr = font1.render('r(m)', False, '#000000')
textv = font1.render('v(m/s)', False, '#000000')
textt = font1.render('t(s)', False, '#000000')

textro = font2.render(f'r\N{SUBSCRIPT ZERO}', False, '#000000')
textvo = font2.render(f'v\N{SUBSCRIPT ZERO}', False, '#000000')
textgam = font3.render(f'\N{LATIN CAPITAL LETTER GAMMA}', False, '#000000')

textro_leyenda = font2.render(f'r\N{SUBSCRIPT ZERO}: Posición Inicial', False, '#000000')
textvo_leyenda = font2.render(f'v\N{SUBSCRIPT ZERO}: Velocidad Inicial', False, '#000000')
textgam_leyenda = font3.render(f'\N{LATIN CAPITAL LETTER GAMMA}: Amortiguamiento', False, '#000000')

def game():
    time=0
    position=[]
    velocity=[]
    firstLoop = True
    global screenColor, mouse, click
    screenColor= (255,255,255)
    
    '''Slider'''
    display = pygame.display.set_mode((1120,630))
    screen = display
    # pygame.display.update(pygame.Rect(0,0,1120,630))
    
    def slider(sx,sy,action,width,height,buttonColor,sliderColor,buttonBorderThickness,sliderBorderThickness,buttonHeight,sliderBarWidth,maxValue, sliderpos):
        pygame.draw.rect(screen,screenColor,(sx,sy,width,height))  #base del slider
        pygame.draw.rect(screen,sliderColor,(sx+width/2-sliderBarWidth/2,sy,sliderBarWidth,height)) # por donde se desliza el slider
        if mouse[0] > sx and mouse[0] < sx+width and mouse[1] > sy and mouse[1] < sy+height and click[0] == 1:
            mouseY = mouse[1] - sliderBarWidth/2
            if mouseY < sy:
                mouseY = sy
            elif mouseY > sy+height-buttonHeight:
                mouseY = sy+height-buttonHeight
            pygame.draw.rect(screen,buttonColor,(sx,mouseY,width,buttonHeight)) #slider en si mismo
            if buttonBorderThickness != 0:
                pygame.draw.rect(screen,(0,0,0),(sx,mouseY,width,buttonHeight),buttonBorderThickness) #borde del slider
            if sliderBorderThickness != 0:
                pygame.draw.rect(screen,(0,0,0),(sx+width/2-sliderBarWidth/2,sy,sliderBarWidth,height),sliderBorderThickness) #borde del slider
            pygame.display.update(pygame.Rect(sx,sy,width,height))
            
            sliderValue = (mouseY-sy)/((height-buttonHeight)/maxValue)
            
            # if action == "test1":
                
            #     print("test1:")
            #     print(sliderValue)
            # elif action == "test2":
            #     sliderValue = (mouseY-sy)/((height-buttonHeight)/maxValue)
            #     print("test2:")
            #     print(sliderValue)
            
        else:
            pygame.draw.rect(screen,screenColor,(sx,sy,width,height))
            pygame.draw.rect(screen,sliderColor,(sx+width/2-sliderBarWidth/2,sy,sliderBarWidth,height))
            pygame.draw.rect(screen,buttonColor,(sx,sy+sliderpos*((height-buttonHeight)/maxValue),width,buttonHeight))
            if buttonBorderThickness != 0:
                pygame.draw.rect(screen,(0,0,0),(sx,sy+sliderpos*((height-buttonHeight)/maxValue),width,buttonHeight),buttonBorderThickness)
            if sliderBorderThickness != 0:
                pygame.draw.rect(screen,(0,0,0),(sx,sy+height/2-sliderBarWidth/2,sliderBarWidth,height),sliderBorderThickness)
            pygame.display.update(pygame.Rect(sx,sy,width,height))
            sliderValue = sliderpos
        
        return sliderValue
    
    sliderpos = 70
    slidervel = 20
    # sliderk = 50
    sliderdump = 100
    
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
            # if event.type == pygame.MOUSEBUTTONDOWN:
            #     coordinates = pygame.mouse.get_pos()
            #     print(coordinates)
        x, y = body.position
        xv,yv = body.velocity
        display.fill((255,255,255))
        position.append((450+time,position_at_axes(y)))
        velocity.append((450+time,velocity_at_axes(yv)))

        '''Seccion texto'''
        display.blit(textr,(455,26))
        display.blit(textv,(455,340))
        display.blit(textt,(1040,160))
        display.blit(textt,(1040,474))
        
        display.blit(textro,(400,26))
        display.blit(textvo,(360,26))
        display.blit(textgam,(404,340))
        
        
        '''Leyenda'''
        display.blit(textro_leyenda,(20,500))
        display.blit(textvo_leyenda,(20,525))
        display.blit(textgam_leyenda,(24,560))
        
        # print(x,y)
        # print(spring(185, 36,int(x),int(y),10,17))
        
        '''Seccion de resorte'''
        pygame.draw.line(display,(0,0,0),(35,36),(335,36),width=1)
        pygame.draw.lines(display,(0,0,0),False,spring(185, 36,int(x),int(y),15,27))
        pygame.draw.circle(display,(0,0,0),(int(x),int(y)),10)

        '''Seccion de Posicion vs tiempo'''
        pygame.draw.line(display,(0,0,0),(450,157),(1085,157),width=2) #eje horizontal
        pygame.draw.line(display,(0,0,0),(450,36),(450,278),width=2) #eje vertical
        pygame.draw.circle(display,(255,0,0),(450+time,position_at_axes(y)),4)
        if time >0:
            pygame.draw.lines(display,(0,0,255),False,position,width=2)
        
        '''Seccion de velocidad vs tiempo'''
        pygame.draw.line(display,(0,0,0,),(450,471),(1085,471),width=2)
        pygame.draw.line(display,(0,0,0,),(450,350),(450,592),width=2)
        pygame.draw.circle(display,(255,0,0),(450+time,velocity_at_axes(yv)),4)
        if time >0:
            pygame.draw.lines(display,(0,0,255),False,velocity,width=2)
            
        '''Seccion controladores'''
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()

        
        sliderposition = sliderpos
        slidervelocity = slidervel
        # sliderstiffness = sliderk
        sliderdumping = sliderdump
        
        sliderpos = slider(400,56,"position",20,202,(255,255,255),(220,220,220),1,0,10,4,100, sliderposition)
        slidervel = slider(360,56,"velocity",20,202,(255,255,255),(220,220,220),1,0,10,4,100, slidervelocity)
        # sliderk = slider(360,370,"test1",20,202,(255,255,255),(220,220,220),1,0,10,4,100, sliderstiffness)
        sliderdump = slider(400,370,"amortiguamiento",20,202,(255,255,255),(220,220,220),1,0,10,4,100, sliderdumping)
        # slider(100,120,"test2",1000,50,(255,255,255),(220,220,220),1,0,25,10,100)
        if sliderposition != sliderpos :
            body.position = (x,sliderpos/100*200+200)
            # pygame.time.wait(500)

        if slidervelocity != slidervel:
            body.velocity = (0,slidervel/100*400-200)
            
        # if sliderstiffness != sliderk:
        #     joint.stiffness = (100-sliderstiffness)
            
        if sliderdumping != sliderdump:
            joint.damping = (100-sliderdump)/10
        # print(joint.damping)

            
        pygame.display.update()
        space.step(1/FPS)
        clock.tick(FPS)
        if time<=635:
            time +=1
        if time>635 :
            # time = 0
            position.pop(0)
            velocity.pop(0)
            position=list(map(lambda x: (x[0]-1,x[1]),position))
            velocity=list(map(lambda x: (x[0]-1,x[1]),velocity))
        #pygame.display.set_caption(coordinates)


game()
pygame.quit()