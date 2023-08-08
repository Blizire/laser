import requests
import pygame
from pygame.locals import *

ip = 'grugserve.com'
port = '5050'
xpos = 0
ypos = 0


#requests.get(f'http://{ip}:{port}/x/90')
#requests.get(f'http://{ip}:{port}/y/90')
#template = f'http://{ip}:{port}/{servo}/{pos}'

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 800
WHITE = (255, 255, 255)
RED   = (255,   0,   0)
FPS = 30

def linear_interpolate(old_value):
    old_min = 0
    old_max = 800
    new_min = 0
    new_max = 180
    new_value = ((old_value - old_min) / (old_max - old_min)) * (new_max - new_min) + new_min
    return new_value

def send_command(x, y):
    x = linear_interpolate(x)
    y = linear_interpolate(y)

    # the x servo is backwards so we have to do this
    #x = 180-x

    requests.get(f'http://{ip}:{port}/x/{x}')
    requests.get(f'http://{ip}:{port}/y/{y}')

pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Tracking System")
rectangle = pygame.rect.Rect(200, 200, 17, 17)
rectangle_draging = False
clock = pygame.time.Clock()
running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:            
                if rectangle.collidepoint(event.pos):
                    rectangle_draging = True
                    mouse_x, mouse_y = event.pos
                    offset_x = rectangle.x - mouse_x
                    offset_y = rectangle.y - mouse_y

        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:            
                rectangle_draging = False

        elif event.type == pygame.MOUSEMOTION:
            if rectangle_draging:
                mouse_x, mouse_y = event.pos
                rectangle.x = mouse_x + offset_x
                rectangle.y = mouse_y + offset_y
        
        send_command(rectangle.x, rectangle.y)

    screen.fill(WHITE)
    pygame.draw.rect(screen, RED, rectangle)
    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()