import os
import pygame
import pickle
import neat
from point import Point, GetDistance
from spline import Spline
from math import sin, radians, degrees, copysign, sqrt
from pygame.math import Vector2
from car import Car
from utils import TrackTriangles, translate
from constants import *
from UI.setup import *

pygame.init()
# pygame.display.set_caption(" Self Driving Car")
screen = pygame.display.set_mode((Width, Height), vsync=True)
clock = pygame.time.Clock()
fps = 60

# load Assets
track_filename = "./map/new_track3"
current_directory = os.path.dirname(os.path.abspath(__file__))
carImage_path = os.path.join(current_directory, "./Assets/car2.png")
car_sprite = pygame.image.load(carImage_path)
sprite = pygame.transform.scale(car_sprite, CAR_SIZE)



#  ---- Initiate New splines and lines ---

# track = Spline()
# trackTopBound = Spline()
# trackBottomBound = Spline()
# trackTopBound.pointRadius = 1
# trackBottomBound.pointRadius = 1
#
# track.CreatePoints(N_POINTS, False)
# trackBottomBound.CreatePoints(N_POINTS, False)
# trackTopBound.CreatePoints(N_POINTS, False)
#
# track.resolution = SPLINE_RESOLUTION
# trackBottomBound.resolution = SPLINE_RESOLUTION
# trackTopBound.resolution = SPLINE_RESOLUTION
# TrackLines = []

# -- OR --

# ---- load the Saved data ----
# if you load the tracks and it doesn't look like before (incomplete)
# check if the constants is the
# same as the saved data

filename = "./map/track4"
loadData = pickle.load(open(filename, 'rb'))
track = loadData['TRACK']
trackTopBound = loadData['TOP_TRACK']
trackBottomBound = loadData['BOTTOM_TRACK']
TrackLines = loadData['LINES']

# ---------

debug=False
editorMode = False
edit=False
wireframe=False
wireframeLine=False
updateLines = False

# set changed=True if you want to edit a track or create a new one
changed = False

saveChange = False
ThemeIndex = 3

showPanel = False

