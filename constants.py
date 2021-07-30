Width = 1800
Height = 900

Black = (0, 0, 0)
White = (255, 255, 255)
Red = (255, 0, 0)
Green = (0,166,25)
Grass = (9,176,81)
Blue = (0, 0, 255)
Yellow = (255, 255, 0)
Gray = (100, 100, 100)
Cyan = (0, 255, 255)

MAX_STEERING = 30
MAX_VELOCITY = 20
MAX_ACCELERATION = 5.0

TRACK_WIDTH = 70
SPLINE_RESOLUTION = 5
N_POINTS = 25
# CORRELATION BETWEEN THE SPLINE RESOLUTION AND THE
# NUMBER OF POINTS
CORRELATION = N_POINTS/SPLINE_RESOLUTION

INITIAL_POINT_RADIUS_SPLINE = 400

Themes = [
    { # -- Black and white--0
        "track": White,
        "background": Black
    },
    { # --- Inverted--1
        "track": Black,
        "background": White
    },
    { # --- Desert--2
        "track": (178,150,146),
        "background": (212,164,60)
    },
    { # --- Default--3
        "track": (100, 100, 100),
        "background": Grass
    }
]
