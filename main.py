import sys
from pygame import *
from shapes import *
from settings import *

'''
Initalized settings
'''
colour = Colours()
settings = Settings(colour)
cursor = Cursor()
screen = settings.screen


def game_loop():
    # creates a new rectangle on the screen according to the variables given to the class
    rectangle = Rectangle(screen, 176, 134, 50, 50, colour.PURPLE)
    # game loop.
    score = 0
    category_rectangles = [settings.category1,
                           settings.category2,
                           settings.category3,
                           settings.category4]
    while True:

        settings.screen_tick(colour)

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
                    for i in category_rectangles:
                        if rectangle.category == i.category:
                            if rectangle.pygameRectangle.colliderect(i.categoryRectangle):
                                score += 1
                                print(score) # Currently works (NOT SURE HOW SCALABLE).





            elif event.type == pygame.MOUSEMOTION:
                if rectangle.dragging:
                    cursor.xPos, cursor.yPos = event.pos
                    rectangle.xPos = cursor.xPos + offset_x
                    rectangle.yPos = cursor.yPos + offset_y

        rectangle.draw_rectangle()

        cursor.set_cursor(rectangle)

        pygame.display.flip()

        settings.fpsClock.tick(settings.fps)


if __name__ == '__main__':
    game_loop()
