import pygame
from constants import *

def clamp(num, min_value, max_value):
   return max(min(num, max_value), min_value)

def DrawTrackTriangles(screen, Top, Bottom, res, debug=False):
    n = N_POINTS/CORRELATION
    for i in range(N_POINTS * int(n) ):
        t = Top.GetSplinePoints(i * n * res/SPLINE_RESOLUTION , True)
        b = Bottom.GetSplinePoints(i * n * res/SPLINE_RESOLUTION , True)
        t2 = Top.GetSplinePoints(i * n * res/SPLINE_RESOLUTION + 1 - 0.000001, True)
        b2 = Bottom.GetSplinePoints(i * n * res/SPLINE_RESOLUTION + 1 - 0.000001, True)

        if debug:
            pygame.draw.polygon(screen, Yellow, [t, b, b2], 1)
            pygame.draw.polygon(screen, Red, [t, t2, b2], 1)
        else:
            pygame.draw.polygon(screen, Gray, [t, b, b2])
            pygame.draw.polygon(screen, Gray, [t, t2, b2])
