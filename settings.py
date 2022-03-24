import pygame
from shapes import Rectangle


class Settings:
    def __init__(self, colours):

        """
        :param colours:
        :initialises all the values to be used for game settings / rules
        """

        pygame.init()
        self.fps = 240
        self.caption = 'Drag & Drop'
        self.width, self.height = 1280, 720
        self.screen = pygame.display.set_mode((self.width, self.height))
        self.fpsClock = pygame.time.Clock()
        self.colour = (0, 0, 0)

        self.midWidth = self.width / 2
        self.midHeight = self.height / 2

        # initializes categories into an array, each is categorised by a colour for now, but is displayed as white
        self.category1 = Category(self.screen, 0, 0, self.midWidth - 1, self.midHeight - 1,
                                  colours.WHITE, colours.RED)
        self.category2 = Category(self.screen, self.midWidth + 1, 0, self.width, self.midHeight - 1,
                                  colours.WHITE, colours.GREEN)
        self.category3 = Category(self.screen, 0, self.midHeight + 1, self.midWidth - 1, self.height,
                                  colours.WHITE, colours.BLUE)
        self.category4 = Category(self.screen, self.midWidth + 1, self.midHeight + 1, self.width, self.height,
                                  colours.WHITE, colours.PURPLE)

        self.categoryArray = [[self.category1, self.category2], [self.category3, self.category4]]

        pygame.display.set_caption(self.caption)
        pygame.mouse.set_visible(False)

    def screen_tick(self, colours):

        """
        :param colours:
        :return each tick, draws the game 'map':
        """

        self.screen.fill(self.colour)

        for row in self.categoryArray:
            for col in row:
                col.draw_rectangle()


class Cursor:
    def __init__(self):

        """
        initialises all the data to be used for handling the cursor and its actions
        """

        self.defaultCursor = "resources/wii-open.png"
        self.actionCursor = "resources/wii-grab.png"
        self.loadedCursor = pygame.image.load(self.defaultCursor).convert_alpha()
        self.xPos = 0
        self.yPos = 0

    def set_cursor(self, rectangle):

        """
        :param rectangle:
        :return handles the movement of the rectangle on screen according to the mouse actions:
        """

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

        """
        creates the colours to be used in the game
        """

        self.WHITE = (255, 255, 255)
        self.PURPLE = (128, 0, 128)
        self.RED = (255, 0, 0)
        self.GREEN = (0, 255, 0)
        self.BLUE = (0, 0, 255)


class Category(Rectangle):
    def __init__(self, surface, xPos, yPos, length, width, colour, category):

        """
        :param surface:
        :param xPos:
        :param yPos:
        :param length: 
        :param width:
        :param colour:
        :param category:
        handles the drawing of category rectangles (to recognise collisions with the game piece)
        """

        super().__init__(surface, xPos, yPos, length, width, colour)
        self.category = category
        self.categoryRectangle = pygame.rect.Rect(self.xPos, self.yPos, self.length, self.width)
