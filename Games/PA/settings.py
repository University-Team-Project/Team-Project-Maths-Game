import csv

import pygame
import random
import pygame_textinput


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
        self.background = pygame.transform.scale(pygame.image.load('resources/overlay/space_overlay.png'),
                                                 (1280, 720)).convert()
        self.endgame_background = pygame.transform.scale(pygame.image.load('resources/overlay/end_space_overlay.png'),
                                                         (1280, 720)).convert()
        self.midWidth = self.width / 2
        self.midHeight = self.height / 2
        self.objects = []
        self.colours = Colours()
        self.question = self.generate_question()
        self.timer, self.timer_text = 60, '60'.rjust(3)

        self.score_font = pygame.font.Font("resources/font/static/Inter-SemiBold.ttf", 40)
        self.timer_font = pygame.font.Font("resources/font/static/Inter-SemiBold.ttf", 40)
        self.question_font = pygame.font.Font("resources/font/static/Inter-SemiBold.ttf", 60)
        self.label_font = pygame.font.Font("resources/font/static/Inter-SemiBold.ttf", 15)

        self.saved = False

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
        rectangle = Rectangle(self.screen, True, self.screen.get_rect().centerx - length / 2,
                              (self.screen.get_rect().centery - height / 2) - 40, length, height,
                              self.colours.completely_random_colour())
        self.objects = [rectangle.answer]
        self.question = rectangle

        pos_choice = [[170, 128], [1110, 128], [170, 470], [1110, 470]]
        temp = random.choice(pos_choice)
        pos_choice.remove(temp)
        rectangle.answer.xPos, rectangle.answer.yPos = temp[0], temp[1]
        random.shuffle(pos_choice)
        if rectangle.choice == "Area":
            answer_choice = random.sample(range(1, 10), 3)
            for i in pos_choice:
                self.objects.append(
                    Answer(str(answer_choice[pos_choice.index(i)] + int(rectangle.answer.text[:-3])) + "cm²",
                           self.screen, False, i[0], i[1]))
        else:
            answer_choice = random.sample(range(1, 10), 3)
            for i in pos_choice:
                self.objects.append(
                    Answer(str(answer_choice[pos_choice.index(i)] + int(rectangle.answer.text[:-2])) + "cm",
                           self.screen, False, i[0], i[1]))

        self.objects.append(rectangle)  # Added to the list last so that it is drawn last so it is on top.
        return rectangle

    def correct_answer(self, pos):
        self.objects = []
        self.score += 1
        self.generate_question()

    def incorrect_answer(self, pos):
        self.objects = []
        self.timer -= 1
        self.timer_text = str(self.timer).rjust(3)
        self.generate_question()

    def save_score(self, player):
        if not self.saved:
            with open('Scores.csv', 'a+', newline='') as csv_file:
                writer = csv.writer(csv_file)
                writer.writerow(["mental-matchup", player.title(), self.score])
            self.saved = True


class Cursor:
    def __init__(self, screen):

        """
        initialises all the data to be used for handling the cursor and its actions
        """
        self.screen = screen
        self.defaultCursor = "resources/cursor/wii-open.png"
        self.actionCursor = "resources/cursor/wii-grab.png"
        self.hoverCursor = "resources/cursor/wii-point.png"
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

    def set_hover(self, hovering):
        if hovering:
            self.loadedCursor = pygame.image.load(self.hoverCursor).convert_alpha()
            return
        self.loadedCursor = pygame.image.load(self.defaultCursor).convert_alpha()

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
            self.answer = Answer(str(self.estimated_area) + "cm²", self.surface, False, random.randint(100, 1100),
                                 random.randint(600, 600))
        else:
            self.answer = Answer(str(self.estimated_perimeter) + "cm", self.surface, False, random.randint(100, 1100),
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


class Text(Object):
    def __init__(self, text, font_size, surface, draggable, xPos, yPos):
        super().__init__(surface, draggable, xPos, yPos)
        self.text = text
        self.font = pygame.font.Font("resources/font/static/Inter-SemiBold.ttf", font_size)
        self.place_text = self.font.render(self.text, True, (0, 0, 0))
        self.pygameRectangle = self.place_text.get_rect(center=(self.xPos, self.yPos))

    def draw(self, game):
        self.place_text = self.font.render(self.text, True, (0, 0, 0))
        self.pygameRectangle = self.place_text.get_rect(center=(self.xPos, self.yPos))
        self.surface.blit(self.place_text, self.pygameRectangle)


class Category(Rectangle):
    def __init__(self, surface, xPos, yPos, length, height, colour, draggable, category):
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


class TextInput:
    def __init__(self, text, font_size, screen, xPos, yPos):
        self.text = text
        self.font = pygame.font.Font("resources/font/static/Inter-SemiBold.ttf",
                                     font_size)  # Requires font in resource folder.
        self.screen = screen
        self.xPos = xPos
        self.yPos = yPos
        self.active = False
        self.active_colour = pygame.Color('lightskyblue3')
        self.passive_colour = pygame.Color('chartreuse4')
        self.colour = self.passive_colour
        self.input_rect = pygame.Rect(xPos, yPos, 140, 32)
        self.text_surface = self.font.render(self.text, True, (255, 255, 255))
        self.visible = True

    def check_active(self, event):
        if self.input_rect.collidepoint(event.pos):
            self.active = True
            self.colour = self.active_colour
        else:
            self.active = False
            self.colour = self.passive_colour

    def update_text(self, event):
        if self.active:
            print(self.text)
            if event.type == pygame.KEYDOWN:

                # Check for backspace
                if event.key == pygame.K_BACKSPACE:

                    # get text input from 0 to -1 i.e. end.
                    self.text = self.text[:-1]

                # Unicode standard is used for string
                # formation
                else:
                    self.text += event.unicode
                if event.key == pygame.K_RETURN:
                    self.visible = False
                    self.active = False
        self.text_surface = self.font.render(self.text, True, (255, 255, 255))

    def draw(self):
        if self.visible:
            pygame.draw.rect(self.screen, self.colour, self.input_rect)
            self.screen.blit(self.text_surface, (self.input_rect.x + 5, self.input_rect.y + 5))
            self.input_rect.w = max(100, self.text_surface.get_width() + 10)
