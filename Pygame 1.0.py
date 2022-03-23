import sys
import pygame
from pygame.locals import *
from shapes import *
pygame.init()

pygame.display.set_caption('Drag & Drop')

fps = 60
fpsClock = pygame.time.Clock()

width, height = 1280, 720
screen = pygame.display.set_mode((width, height))

WHITE = (255, 255, 255)
PURPLE = (128, 0, 128)

rectangle = Rectangle(screen, 176, 134, 50, 50, PURPLE)

mouseFlag = False
defaultCursor = "resources/wii-open.png"
actionCursor = "resources/wii-grab.png"
loadedCursor = pygame.image.load(defaultCursor).convert_alpha()

pygame.mouse.set_visible(False)


def handle_mouse_render(flag, default_cursor, action_cursor):

    if flag:
        loaded_cursor = pygame.image.load(action_cursor).convert_alpha()
    else:
        loaded_cursor = pygame.image.load(default_cursor).convert_alpha()

    x, y = pygame.mouse.get_pos()
    x -= loaded_cursor.get_width() / 2
    y -= loaded_cursor.get_height() / 2

    screen.blit(loaded_cursor, (x, y))


# Game loop.
while True:
    screen.fill((0, 0, 0))

    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                if rectangle.pygameRectangle.collidepoint(event.pos):
                    mouseFlag = True
                    handle_mouse_render(mouseFlag, defaultCursor, actionCursor)
                    rectangle.dragging = True
                    mouse_x, mouse_y = event.pos
                    offset_x = rectangle.xPos - mouse_x
                    offset_y = rectangle.yPos - mouse_y

        elif event.type == pygame.MOUSEBUTTONUP:
            mouseFlag = False
            handle_mouse_render(mouseFlag, defaultCursor, actionCursor)
            if event.button == 1:
                rectangle.dragging = False

        elif event.type == pygame.MOUSEMOTION:
            if rectangle.dragging:
                mouse_x, mouse_y = event.pos
                rectangle.xPos = mouse_x + offset_x
                rectangle.yPos = mouse_y + offset_y

    screen.fill(WHITE)

    rectangle.drawRectangle()

    handle_mouse_render(mouseFlag, defaultCursor, actionCursor)

    pygame.display.flip()

    # Update.

    # Draw.

    pygame.display.flip()
    fpsClock.tick(fps)
