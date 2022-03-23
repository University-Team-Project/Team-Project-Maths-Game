import sys
import pygame
from pygame.locals import *
from shapes import *
from settings import *

settings = Settings()
cursor = Cursor()
screen = settings.screen
colour = Colours()


rectangle = Rectangle(screen, 176, 134, 50, 50, colour.PURPLE)

mouseFlag = False
pygame.mouse.set_visible(False)


# Game loop.
while True:
    screen.fill(colour.WHITE)

    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                if rectangle.pygameRectangle.collidepoint(event.pos):
                    rectangle.dragging = True
                    cursor.setCursor(rectangle)
                    mouse_x, mouse_y = event.pos
                    offset_x = rectangle.xPos - mouse_x
                    offset_y = rectangle.yPos - mouse_y

        elif event.type == pygame.MOUSEBUTTONUP:
            cursor.setCursor(rectangle)
            if event.button == 1:
                rectangle.dragging = False

        elif event.type == pygame.MOUSEMOTION:
            if rectangle.dragging:
                mouse_x, mouse_y = event.pos
                rectangle.xPos = mouse_x + offset_x
                rectangle.yPos = mouse_y + offset_y

    screen.fill(colour.WHITE)

    rectangle.drawRectangle()

    cursor.setCursor(rectangle)

    pygame.display.flip()

    # Update.

    # Draw.

    pygame.display.flip()
    settings.fpsClock.tick(settings.fps)
