import pygame


class Rectangle:
    def __init__(self, surface, xPos, yPos, length, width, colour):
        self.surface = surface
        self.xPos = xPos
        self.yPos = yPos
        self.length = length
        self.width = width
        self.colour = colour
        self.dragging = False
        self.pygameRectangle = pygame.rect.Rect(self.xPos, self.yPos, self.length, self.width)

    def draw_rectangle(self):
        self.pygameRectangle = pygame.rect.Rect(self.xPos, self.yPos, self.length, self.width)
        pygame.draw.rect(self.surface, self.colour, self.pygameRectangle)
