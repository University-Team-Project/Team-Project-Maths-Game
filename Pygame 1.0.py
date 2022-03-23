import sys
import pygame
from pygame.locals import *
from shapes import *
from settings import *

# gets the game settings and data from the classes in the setting and shapes py file
settings = Settings()
cursor = Cursor()
screen = settings.screen
colour = Colours()

# creates a new rectangle on the screen according to the variables given to the class
rectangle = Rectangle(screen, 176, 134, 50, 50, colour.PURPLE)

# game loop.
while True:

    screen.fill(colour.WHITE)

    # event handler
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                if rectangle.pygameRectangle.collidepoint(event.pos):
                    rectangle.dragging = True
                    cursor.set_cursor(rectangle)
                    cursor.xPos, cursor.yPos = event.pos
                    offset_x = rectangle.xPos - cursor.xPos
                    offset_y = rectangle.yPos - cursor.yPos

        elif event.type == pygame.MOUSEBUTTONUP:
            cursor.set_cursor(rectangle)
            if event.button == 1:
                rectangle.dragging = False

        elif event.type == pygame.MOUSEMOTION:
            if rectangle.dragging:
                cursor.xPos, cursor.yPos = event.pos
                rectangle.xPos = cursor.xPos + offset_x
                rectangle.yPos = cursor.yPos + offset_y

    screen.fill(colour.WHITE)

    rectangle.draw_rectangle()

    cursor.set_cursor(rectangle)

    pygame.display.flip()

    # Update.

    # Draw.

    settings.fpsClock.tick(settings.fps)
