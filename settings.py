import pygame
from shapes import Rectangle


class Settings:
    def __init__(self, colours):
        pygame.init()
        self.fps = 240
        self.caption = 'Drag & Drop'
        self.width, self.height = 1280, 720
        self.screen = pygame.display.set_mode((self.width, self.height))
        self.fpsClock = pygame.time.Clock()
        self.colour = (0, 0, 0)
        self.category1 = Category(self.screen, 0, 0, self.width / 2, self.height / 2, colours.RED,
                                  colours.RED)
        self.category2 = Category(self.screen, self.width / 2, 0, self.width, self.height / 2, colours.GREEN,
                                  colours.GREEN)
        self.category3 = Category(self.screen, 0, self.height / 2, self.width / 2, self.height, colours.BLUE,
                                  colours.BLUE)
        self.category4 = Category(self.screen, self.width / 2, self.height / 2, self.width, self.height, colours.PURPLE,
                                  colours.PURPLE)
        pygame.display.set_caption(self.caption)
        pygame.mouse.set_visible(False)

    def screen_tick(self, colours):
        self.screen.fill(self.colour)
        self.category1.draw_rectangle()
        self.category2.draw_rectangle()
        self.category3.draw_rectangle()
        self.category4.draw_rectangle()


class Cursor:
    def __init__(self):
        self.defaultCursor = "resources/wii-open.png"
        self.actionCursor = "resources/wii-grab.png"
        self.loadedCursor = pygame.image.load(self.defaultCursor).convert_alpha()
        self.xPos = 0
        self.yPos = 0

    def set_cursor(self, rectangle):
        if rectangle.dragging:
            self.loadedCursor = pygame.image.load(self.actionCursor).convert_alpha()
        else:
            self.loadedCursor = pygame.image.load(self.defaultCursor).convert_alpha()

        self.xPos, self.yPos = pygame.mouse.get_pos()
        self.xPos -= self.loadedCursor.get_width() / 2
        self.yPos -= self.loadedCursor.get_height() / 2

        rectangle.surface.blit(self.loadedCursor, (self.xPos, self.yPos))


class Colours:
    def __init__(self):
        self.WHITE = (255, 255, 255)
        self.PURPLE = (128, 0, 128)
        self.RED = (255, 0, 0)
        self.GREEN = (0, 255, 0)
        self.BLUE = (0, 0, 255)


class Category(Rectangle):
    def __init__(self, surface, xPos, yPos, length, width, colour, category):
        super().__init__(surface, xPos, yPos, length, width, colour)
        self.category = category
        self.categoryRectangle = pygame.rect.Rect(self.xPos, self.yPos, self.length, self.width)
