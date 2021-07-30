import pygame
from constants import *

def clamp(num, min_value, max_value):
   return max(min(num, max_value), min_value)

def Line(a, b):
    return {"a": a, "b": b}

def TrackTriangles(screen, Top, Bottom, themeIndex=3, updateLines=False, Lines=None, wireframe=False, wireframeLine=False):
    n = N_POINTS/CORRELATION
    res = 1
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
        if wireframeLine:
            pygame.draw.line(screen, Red, t, t2, 3)
            pygame.draw.line(screen, Yellow, b, b2, 3)

        if updateLines == True:
            if Line(t, t2) not in Lines:
                Lines.append(Line(t, t2))
            if Line(b, b2) not in Lines:
                Lines.append(Line(b, b2))

    updateLines=False
