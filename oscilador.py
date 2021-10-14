import pymunk
import pymunk.pygame_util
import pygame
from pygame.locals import *

import math

def position(y0,omega,v0):
    y=y0*math.cos(omega*t)+v0/omega*math.sin(omega*t)

pygame.init()

display = pygame.display.set_mode((800,800))
clock = pygame.time.Clock()
space = pymunk.Space()
FPS = 80

space = pymunk.Space()
space.gravity = 0, -9.81

b0 = space.static_body
p0 = 100, 20

body = pymunk.Body(mass=0.5, moment=1)
body.position = (100, 100)
circle = pymunk.Circle(body, radius=20)

joint = pymunk.constraints.DampedSpring(b0, body, p0, (0, 0), 110, 10, 0)
space.add(body, circle, joint)

# mass = pymunk.Body()
# mass.position = 300, 300
# square = pymunk.Circle(mass, 10)
# square.density = 1
# space.add(mass, square)

def spring(xo,yo,xf,yf,width,points):
    cicle=(-1,0,1)
    j=0
    spr=[(xo,yo)]
    for i in range(points):
        if j>=3:
            j=0
        spr.append((int(xo+width*cicle[j]),int(yo+(i+1)/points*(yf-yo))))
        j+=1
    return spr

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
        x, y = body.position
        pygame.draw.line(display,(255,255,255),(50,20),(150,20),width=1)
        pygame.draw.lines(display,(255,255,255),False,spring(100,20,int(x),int(y),10,17))
        pygame.draw.circle(display,(255,255,255),(int(x),int(y)),10)
        
        
        pygame.display.update()
        space.step(1/FPS)
        clock.tick(FPS)
        #pygame.display.set_caption(coordinates)


game()
pygame.quit()