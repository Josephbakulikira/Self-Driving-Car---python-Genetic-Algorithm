import os
import pygame
import pickle

from point import Point, GetDistance
from spline import Spline
from math import sin, radians, degrees, copysign, sqrt
from pygame.math import Vector2
from car import Car
from constants import *

pygame.init()
pygame.display.set_caption(" Self Driving Car")
screen = pygame.display.set_mode((Width, Height))
clock = pygame.time.Clock()
fps = 60

track = Spline()
trackTopBound = Spline()
trackBottomBound = Spline()
trackTopBound.pointRadius = 1
trackBottomBound.pointRadius = 1

track.CreatePoints(N_POINTS, False)
trackBottomBound.CreatePoints(N_POINTS, False)
trackTopBound.CreatePoints(N_POINTS, False)

track.resolution = SPLINE_RESOLUTION
trackBottomBound.resolution = SPLINE_RESOLUTION
trackTopBound.resolution = SPLINE_RESOLUTION



# load Assets
current_directory = os.path.dirname(os.path.abspath(__file__))
carImage_path = os.path.join(current_directory, "./Assets/car.png")
car_sprite = pygame.image.load(carImage_path)
sprite = pygame.transform.scale(car_sprite, (128, 64))

car = Car(30, 15)
car.sprite = sprite

MouseClicked = False
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
        if event.type == pygame.MOUSEBUTTONDOWN:
            MouseClicked = True

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


    for i in range(N_POINTS ):
        p1 = track.GetSplinePoints(i * SPLINE_RESOLUTION, True)
        g1 = track.GetSplineGradient(i * SPLINE_RESOLUTION, True)
        glength = sqrt(g1[0] * g1[0] + g1[1] * g1[1])

        trackTopBound.points[i].x = p1[0] - TRACK_WIDTH * (-g1[1]/glength)
        trackTopBound.points[i].y = p1[1] - TRACK_WIDTH * (g1[0]/glength)

        trackBottomBound.points[i].x = p1[0] + TRACK_WIDTH * (-g1[1]/glength)
        trackBottomBound.points[i].y = p1[1] + TRACK_WIDTH * (g1[0]/glength)

    track.Draw(screen, MouseClicked)
    trackBottomBound.Draw(screen, False)
    trackTopBound.Draw(screen, False)

    car.update(dt)
    car.Draw(screen)

    pygame.display.flip()
    clock.tick(fps)

    MouseClicked = False
pygame.quit()
