import pygame


class Rectangle:
    def __init__(self, surface, xPos, yPos, length, width, category):
        self.surface = surface
        self.xPos = xPos
        self.yPos = yPos
        self.length = length
        self.width = width
        self.colour = (255, 255, 255)
        self.border = (0, 0, 0)
        self.category = category
        self.active = True
        self.dragging = False
        self.pygameRectangle = pygame.rect.Rect(self.xPos, self.yPos, self.length, self.width)

    def draw_rectangle(self):
        self.pygameRectangle = pygame.rect.Rect(self.xPos, self.yPos, self.length, self.width)
        pygame.draw.rect(self.surface, self.colour, self.pygameRectangle)

    def draw_question_rectangle(self):
        self.pygameRectangle = pygame.rect.Rect(self.xPos, self.yPos, self.length, self.width)
        pygame.draw.rect(self.surface, self.colour, self.pygameRectangle, 0, 15)
        pygame.draw.rect(self.surface, self.border, self.pygameRectangle, 3, 15)
