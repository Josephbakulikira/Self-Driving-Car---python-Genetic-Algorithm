import pygame
from point import Point, GetDistance
from random import randint
from constants import Width, Height, Black, White
from math import sqrt, pow, sin, cos, pi

class Spline:
    def __init__(self):
        self.points = []
        self.pointRadius = 10
        self.resolution = 40
        self.lineWidth = 5
        self.lineColor = White
        self.move = 0
        self.length = 0

    def CreatePoints(self, n, showLabel=False):
        for i in range(n):
            x = 500 * sin( i/n * pi * 2) + Width//2
            y = 500 * cos( i/n * pi * 2) + Height//2
            point = Point(x, y, self.pointRadius)
            if showLabel:
                point.label = "P" + str(i)
            self.points.append(point)

    def GetSplinePoints(self, t, loop=False):
        t = t/self.resolution

        if loop == False:
            p1 = int(t) + 1
            p2 = p1 + 1
            p3 = p2 + 1
            p0 = p1 - 1
        else:
            p1 = int(t)
            p2 = (p1 + 1) % len(self.points)
            p3 = (p2 + 1) % len(self.points)
            p0 = p1 - 1 if p1 >= 1 else len(self.points) - 1

        t = t - int(t)

        tt = pow(t, 2)
        ttt = pow(t, 3)

        f1 = -ttt + 2 * tt - t
        f2 = 3 * ttt - 5 * tt + 2
        f3 = -3 * ttt + 4 * tt + t
        f4 = ttt - tt

        _x = (self.points[p0].x * f1 + self.points[p1].x * f2 + self.points[p2].x * f3 + self.points[p3].x * f4) / 2
        _y = (self.points[p0].y * f1 + self.points[p1].y * f2 + self.points[p2].y * f3 + self.points[p3].y * f4) / 2

        return (_x, _y)

    def CalculateSegmentLength(self, node, loop=False):
        length = 0
        # node /= self.resolution
        step_size = 1/self.resolution
        old_point = self.GetSplinePoints(node, loop)
        # new_point = None
        for i in range(self.resolution):
            new_point = self.GetSplinePoints(node + i/self.resolution, loop)
            length += GetDistance(new_point[0], new_point[1], old_point[0], old_point[1])
            old_point = new_point

        return length

    def GetSplineGradient(self, t, loop=False):

        t = t/self.resolution

        if loop == False:
            p1 = int(t) + 1
            p2 = p1 + 1
            p3 = p2 + 1
            p0 = p1 - 1
        else:
            p1 = int(t)
            p2 = (p1 + 1) % len(self.points)
            p3 = (p2 + 1) % len(self.points)
            p0 = p1 - 1 if p1 >= 1 else len(self.points) - 1

        t = t - int(t)

        tt = pow(t, 2)
        ttt = pow(t, 3)

        f1 = -3 * tt + 4 * t - 1
        f2 = 9 * tt - 10 * t
        f3 = -9 * tt + 8 * t + 1
        f4 = 3 * tt - 2 * t

        _x = (self.points[p0].x * f1 + self.points[p1].x * f2 + self.points[p2].x * f3 + self.points[p3].x * f4) / 2
        _y = (self.points[p0].y * f1 + self.points[p1].y * f2 + self.points[p2].y * f3 + self.points[p3].y * f4) / 2

        return (_x, _y)

    def GetNormalizedOffset(p):
        index = 0
        while p > self.points[index].length:
            p -= self.points[index].length
            index += 1
        return (index + (p / self.points[index].length))

    def Draw(self, screen, clicked):
        keys = pygame.key.get_pressed()
        # self.length = 0
        for i in range(self.resolution * len(self.points)):
            x, y = self.GetSplinePoints(i, True)
            pygame.draw.rect(screen, self.lineColor, [int(x), int(y), self.lineWidth, self.lineWidth])

        for i in range(len(self.points)):
            self.points[i].length = self.CalculateSegmentLength(i , True)
            self.length += self.points[i].length
            self.points[i].update(clicked)
            self.points[i].Draw(screen)
            #print(self.points[i].length)

        # print(self.length)
