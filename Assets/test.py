import pygame

pygame.init()
screen = pygame.display.set_mode((1080, 720))
pygame.display.set_caption("White Transition testing")

# transition_surface = pygame.image.load("YOUR_IMAGE.PNG").convert()
# or use the following code for testing
# -----------------------------------------------------------------
transition_surface = pygame.image.load("TITLESCREEN.png").convert()
# -----------------------------------------------------------------

clock = pygame.time.Clock()
STOP_GAME = True
# Start here with full opacity
alpha_value = 255
transition_surface.set_alpha(alpha_value)

MAX_FPS = 60

pygame_display_flip = pygame.display.flip
screen_fill = screen.fill
event_pump = pygame.event.pump
key_pressed = pygame.key.get_pressed
screen_blit = screen.blit
transition_surface_set_alpha = transition_surface.set_alpha
busy_loop = clock.tick_busy_loop

while STOP_GAME:

    screen_fill((0, 0, 0, 0))

    event_pump()
    keys = key_pressed()
    if keys[pygame.K_ESCAPE]:
        STOP_GAME = False

    if alpha_value > 0:
        screen_blit(transition_surface, (0, 0))
        alpha_value -= 1
        if alpha_value <= 0:
            alpha_value = 0
        transition_surface_set_alpha(alpha_value)

    busy_loop(MAX_FPS)
    pygame_display_flip()


pygame.quit()
