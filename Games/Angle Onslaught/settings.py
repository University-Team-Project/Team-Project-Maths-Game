import random
import csv
import pygame
import pygame_textinput
from shapes import Rectangle


class Settings:
    def __init__(self, colours):

        """
        :param colours:
        :initialises all the values to be used for game settings / rules
        """

        pygame.init()
        self.fps = 165
        self.caption = 'Drag & Drop'
        self.width, self.height = 1280, 720
        self.screen = pygame.display.set_mode((self.width, self.height))
        self.start_image = pygame.image.load('resources/overlay/game_start.png').convert_alpha()
        self.overlay = "resources/overlay/space_overlay.png"
        self.endOverlay = "resources/overlay/end_space_overlay.png"
        self.loadedOverlay = pygame.image.load(self.overlay).convert_alpha()
        self.loadedEndOverlay = pygame.image.load(self.endOverlay).convert_alpha()
        self.fpsClock = pygame.time.Clock()
        self.colour = (0, 0, 0)
        self.username = ""

        self.timer_font = pygame.font.Font("resources/font/static/Inter-SemiBold.ttf", 30)
        self.score_font = pygame.font.Font("resources/font/static/Inter-SemiBold.ttf", 40)
        self.question_font = pygame.font.Font("resources/font/static/Inter-SemiBold.ttf", 13)
        self.username_font = pygame.font.Font("resources/font/static/Inter-SemiBold.ttf", 20)
        self.choice_font = pygame.font.Font("resources/font/static/Inter-SemiBold.ttf", 30)
        self.end_font = pygame.font.Font("resources/font/static/Inter-SemiBold.ttf", 60)

        self.questions_array = []

        self.midWidth = self.width / 2
        self.midHeight = ((5 / 6) * self.height) / 2

        self.defCatWidth = 600
        self.defCatHeight = 344

        self.settingCatWidth = 70
        self.settingCatHeight = 72

        self.restartCatWidth = 190
        self.restartCatHeight = 64

        self.exitCatWidth = 140
        self.exitCatHeight = 64

        self.defaultCategory = Category(self.screen,
                                        self.midWidth - (self.defCatWidth / 2),
                                        self.midHeight - (self.defCatHeight / 2),
                                        self.defCatWidth,
                                        self.defCatHeight,
                                        colours.WHITE,
                                        None)

        self.timerCategory = Category(self.screen,
                                      self.midWidth - (self.settingCatWidth + 20),
                                      20,
                                      self.settingCatWidth,
                                      self.settingCatHeight,
                                      colours.WHITE,
                                      None)

        self.scoreCategory = Category(self.screen,
                                      self.midWidth + 20 + self.settingCatWidth,
                                      20,
                                      self.settingCatWidth,
                                      self.settingCatHeight,
                                      colours.WHITE,
                                      None)

        self.restartCategory = Category(self.screen,
                                        (self.screen.get_width() / 2) - 95,
                                        (self.screen.get_height() / 2) + 168,
                                        self.restartCatWidth,
                                        self.restartCatHeight,
                                        colours.WHITE,
                                        'button')

        self.exitCategory = Category(self.screen,
                                     (self.screen.get_width() / 2) - 70,
                                     (self.screen.get_height() / 2) + 252,
                                     self.exitCatWidth,
                                     self.exitCatHeight,
                                     colours.WHITE,
                                     'button')

        self.endgameCategoryArray = [self.restartCategory, self.exitCategory]

        # initializes categories into an array, each is categorised by a colour for now, but is displayed as white
        self.category1 = Category(self.screen, 0, 0, self.midWidth - 1, self.midHeight - 1,
                                  colours.WHITE, colours.RED)
        self.category2 = Category(self.screen, self.midWidth + 1, 0, self.midWidth, self.midHeight - 1,
                                  colours.WHITE, colours.GREEN)
        self.category3 = Category(self.screen, 0, self.midHeight + 1, self.midWidth - 1, self.midHeight,
                                  colours.WHITE, colours.BLUE)
        self.category4 = Category(self.screen, self.midWidth + 1, self.midHeight + 1, self.midWidth, self.midHeight,
                                  colours.WHITE, colours.PURPLE)

        self.categoryArray = [self.category1, self.category2, self.category3, self.category4]

        pygame.display.set_caption(self.caption)
        pygame.mouse.set_visible(False)

    # function to load three images using an array of file paths
    def countdown_overlay(self):

        paths = [pygame.image.load('resources/countdown/countdown_three.png').convert_alpha(),
                 pygame.image.load('resources/countdown/countdown_two.png').convert_alpha(),
                 pygame.image.load('resources/countdown/countdown_one.png').convert_alpha()]

        # wait 1000 milliseconds between each image blit

        for i in range(len(paths)):
            self.screen.blit(paths[i], (0, 0))
            pygame.display.flip()
            pygame.time.wait(1000)

    def screen_tick(self, colours, score, timer, active):

        """
        :param active:
        :param timer:
        :param score:
        :param colours:
        :return each tick, draws the game 'map':
        """

        if active:

            self.screen.fill(self.colour)

            self.defaultCategory.draw_rectangle()
            self.scoreCategory.draw_rectangle()
            self.timerCategory.draw_rectangle()

            for row in self.categoryArray:
                row.draw_rectangle()

            self.screen.blit(self.loadedOverlay, (0, 0))

            temp_count = 0
            for row in self.categoryArray:
                temp_count += 1
                category_text = self.choice_font.render(str(row.category), True, (0, 0, 0))

                # if temp_count is even
                if temp_count < 3:
                    # if temp_count is 1
                    if temp_count == 1:
                        category_text_rect = category_text.get_rect(
                            center=(row.xPos + self.midWidth / 2 - 150, row.yPos + self.midHeight / 2 - 25))
                    # if temp_count is 2
                    elif temp_count == 2:
                        category_text_rect = category_text.get_rect(
                            center=(row.xPos + self.midWidth / 2 + 150, row.yPos + self.midHeight / 2 - 25))
                else:
                    # if temp_count is 3
                    if temp_count == 3:
                        category_text_rect = category_text.get_rect(
                            center=(row.xPos + self.midWidth / 2 - 150, row.yPos + self.midHeight / 2 + 25))
                    # if temp_count is 4
                    elif temp_count == 4:
                        category_text_rect = category_text.get_rect(
                            center=(row.xPos + self.midWidth / 2 + 150, row.yPos + self.midHeight / 2 + 25))

                self.screen.blit(category_text, category_text_rect)

            timer_text = self.timer_font.render(str(timer) + "%", True, (0, 0, 0))
            text_rect = (self.midWidth - (self.settingCatWidth + 35), 37)
            self.screen.blit(timer_text, text_rect)

            score_text = self.score_font.render(str(score), True, (0, 0, 0))
            text_rect = (self.midWidth + 10 + self.settingCatWidth, 33)
            self.screen.blit(score_text, text_rect)

        else:

            self.screen.fill(self.colour)

            self.restartCategory.draw_rectangle()

            self.screen.blit(self.loadedEndOverlay, (0, 0))

            score_text = self.end_font.render(str(score), True, (0, 0, 0))
            text_rect = score_text.get_rect(center=(self.midWidth, (self.height / 2) + 55))
            self.screen.blit(score_text, text_rect)

    def end_game(self, score):

        for i in range(255):
            text = self.end_font.render(str(score), True, (0, 0, 0))
            text.set_alpha(i)
            text_rect = text.get_rect(center=(self.midWidth, (self.height / 2) + 55))

            self.loadedEndOverlay.set_alpha(i)

            self.screen.blit(self.loadedEndOverlay, (0, 0))
            self.screen.blit(text, text_rect)
            pygame.display.flip()
            pygame.time.delay(1)


