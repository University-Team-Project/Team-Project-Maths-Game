import pygame
import random


class Game:
    def __init__(self):
        """
        :initialises all the values to be used for game settings / rules
        """

        pygame.init()
        self.fps = 240
        self.caption = 'Area & Perimeter'
        self.width, self.height = 1280, 720
        self.screen = pygame.display.set_mode((self.width, self.height))
        self.clock = pygame.time.Clock()
        self.colour = (251, 204, 194)
        self.score = 0
        self.background = pygame.transform.scale(pygame.image.load('resources/background.png'), (1280, 720)).convert()
        self.midWidth = self.width / 2
        self.midHeight = self.height / 2
        self.objects = []
        self.colours = Colours()
        self.question = self.generate_question()

        self.score_font = pygame.font.Font("resources/font/static/Inter-SemiBold.ttf", 40)
        self.timer_font = pygame.font.Font("resources/font/static/Inter-SemiBold.ttf", 40)
        self.question_font = pygame.font.Font("resources/font/static/Inter-SemiBold.ttf", 60)
        self.label_font = pygame.font.Font("resources/font/static/Inter-SemiBold.ttf", 15)

        pygame.display.set_caption(self.caption)
        pygame.mouse.set_visible(False)
        pygame.time.set_timer(pygame.USEREVENT, 1000)

    def screen_tick(self):
        """
        :return each tick, draws the game 'map':
        """

        self.screen.blit(self.background, (0, 0))

    def generate_question(self):
        length = random.randint(50, 250)
        height = random.randint(50, 250)
        rectangle = Rectangle(self.screen, False, self.screen.get_rect().centerx - length / 2,
                              self.screen.get_rect().centery - height / 2, length, height,
                              self.colours.completely_random_colour())
        self.objects = self.objects = [rectangle]
        self.objects.append(rectangle.answer)
        self.question = rectangle
        if rectangle.choice == "Area":
            self.objects.append(Answer(str(random.randint(1, 800)) + "cm²",
                                       self.screen, True, random.randint(100, 1100), random.randint(600, 600)))
            self.objects.append(Answer(str(random.randint(1, 800)) + "cm²",
                                       self.screen, True, random.randint(100, 1100), random.randint(600, 600)))
        else:
            self.objects.append(Answer(str(random.randint(1, 100)) + "cm",
                                       self.screen, True, random.randint(100, 1100), random.randint(600, 600)))
            self.objects.append(Answer(str(random.randint(1, 100)) + "cm",
                                       self.screen, True, random.randint(100, 1100), random.randint(600, 600)))

        return rectangle

    def correct_answer(self, pos):
        self.objects = []
        self.score += 1
        self.generate_question()

    def incorrect_answer(self, pos):
        self.objects = []
        self.generate_question()


class Cursor:
    def __init__(self, screen):

        """
        initialises all the data to be used for handling the cursor and its actions
        """
        self.screen = screen
        self.defaultCursor = "resources/wii-open.png"
        self.actionCursor = "resources/wii-grab.png"
        self.loadedCursor = pygame.image.load(self.defaultCursor).convert_alpha()
        self.xPos = 0
        self.yPos = 0
        self.holding = False

    def set_holding(self, holding, obj=None):

        """
        :param obj:
        :param holding:
        :return handles the movement of the rectangle on screen according to the mouse actions:
        """

        if holding:
            self.loadedCursor = pygame.image.load(self.actionCursor).convert_alpha()
        else:
            self.holding = False
            self.loadedCursor = pygame.image.load(self.defaultCursor).convert_alpha()

        self.xPos, self.yPos = pygame.mouse.get_pos()
        if obj is not None:
            self.holding = True
            self.xPos -= self.loadedCursor.get_width() / 2
            self.yPos -= self.loadedCursor.get_height() / 2
            obj.surface.blit(self.loadedCursor, (self.xPos, self.yPos))
        else:
            self.load_cursor()

    def load_cursor(self):
        self.screen.blit(self.loadedCursor, (self.xPos, self.yPos))


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

    def random_colour(self):
        return random.choice(list(self.__dict__.values()))

    def completely_random_colour(self):
        return random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)


class Object:
    def __init__(self, surface, draggable, xPos, yPos):
        self.surface = surface
        self.draggable = draggable
        self.dragging = False
        self.xPos = xPos
        self.yPos = yPos


class Rectangle(Object):
    def __init__(self, surface, draggable, xPos, yPos, length, height, colour):
        super().__init__(surface, draggable, xPos, yPos)
        self.length = length
        self.height = height
        self.estimated_length = round(length * 0.1)
        self.estimated_height = round(height * 0.1)
        self.estimated_area = self.estimated_length * self.estimated_height
        self.estimated_perimeter = (self.estimated_length * 2) + (self.estimated_height * 2)
        self.colour = colour
        self.pygameRectangle = pygame.rect.Rect(self.xPos, self.yPos, self.length, self.height)
        self.choice = random.choice(["Area", "Perimeter"])
        if self.choice == "Area":
            self.answer = Answer(str(self.estimated_area) + "cm²", self.surface, True, random.randint(100, 1100),
                                 random.randint(600, 600))
        else:
            self.answer = Answer(str(self.estimated_perimeter) + "cm", self.surface, True, random.randint(100, 1100),
                                 random.randint(600, 600))

    def draw(self, game):
        self.pygameRectangle = pygame.rect.Rect(self.xPos, self.yPos, self.length, self.height)
        pygame.draw.rect(self.surface, self.colour, self.pygameRectangle)
        self.surface.blit(game.label_font.render(str(self.estimated_length) + "cm", True, (0, 0, 0)),
                          (self.pygameRectangle.centerx - 7.5, self.yPos + self.height))
        self.surface.blit(game.label_font.render(str(self.estimated_height) + "cm", True, (0, 0, 0)),
                          (self.xPos + self.length, self.pygameRectangle.centery - 7.5))


class Answer(Object):
    def __init__(self, text, surface, draggable, xPos, yPos):
        super().__init__(surface, draggable, xPos, yPos)
        self.text = text
        self.font = pygame.font.Font("resources/font/static/Inter-SemiBold.ttf", 50)
        self.place_text = self.font.render(self.text, True, (0, 0, 0))
        self.pygameRectangle = self.place_text.get_rect(center=(self.xPos, self.yPos))

    def draw(self, game):
        self.place_text = self.font.render(self.text, True, (0, 0, 0))
        self.pygameRectangle = self.place_text.get_rect(center=(self.xPos, self.yPos))
        self.surface.blit(self.place_text, self.pygameRectangle)


class Category(Rectangle):
    def __init__(self, surface, xPos, yPos, length, colour, category, draggable, height):
        """
        :param surface:
        :param xPos:
        :param yPos:
        :param length:
        :param colour:
        :param category:
        handles the drawing of category rectangles (to recognise collisions with the game piece)
        """
        super().__init__(surface, draggable, xPos, yPos, length, height, colour)
        self.category = category
        self.categoryRectangle = pygame.rect.Rect(self.xPos, self.yPos, self.length, self.height)
