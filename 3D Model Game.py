import pygame
import os
import time
import random

pygame.font.init()

WIDTH, HEIGHT = 750, 750
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("3D Model")
#load images

#background
BG = pygame.transform.scale(pygame.image.load(os.path.join("Assets", "background", "background-black.png")),
                            (WIDTH, HEIGHT)
                            )

#Load Shapes
SQUARE = pygame.image.load(os.path.join("Assets/shapes", "square.png"))
RECTANGLE = pygame.image.load(os.path.join("Assets/shapes", "rectangle.png"))
CIRCLE = pygame.image.load(os.path.join("Assets/shapes", "circle.png"))
TRIANGLE = pygame.image.load(os.path.join("Assets/shapes", "triangle.png"))

#player ship
PLAYER_SHIP = pygame.image.load(os.path.join("Assets/ships", "pixel_ship_yellow.png"))

# lasers
RED_LASER = pygame.image.load(os.path.join("Assets/lasers", "pixel_laser_red.png"))
GREEN_LASER = pygame.image.load(os.path.join("Assets/lasers", "pixel_laser_green.png"))
BLUE_LASER = pygame.image.load(os.path.join("Assets/lasers", "pixel_laser_blue.png"))
YELLOW_LASER = pygame.image.load(os.path.join("Assets/lasers", "pixel_laser_yellow.png"))


class Character:
    def __init__(self, x, y, health=100):
        self.x = x
        self.y = y
        self.health = health
        self.character_img = None
        self.laser_img = None
        self.lasers = []
        self.cool_down_counter = 0

    def draw(self, window):
        window.blit(self.character_img, (self.x, self.y))

    def get_width(self):
        return self.character_img.get_width()

    def get_height(self):
        return self.character_img.get_height()


class Player(Character):
    def __init__(self, x, y, health=100):
        super().__init__(x, y, health)
        self.character_img = PLAYER_SHIP
        self.laser_img = YELLOW_LASER
        self.mask = pygame.mask.from_surface(self.character_img)
        self.max_health = health


class Enemy(Character):
    SHAPE_MAP = {
        "square": (SQUARE, RED_LASER),
        "rectangle": (RECTANGLE, RED_LASER),
        "circle": (CIRCLE, BLUE_LASER),
        "triangle": (TRIANGLE, GREEN_LASER)
    }

    def __init__(self, x, y, shape, health=100):
        super().__init__(x, y, health)
        self.character_img, self.laser_img = self.SHAPE_MAP[shape]
        self.mask = pygame.mask.from_surface(self.character_img)

    def move(self, vel):
        self.y += vel


def main():
    running = True
    fps = 60
    lost = False
    level = 0
    lives = 3
    main_font = pygame.font.SysFont("arial", 50)
    enemies = []
    wave_length = 5
    enemy_vel = 1
    player_vel = 5
    boundaries = [0, WIDTH, 0, HEIGHT * 0.25]
    player = Player(300, 650)

    clock = pygame.time.Clock()

    # Function To Handle Drawing
    def redraw_window():
        WIN.blit(BG, (0, 0))
        # draw text
        lives_label = main_font.render(f"Lives: {lives}", 1, (255, 0, 0))
        levels_label = main_font.render(f"Level: {level}", 1, (255, 0, 0))

        WIN.blit(lives_label, (10, 10))
        WIN.blit(levels_label, (WIDTH - levels_label.get_width() - 10, 10))
        for enemy in enemies:
            enemy.draw(WIN)
        player.draw(WIN)
        pygame.display.update()

    while running:
        clock.tick(fps)

        if lives <= 0 or player.health <= 0:
            lost = True


        # TODO: Need to add in functionality when user reaches no lost state
        if lost:
            pass

        # TODO: Need to make sure that if the user selects the wrong shape then they lose life
        if len(enemies) == 0:
            level += 1
            wave_length +=5
            for i in range(wave_length):
                enemy = Enemy(random.randrange(50, WIDTH-100), random.randrange(-1500, - 100), random.choice(["square", "rectangle", "circle", "triangle"]))
                enemies.append(enemy)

        # Event Checker
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        keys = pygame.key.get_pressed()

        if keys[pygame.K_LEFT] and player.x - player_vel > 0:
            player.x -= player_vel

        if keys[pygame.K_RIGHT] and player.x + player_vel + player.get_width() < WIDTH:
            player.x += player_vel

        if keys[pygame.K_UP] and HEIGHT * 0.65 < player.y - player_vel > 0:
            player.y -= player_vel

        if keys[pygame.K_DOWN] and player.y + player_vel + player.get_height() < HEIGHT:
            player.y += player_vel

        for enemy in list(enemies):
            enemy.move(enemy_vel)
            if enemy.y + enemy.get_height() > HEIGHT:
                lives -= 1
                enemies.remove(enemy)

        redraw_window()

if __name__ == "__main__":
    main()