class Cursor:
    def __init__(self):

        """
        initialises all the data to be used for handling the cursor and its actions
        """

        self.defaultCursor = "resources/cursor/wii-open.png"
        self.actionCursor = "resources/cursor/wii-grab.png"
        self.pointCursor = "resources/cursor/wii-point.png"
        self.loadedCursor = pygame.image.load(self.defaultCursor).convert_alpha()
        self.xPos = 0
        self.yPos = 0

    def set_cursor(self, rectangle, settings, game_active):

        """
        :param settings:
        :param rectangle:
        :return handles the movement of the rectangle on screen according to the mouse actions:
        """
        if game_active:
            if rectangle.dragging:
                self.loadedCursor = pygame.image.load(self.actionCursor).convert_alpha()
            else:
                self.loadedCursor = pygame.image.load(self.defaultCursor).convert_alpha()
        elif not game_active:
            if settings.restartCategory.categoryRectangle.collidepoint(pygame.mouse.get_pos()):
                self.loadedCursor = pygame.image.load(self.pointCursor).convert_alpha()
            elif settings.exitCategory.categoryRectangle.collidepoint(pygame.mouse.get_pos()):
                self.loadedCursor = pygame.image.load(self.pointCursor).convert_alpha()
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
        self.colour_array = [self.PURPLE, self.RED, self.GREEN, self.BLUE]

    def rand_colour(self):
        return random.choice(self.colour_array)


class Category(Rectangle):
    def __init__(self, surface, x_pos, y_pos, length, width, colour, category):
        """
        :param surface:
        :param x_pos:
        :param y_pos:
        :param length:
        :param width:
        :param colour:
        :param category:
        handles the drawing of category rectangles (to recognise collisions with the game piece)
        """

        super().__init__(surface, x_pos, y_pos, length, width, colour)
        self.category = category
        self.categoryRectangle = pygame.rect.Rect(self.xPos, self.yPos, self.length, self.width)


class Questions:
    def __init__(self):
        """
        loads the questions file and handles question processing.
        """

        self.questions_data = []
        self.active_rectangle = None
        self.active_question = None
        self.loaded_question_image = None

        with open('resources/question/questions.csv', 'r') as file:
            reader = csv.reader(file)
            for row in reader:
                self.questions_data.append(row)

        self.questions_data.pop(0)

    def new_question(self, settings, colours):
        self.active_rectangle = Rectangle(settings.screen,
                                          settings.midWidth - 275,
                                          settings.midHeight - 80,
                                          160, 160,
                                          None)

        return self.active_rectangle

    def assign_questions(self, settings, category_rectangles):

        random_question = random.choice(self.questions_data)
        self.active_rectangle.category = random_question[5]
        self.active_question = random_question[0]
        self.loaded_question_image = pygame.image.load(random_question[6]).convert_alpha()

        # adjust the longer side to the length of the rectangle
        if self.loaded_question_image.get_width() > self.loaded_question_image.get_height():
            self.loaded_question_image = pygame.transform.scale(self.loaded_question_image, (400, 300))
        else:
            self.loaded_question_image = pygame.transform.scale(self.loaded_question_image, (400, 300))

        options = []

        for i in range(4):
            options.append(random_question[i + 1])
            category_rectangles[i].category = options[i]
