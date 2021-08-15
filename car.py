import pygame
from math import degrees, sin, radians, copysign, atan2, cos, sin
from pygame.math import Vector2
from constants import *
from utils import clamp, GetPerpendicular, LineLineIntersection, GetDistance

class Car:
    def __init__(self, x, y, angle=0.0, length=4, max_steering=MAX_STEERING, max_acceleration=MAX_ACCELERATION):
        self.position = Vector2(x, y)
        self.velocity = Vector2(0.0, 0.0)
        self.angle = angle
        self.length = length
        self.max_acceleration = max_acceleration
        self.max_steering = max_steering
        self.max_velocity = MAX_VELOCITY
        self.brake_deceleration = 10
        self.free_deceleration = 2
        self.t = 32
        self.acceleration = 0.0
        self.steering = 0.0
        self.sprite = None
        self.x = 0
        self.y = 0
        self.origin = (0, 0)
        self.rectangle = None
        self.lines = None

    def update(self, dt):
        self.velocity += (self.acceleration * dt, 0)
        # max(-self.max_velocity, min(self.velocity.x, self.max_velocity))
        self.velocity.x = clamp(self.velocity.x, -self.max_velocity, self.max_velocity)

        if self.steering:
            turning_radius = self.length / sin(radians(self.steering))
            angular_velocity = self.velocity.x / turning_radius
        else:
            angular_velocity = 0

        self.position += self.velocity.rotate(-self.angle) * dt
        self.angle += degrees(angular_velocity) * dt

    def Forward(self, dt):
        if self.velocity.x < 0:
            self.acceleration = self.brake_deceleration
        else:
            self.acceleration += 1 * dt
    def Backward(self, dt):
        if self.velocity.x > 0:
            self.acceleration = -self.brake_deceleration
        else:
            self.acceleration -= 1 * dt
    def Brake(self, dt):
        if abs(self.velocity.x) > dt * self.brake_deceleration:
            self.acceleration = -copysign(self.brake_deceleration, self.velocity.x)
        else:
            self.acceleration = -self.velocity.x / dt

    def fixed(self,dt):
        if abs(self.velocity.x) > dt * self.free_deceleration:
            self.acceleration = -copysign(self.free_deceleration, self.velocity.x)
        else:
            if dt != 0:
                self.acceleration = -self.velocity.x / dt

    def constrainAcceleration(self):
        # max(-self.max_acceleration, min(self.acceleration, self.max_acceleration))
        self.acceleration = clamp(self.acceleration, -self.max_acceleration, self.max_acceleration)

    def constrainSteering(self):
        # max(-self.max_steering, min(self.steering, self.max_steering))
        self.steering = clamp(self.steering, -self.max_steering, self.max_steering)

    def Right(self, dt):
        self.steering -= MAX_STEERING * dt

    def Left(self, dt):
        self.steering += MAX_STEERING * dt

    def resetSteering(self):
        self.steering = 0

    def SetRectangle(self, screen ,w, h, debug):
        px = self.x + w/2
        py = self.y + h/2

        t0 = cos(radians(self.angle))
        t1 = -sin(radians(self.angle))

        x = t0 * ((w/2)-4) + px
        y = t1 * ((h/2)-4) + py

        x1 = t0 * ((-w/2)+7) + px
        y1 = t1 * ((-h/2)+7) + py

        LeftLine = GetPerpendicular(Vector2(x,y), Vector2(x1, y1), CAR_SIZE[1]/2)
        RightLine = GetPerpendicular(Vector2(x1, y1), Vector2(x, y), CAR_SIZE[1]/2)
        BottomLine = [LeftLine[0], RightLine[0]]
        TopLine = [LeftLine[1], RightLine[1]]

        self.lines = [
        LeftLine,
        RightLine,
        BottomLine,
        TopLine
        ]
        if debug == True:
            pygame.draw.line(screen, Cyan, LeftLine[0], LeftLine[1], 2)
            pygame.draw.line(screen, Cyan, RightLine[0], RightLine[1], 2)
            pygame.draw.line(screen, Cyan, BottomLine[0], BottomLine[1], 2)
            pygame.draw.line(screen, Cyan, TopLine[0], TopLine[1], 2)

    def CheckCollision(self, raceLines):

        for line in self.lines:
            for l in raceLines:
                intersection = LineLineIntersection(
                    line[0][0], line[0][1],
                    line[1][0], line[1][1],
                    l['a'][0], l['a'][1],
                    l['b'][0], l['b'][1])
                if intersection != None:
                    return True

    def Draw(self, screen, debug=False):
        rotated = pygame.transform.rotate(self.sprite, self.angle)
        rect = rotated.get_rect()
        self.x, self.y = self.position * self.t - (rect.width / 2, rect.height / 2)
        self.rectangle = rotated.get_bounding_rect()
        collide = rect.collidepoint(pygame.mouse.get_pos())
        # print(dir(rotated))
        screen.blit(rotated, (self.x, self.y))
        if collide:
            pygame.draw.circle(screen, White, (self.x, self.y), 5)
        self.SetRectangle(screen, rotated.get_width(), rotated.get_height(), debug)
