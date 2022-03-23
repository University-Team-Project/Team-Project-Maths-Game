import pygame


class Settings:
    def __init__(self):
        pygame.init()
        self.fps = 60
        self.caption = 'Drag & Drop'
        self.width, self.height = 1280, 720
        self.screen = pygame.display.set_mode((self.width, self.height))
        self.fpsClock = pygame.time.Clock()
        pygame.display.set_caption(self.caption)


class Cursor:
    def __init__(self):
        self.defaultCursor = "resources/wii-open.png"
        self.actionCursor = "resources/wii-grab.png"
        self.loadedCursor = pygame.image.load(self.defaultCursor).convert_alpha()

    def setCursor(self, rectangle):
        if rectangle.dragging:
            self.loadedCursor = pygame.image.load(self.actionCursor).convert_alpha()
        else:
            self.loadedCursor = pygame.image.load(self.defaultCursor).convert_alpha()

        x, y = pygame.mouse.get_pos()
        x -= self.loadedCursor.get_width() / 2
        y -= self.loadedCursor.get_height() / 2

        rectangle.surface.blit(self.loadedCursor, (x, y))


class Colours:
    def __init__(self):
        self.WHITE = (255, 255, 255)
        self.PURPLE = (128, 0, 128)
        self.BLACK = (0, 0, 0)
