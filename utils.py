import pygame
from constants import *
from math import sqrt
from pygame.math import Vector2

def clamp(num, min_value, max_value):
   return max(min(num, max_value), min_value)

def Line(a, b):
    return {"a": a, "b": b}

def translate(value, min1, max1, min2, max2):
    return min2 + (max2-min2) * ((value-min1)/(max1-min1))

def Intersection(position, distance):
    return {"position":position, "distance":distance}

def TrackTriangles(screen, Top, Bottom, themeIndex=3, updateLines=False, Lines=None, wireframe=False, wireframeLine=False):
    n = N_POINTS/CORRELATION
    res = 1
    lines = []
    if updateLines == True:
        Lines.clear()

    for i in range(N_POINTS * int(n) ):
        t = Top.GetSplinePoints(i * n * res/SPLINE_RESOLUTION , True)
        b = Bottom.GetSplinePoints(i * n * res/SPLINE_RESOLUTION , True)
        t2 = Top.GetSplinePoints(i * n * res/SPLINE_RESOLUTION + 1 - 0.000001, True)
        b2 = Bottom.GetSplinePoints(i * n * res/SPLINE_RESOLUTION + 1 - 0.000001, True)

        pygame.draw.polygon(screen, Themes[themeIndex]["track"], [t, b, b2])
        pygame.draw.polygon(screen, Themes[themeIndex]["track"], [t, t2, b2])

        if wireframe:
            pygame.draw.polygon(screen, Cyan, [t, b, b2], 1)
            pygame.draw.polygon(screen, Cyan, [t, t2, b2], 1)
            pygame.draw.line(screen, Red, t, b)
            lines.append([t, b])

        if wireframeLine:
            pygame.draw.line(screen, (175, 152, 255), t, t2, 3)
            pygame.draw.line(screen, (175, 152, 255), b, b2, 3)

        if updateLines == True:
            if Line(t, t2) not in Lines:
                Lines.append(Line(t, t2))
            if Line(b, b2) not in Lines:
                Lines.append(Line(b, b2))

    updateLines=False
    return lines
def GetDistance(a, b):
    return sqrt( (b.x-a.x)*(b.x-a.x) + (b.y-a.y)*(b.y-a.y))

def Magnitude(a):
    return sqrt(a.x * a.x + b.y * b.y)

def GetPerpendicular(A, B, length):
    _rise, _run = (B.y - A.y), (B.x - A.x)
    slope = 0
    if _run == 0:
        slope = 0
    else:
        slope = _rise/_run
    dy = sqrt(length**2 / (slope**2+1))
    dx = -slope * dy
    C = Vector2( B.x + dx, B.y + dy )
    D = Vector2( B.x - dx, B.y - dy )

    return [tuple(C), tuple(D)]

def LineLineIntersection(x1, y1, x2, y2, x3, y3, x4, y4):
    denominator = (x1-x2)*(y3-y4) - (y1-y2)*(x3-x4)
    if denominator == 0:
        # if the denominator is 0 , that means the two lines are almost parallel
        return None
    numeratorT = (x1-x3)*(y3-y4) - (y1-y3)*(x3-x4)
    numeratorU = (x2-x1)*(y1-y3) - (y2-y1)*(x1-x3)

    t = numeratorT/denominator
    u = numeratorU/denominator

    if t>=0 and t<=1 and u >= 0 and u <= 1:
        x = x1 + t*(x2-x1)
        y = y1 + t*(y2-y1)
        # or
        #x = x3+u*(x4-x3)
        #y = y3+u*(y4-y3)
        return (x, y)
    return None
