import pygame
import os
import time
import math

# Size of the cars
CAR_WIDTH, CAR_HEIGHT = 55, 40
# Loading of the Car images
RED_CAR_IMAGE = pygame.image.load(os.path.join('Assets', 'Car_Cartoon_2.png'))
RED_CAR = pygame.transform.scale(RED_CAR_IMAGE, (CAR_WIDTH, CAR_HEIGHT))

BACKGROUND = pygame.image.load(os.path.join('Assets', 'TEST Car background.png'))

# Size of the window
WIDTH, HEIGHT = BACKGROUND.get_width(), BACKGROUND.get_height()
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
# Sets the name for the window
pygame.display.set_caption("Driving Maths Game")


# FPS of the game
FPS = 60
# Velocity of the cars
VEL = 5


def red_car_handle_movement(keys_pressed, red_car):
    if keys_pressed[pygame.K_LEFT]:  # LEFT
        red_car.x -= VEL
    if keys_pressed[pygame.K_RIGHT]:  # RIGHT
        red_car.x += VEL
    if keys_pressed[pygame.K_UP]:  # UP
        red_car.y -= VEL
    if keys_pressed[pygame.K_DOWN]:  # DOWN
        red_car.y += VEL


def draw_window(red_car):
    WIN.fill(GREY)
    WIN.blit(RED_CAR, (red_car.x, red_car.y))
    pygame.display.update()


def draw(win, images, red_car):
    for img, pos in images:
        win.blit(img, pos)

    win.blit(red_car)


def main():
    red_car = pygame.Rect(700, 300, CAR_WIDTH, CAR_HEIGHT)
    images = [(BACKGROUND, (0, 0))]

    clock = pygame.time.Clock()
    run = True
    while run:
        clock.tick(FPS)

        draw(WIN, images, red_car)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()

        keys_pressed = pygame.key.get_pressed()
        red_car_handle_movement(keys_pressed, red_car)
        # draw_window(red_car)

    #main()


if __name__ == "__main__":
    main()
