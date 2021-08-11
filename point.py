import pygame
from constants import Width, Height, Green, Black, White
from math import sqrt

class Point:
    def __init__(self, x=Width//2, y=Height//2, radius=5, color=(40, 240, 235)):
        self.x = x
        self.y = y
        self.color = color
        self.temp = color
        self.selectColor = (225, 40, 245)
        self.radius = radius
        self.selected = False
        self.label = None
        self.labelColor = Green
        self.fontSize = 25
        self.length = 0

    def parseToInt(self):
        return (int(self.x), int(self.y))

    def update(self, clicked):
        mouseX, mouseY = pygame.mouse.get_pos()

        if clicked == True and self.selected == False:
            dist = GetDistance(mouseX, mouseY, self.x, self.y)
            if dist <= self.radius:
                self.selected = True
                self.color = self.selectColor
        elif clicked == True and self.selected == True:
            self.selected = False
            self.color = self.temp

        if self.selected == True:
            self.x = mouseX
            self.y = mouseY


    def Draw(self, screen):
        pygame.draw.circle(screen, self.color, self.parseToInt(), self.radius)
        if self.label:
            font = pygame.font.Font('freesansbold.ttf', self.fontSize)
            text = font.render(self.label, True, self.labelColor)
            textRect = text.get_rect()
            setattr(textRect, "center", (self.x, self.y+30))
            screen.blit(text, textRect)

def GetDistance(x1, y1, x2, y2):
    return sqrt( (x2 - x1) * (x2 - x1) + (y2 - y1) * (y2 - y1))
