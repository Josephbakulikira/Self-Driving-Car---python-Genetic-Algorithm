import pygame
from math import degrees, sin, radians, copysign, atan2, cos, sin
from pygame.math import Vector2
from constants import *
from utils import *

class Car:
    def __init__(self, x, y, angle=0.0, length=4, max_steering=MAX_STEERING, max_acceleration=MAX_ACCELERATION):
        self.position = Vector2(x, y)
        self.velocity = Vector2(0.0, 0.0)
        self.center = None
        self.angle = angle
        self.length = length
        self.max_acceleration = max_acceleration
        self.max_steering = max_steering
        self.max_velocity = MAX_VELOCITY
        self.max_distance = MAX_SENSOR
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
        self.lines = []
        self.sensors = []
        self.crashed = False
        self.intersections = [Intersection(None, translate(MAX_SENSOR, 0, MAX_SENSOR, 0, 1)) for _ in range(5)]

    def update(self,screen, dt, tracklines, debug=False):

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

        if self.rectangle != None:
            self.SetRectangle(screen, self.rectangle.get_width(), self.rectangle.get_height(), debug)
            self.updateSensors(screen, debug)
            self.checkSensorIntersection(tracklines)

        self.crashed = self.CheckDeath(tracklines)

        if debug == True:
            if len(self.intersections) > 0:
                for p in self.intersections:
                    if p["position"] != None:
                        pygame.draw.line(screen, (150, 100, 255), self.center, p["position"], 2)
                        pygame.draw.circle(screen, (250, 150, 42), p["position"], 5)
                        # print(p['distance'])

    def Forward(self, dt):
        if self.velocity.x < 0:
            self.acceleration = self.brake_deceleration
        else:
            self.acceleration += 2 * dt
    def Backward(self, dt):
        if self.velocity.x > 0:
            self.acceleration = -self.brake_deceleration
        else:
            self.acceleration -= 2 * dt
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

    def updateSensors(self, screen, debug=False):
        self.sensors = []
        for i in range(0, 180 + 180//4, 180//4):
            x = sin(radians(self.angle + i)) * self.max_distance + self.center.x
            y = cos(radians(self.angle + i)) * self.max_distance + self.center.y
            self.sensors.append(Vector2(x,y))
        if debug==True:
            pygame.draw.circle(screen, (240, 150 ,23), self.center, 5)
            # for p in self.sensors:
            #     pygame.draw.line(screen, (i, i+70, 255), self.center, p, 2)

    def checkSensorIntersection(self, raceTrackLines):
        self.intersections.clear()
        self.intersections = [Intersection(None, translate(MAX_SENSOR, 0, MAX_SENSOR, 0, 1)) for _ in range(5)]

        for i in range(len(self.sensors)):
            closest = Intersection(None, translate(MAX_SENSOR, 0, MAX_SENSOR, 0, 1))
            for l in raceTrackLines:
                intersection = LineLineIntersection(
                self.center.x, self.center.y,
                self.sensors[i].x, self.sensors[i].y,
                l['a'][0], l['a'][1],
                l['b'][0], l['b'][1]
                )
                if intersection != None:

                    inters = Intersection(intersection,
                        translate(
                        GetDistance(self.center, Vector2(intersection[0], intersection[1]))
                        , 0, MAX_SENSOR, 0, 1 )
                        )
                    if inters["distance"] < closest["distance"]:
                        self.intersections[i] = inters
                        closest = inters

    def SetRectangle(self, screen ,w, h, debug):
        px = self.x + w/2
        py = self.y + h/2
        self.center = Vector2(px, py)
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

    def CheckDeath(self, raceLines):
        for line in self.lines:
            for l in raceLines:
                intersection = LineLineIntersection(
                    line[0][0], line[0][1],
                    line[1][0], line[1][1],
                    l['a'][0], l['a'][1],
                    l['b'][0], l['b'][1])
                if intersection != None:
                    return True

        return False


    def Draw(self, screen, debug=False):
        rotated = pygame.transform.rotate(self.sprite, self.angle)
        self.rectangle = rotated
        rect = rotated.get_rect()
        self.x, self.y = self.position * self.t - (rect.width / 2, rect.height / 2)
        collide = rect.collidepoint(pygame.mouse.get_pos())
        # print(dir(rotated))
        screen.blit(rotated, (self.x, self.y))
        if collide:
            pygame.draw.circle(screen, White, (self.x, self.y), 5)
