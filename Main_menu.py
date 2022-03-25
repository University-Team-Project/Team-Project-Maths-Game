import pygame
import pygame_menu

pygame.init()
screen = pygame.display.set_mode((1080, 720))
pygame.display.set_caption("Main Menu")

title_surface = pygame.image.load("Assets/TITLESCREEN.png").convert()

def game_choice(value, choice):
    # Do stuff
    pass
#new test

def start_the_game():
    # Do stuff
    pass


font = pygame_menu.font.FONT_FRANCHISE
purple_background = pygame_menu.baseimage.BaseImage(
    image_path="Assets/Background_purple.png",
    drawing_mode=pygame_menu.baseimage.IMAGE_MODE_REPEAT_XY,
)


my_theme = pygame_menu.themes.THEME_DEFAULT.copy()
my_theme.background_color = purple_background
my_theme.title_bar_style = pygame_menu.widgets.MENUBAR_STYLE_NONE
my_theme.title_offset = (430, 90)
my_theme.title_font_color = (210, 166, 255)
my_theme.widget_font_color = (210, 166, 255)
my_theme.widget_font = font
my_theme.title_font = font
my_theme.title_font_size = 144
my_theme.widget_font_size = 72
my_theme.selection_color = (70, 255, 225)
menu = pygame_menu.Menu('TITLE', 1080, 720, theme=my_theme)


menu.add.text_input('NAME : ', default='John Doe')
menu.add.selector('GAME CHOICE : ', [('GAME 1', 1), ('GAME 2', 2),
                                     ("GAME 3", 3), ("GAME 4", 4),
                                     ("GAME 5", 5), ("GAME 6", 6)], onchange=game_choice)
menu.add.button('PLAY', start_the_game)
menu.add.button('QUIT', pygame_menu.events.EXIT)

menu.mainloop(screen)
