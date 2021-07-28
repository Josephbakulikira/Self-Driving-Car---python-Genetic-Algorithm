import os
import pygame
from math import sin, radians, degrees, copysign
from pygame.math import Vector2
from car import Car
from constants import *

pygame.init()
pygame.display.set_caption(" Self Driving Car")
screen = pygame.display.set_mode((Width, Height))
clock = pygame.time.Clock()
fps = 60

# load Assets
current_directory = os.path.dirname(os.path.abspath(__file__))
carImage_path = os.path.join(current_directory, "./Assets/car1.png")
car_sprite = pygame.image.load(carImage_path)
sprite = pygame.transform.scale(car_sprite, (128, 64))

car = Car(30, 15)
car.sprite = sprite

run = True
while run:
    screen.fill(Black)
    dt = clock.get_time()/1000
    # HANDLE EVENT
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_ESCAPE:
                run = False
    keys = pygame.key.get_pressed()

    if keys[pygame.K_UP] or keys[pygame.K_w]:
        car.Forward(dt)
    elif keys[pygame.K_DOWN] or keys[pygame.K_s]:
        car.Backward(dt)
    elif keys[pygame.K_SPACE]:
        car.Brake(dt)
    else:
        car.fixed(dt)
    car.constrainAcceleration()

    if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
        car.Right(dt)
    elif keys[pygame.K_LEFT] or keys[pygame.K_a]:
        car.Left(dt)
    else:
        car.resetSteering()
    car.constrainSteering()

    car.update(dt)
    car.Draw(screen)

    pygame.display.flip()
    clock.tick(fps)

pygame.quit()
