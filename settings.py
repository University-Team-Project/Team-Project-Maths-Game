import pygame


class Settings:
    def __init__(self):
        self.fps = 60
        self.caption = 'Drag & Drop'
        self.width, self.height = 1280, 720
        self.screen = pygame.display.set_mode((self.width, self.height))
        