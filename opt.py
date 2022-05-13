import pygame
pygame.init()



def blit_rotate_center(win, image, top_left, angle):
    rotated_image = pygame.transform.rotate(image, angle)
    new_rect = rotated_image.get_rect(center=image.get_rect(topleft=top_left).center)
    win.blit(rotated_image, new_rect.topleft)


def scale_image(img, factor):
    size = round(img.get_width() * factor), round(img.get_height() * factor)
    return pygame.transform.scale(img, size)


def blit_text_center(win, font, text):
    pygame.font.init()
    render = font.render(text, 1, (0, 0, 0))
    win.blit(render, (win.get_width()/2 - render.get_width()/2, win.get_height()/2 - render.get_height()/2))


def blit_question_top(win, font, text):
    render = font.render(text, 1, (0, 0, 0))
    win.blit(render, (win.get_width()/2 - render.get_width()/2, (win.get_height()/8 - render.get_height()/2) + 100))
    # win.blit(render, (win.get_width() / 2 - render.get_width() / 2, 200 - render.get_height() / 2))

def blit_question_text_top(win, font, text):
    render = font.render(text, 1, (0, 0, 0))
    win.blit(render, (win.get_width()/2 - render.get_width()/2, (win.get_height()/8 - render.get_height()/2) + 50))

def blit_text_top(win, font, text):
    render = font.render(text, 1, (0, 0, 0))
    win.blit(render, (win.get_width()/2 - render.get_width()/2, (win.get_height()/8 - render.get_height()/2) - 60))
    # win.blit(render, (win.get_width() / 2 - render.get_width() / 2, 200 - render.get_height() / 2))


def blit_text_top_left(win, font, text):
    pygame.font.init()
    render = font.render(text, 1, (0, 0, 0))
    # win.blit(render, (win.get_width()/2 - render.get_width()/2, win.get_height()/2 - render.get_height()/2))
    # win.blit(render, (win.get_width() / 5 - render.get_width() / 2, win.get_height() / 2.5 - render.get_height() / 2))
    win.blit(render, (182.5 - render.get_width() / 2, 149 - render.get_height() / 2))


def blit_text_top_right(win, font, text):
    pygame.font.init()
    render = font.render(text, 1, (0, 0, 0))
    # win.blit(render, (win.get_width()/2 - render.get_width()/2, win.get_height()/2 - render.get_height()/2))
    # win.blit(render, (win.get_width() / 1.5 - render.get_width() / 2, win.get_height() / 2.5 - render.get_height() / 2))
    win.blit(render, (win.get_width() - 182.5 - render.get_width() / 2, 149 - render.get_height() / 2))


def blit_text_bottom_left(win, font, text):
    pygame.font.init()
    render = font.render(text, 1, (0, 0, 0))
    # win.blit(render, (win.get_width()/2 - render.get_width()/2, win.get_height()/2 - render.get_height()/2))
    # win.blit(render, (win.get_width() / 5 - render.get_width() / 2, win.get_height() / 2 - render.get_height() / 2))
    win.blit(render, (182.5 - render.get_width() / 2, win.get_height() - 149 - render.get_height() / 2))


def blit_text_bottom_right(win, font, text):
    pygame.font.init()
    render = font.render(text, 1, (0, 0, 0))
    # win.blit(render, (win.get_width()/2 - render.get_width()/2, win.get_height()/2 - render.get_height()/2))
    # win.blit(render, (win.get_width() / 1.5 - render.get_width() / 2, win.get_height() / 2 - render.get_height() / 2))
    win.blit(render, (win.get_width() - 182.5 - render.get_width() / 2, win.get_height() - 149 - render.get_height() / 2))

def blit_text_player_one_score(win, font, text):
    pygame.font.init()
    render = font.render(text, 1, (0, 0, 0))
    win.blit(render, (425 - render.get_width() / 2, 30 - render.get_height() / 2))

def blit_text_player_two_score(win, font, text):
    pygame.font.init()
    render = font.render(text, 1, (0, 0, 0))
    win.blit(render, (865 - render.get_width() / 2, 30 - render.get_height() / 2))

def blit_timer_text(win, font, text):
    pygame.font.init()
    render = font.render(text, 1, (0, 0, 0))
    win.blit(render, (win.get_width()/2 - render.get_width()/2, (win.get_height()/2 - 165 - render.get_height()/2) + 50))

def blit_player1_scoreboard(win, font, text):
    pygame.font.init()
    render = font.render(text, 1, (0, 0, 0))
    win.blit(render, (win.get_width()/2 - render.get_width()/2, (win.get_height()/2 - render.get_height()/2) - 200))

def blit_player2_scoreboard(win, font, text):
    pygame.font.init()
    render = font.render(text, 1, (0, 0, 0))
    win.blit(render, (win.get_width()/2 - render.get_width()/2, (win.get_height()/2 - render.get_height()/2) - 150))
