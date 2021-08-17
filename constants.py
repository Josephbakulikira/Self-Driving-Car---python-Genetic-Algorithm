Width = 1920
Height = 1080

Black = (0, 0, 0)
White = (255, 255, 255)
Red = (255, 0, 0)
Green = (0,166,25)
Grass = (9,176,81)
Blue = (0, 0, 255)
Yellow = (255, 255, 0)
Gray = (100, 100, 100)
Cyan = (0, 255, 255)

MAX_SENSOR = 100

MAX_STEERING = 45
MAX_VELOCITY = 5
MAX_ACCELERATION = 1.0

CAR_SIZE = (60, 30)

# when you load a data file ,
# check if these 3 value are the same with the saved data
# eg1: track1 -> N_POINTS=25, SPLINE_RESOLUTION=10
# eg2: track2 -> N_POINTS=25, SPLINE_RESOLUTION=10
# eg3: track3 -> N_POINTS=10, SPLINE_RESOLUTION=15
# eg4: track4 -> N_POINTS=10, SPLINE_RESOLUTION=5

TRACK_WIDTH = 70
SPLINE_RESOLUTION = 5
N_POINTS = 10

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
    },
    { # --- Night Drive -- 4
        "track": (102,51,68),
        "background": (17,17,34)
    }
]
