import pygame
from constants import *

def clamp(num, min_value, max_value):
   return max(min(num, max_value), min_value)

def DrawTrackTriangles(screen, Top, Bottom, themeIndex=3, wireframe=False):
    n = N_POINTS/CORRELATION
    res = 1
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