def Fitness(genomes, config):
    global ThemeIndex, edit, debug, editorMode, wireframe, wireframeLine, updateLines
    global changed, saveChange, showPanel
    nets = []
    genes = []
    cars = []

    for index, genome in genomes:
        genome.fitness = 0
        nn = neat.nn.FeedForwardNetwork.create(genome, config)
        nets.append(nn)

        car = Car(4, 21)
        car.sprite = sprite
        car.angle = 90
        cars.append(car)
        genome.fitness = 0
        genes.append(genome)

    # car = Car(30, 4)
    # car.sprite = sprite


    counter = 1

    run = True
    MouseClicked = False

    while run:
        screen.fill(Themes[ThemeIndex]["background"])

        dt = clock.get_time()/1000
        clock.tick(fps)
        framerate = clock.get_fps()
        pygame.display.set_caption("Self Driving Car AI - FrameRate(fps) : {}".format(int(framerate)))

        if edit == True:
            changed = True

        # HANDLE EVENT
        # q -> Switch themes , Esc -> to close window
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_ESCAPE:
                    run = False
                    pygame.quit()
                if event.key == pygame.K_q:
                    ThemeIndex = (ThemeIndex + 1 ) % len(Themes)
                if event.key == pygame.K_RETURN or event.key == pygame.K_p:
                    showPanel = not showPanel
                if event.key == pygame.K_r:
                    debug = not debug
                    wireframeLine= not wireframeLine
            if event.type == pygame.MOUSEBUTTONDOWN:
                MouseClicked = True

        # --- CAR HANDLE INPUTS ------------
        # keys = pygame.key.get_pressed()
        # if keys[pygame.K_UP] or keys[pygame.K_w]:
        #     car.Forward(dt)
        #
        # elif keys[pygame.K_DOWN] or keys[pygame.K_s]:
        #     car.Backward(dt)
        #
        # elif keys[pygame.K_SPACE]:
        #     car.Brake(dt)
        # else:
        #     car.fixed(dt)
        #
        # if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
        #     car.Right(dt)
        # elif keys[pygame.K_LEFT] or keys[pygame.K_a]:
        #     car.Left(dt)
        # else:
        #     car.resetSteering()
        # ----------------------------------

        for index, car in enumerate(cars):

            car.Forward(dt)
            car.constrainAcceleration()
            genes[index].fitness += 0.1
            output = nets[index].activate(
                (car.velocity.x,
                car.velocity.y,
                car.intersections[0]["distance"],
                car.intersections[1]["distance"],
                car.intersections[2]["distance"],
                car.intersections[3]["distance"],
                car.intersections[4]["distance"],
                )
            )

            # if abs(output[0]) == 1:
            #     car.Forward(dt)
            # elif abs(output[1]) == 1:
            #     car.Brake(dt)

            if output[0] > 0.5:
                car.Right(dt)
            if output[1] > 0.5:
                car.Left(dt)



        if changed == True:
            for i in range(N_POINTS ):
                p1 = track.GetSplinePoints(i * SPLINE_RESOLUTION, True)
                g1 = track.GetSplineGradient(i * SPLINE_RESOLUTION, True)
                glength = sqrt(g1[0] * g1[0] + g1[1] * g1[1])

                trackTopBound.points[i].x = p1[0] - TRACK_WIDTH * (-g1[1]/glength)
                trackTopBound.points[i].y = p1[1] - TRACK_WIDTH * (g1[0]/glength)

                trackBottomBound.points[i].x = p1[0] + TRACK_WIDTH * (-g1[1]/glength)
                trackBottomBound.points[i].y = p1[1] + TRACK_WIDTH * (g1[0]/glength)

        # draw track triangles and extract the lines out of the track
        TrackTriangles(
            screen ,
            Top=trackTopBound,
            Bottom=trackBottomBound,
            themeIndex=ThemeIndex,
            updateLines=True,
            Lines=TrackLines,
            wireframe=wireframe,
            wireframeLine=wireframeLine
            )

        if debug:
            trackBottomBound.Draw(screen, False)
            trackTopBound.Draw(screen, False)

        if editorMode:
            track.Draw(screen, MouseClicked, edit)

        if len(cars) > 0:
            for index, car in enumerate(cars):

                car.constrainSteering()
                car.update(screen, dt, TrackLines, debug)
                car.Draw(screen, debug)

                if car.crashed == True:
                    pygame.draw.circle(screen, Red, car.center, 8)
                    genes[index].fitness -= 1
                    cars.pop(index)
                    nets.pop(index)
                    genes.pop(index)
        else:
            run = False

        # Render UI
        if showPanel == True:
            # might need to change the way i render ui for optimisation
            panel.Render(screen)
            quitSave.Render(screen)
            editorModeText.Render(screen)
            editText.Render(screen)
            wireframeModeText.Render(screen)
            showLineText.Render(screen)

            editorMode = editorModeToggle.Render(screen, MouseClicked)
            edit = editToggle.Render(screen, MouseClicked)
            wireframe = wireframeToggle.Render(screen, MouseClicked)
            debug = ShowlineToggle .Render(screen, MouseClicked)
            wireframeLine = debug

            if edit == True:
                TrackWidthText.Render(screen)
                TRACK_WIDTH = WidthSlider.Render(screen)

        if quitSave.state == True:
            saveChange = True
            run = False

        for gene in genes:
            gene.fitness += 0.5

        counter += 1


        MouseClicked = False
        if editorMode:
            changed = True
        else:
            changed = False

        pygame.display.flip()

    # save our edited track and the lines of the track
    if saveChange == True:
        data = {
            "TRACK":track,
            "TOP_TRACK": trackTopBound,
            "BOTTOM_TRACK": trackBottomBound,
            "LINES": TrackLines,
            "VARIABLES": {
                "N_POINTS": N_POINTS,
                "RESOLUTION": SPLINE_RESOLUTION,
                "TRACK_WIDTH": TRACK_WIDTH
            }
        }
        pickle.dump(data, open(track_filename, 'wb'))


# main(genomes, configfiles)

# neat setup


def run(config_path):
    config = neat.config.Config(
        neat.DefaultGenome,
        neat.DefaultReproduction,
        neat.DefaultSpeciesSet,
        neat.DefaultStagnation,
        config_path
        )
    popul = neat.Population(config)
    popul.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    popul.add_reporter(stats)
    winner = popul.run(Fitness,50)
    # print("\n Best genome: \n{!s}".format(winner))
if __name__ == "__main__":
    local_dir = os.path.dirname(__file__) # current directory
    config_path = os.path.join(local_dir, "config-feedforward.txt")
    run(config_path)
