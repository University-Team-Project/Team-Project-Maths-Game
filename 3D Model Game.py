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

#Load Models
CUBE = pygame.transform.scale(pygame.image.load(os.path.join("Assets/models", "cube.png")), (50, 50))
CUBOID = pygame.transform.scale(pygame.image.load(os.path.join("Assets/models", "cuboid.png")), (50, 50))
TRI_PRISM = pygame.transform.scale(pygame.image.load(os.path.join("Assets/models", "triangular_prism.png")), (50, 50))

MODEL_MAP = {
        "cube": (CUBE, {SQUARE, SQUARE, SQUARE, SQUARE, SQUARE, SQUARE}),
        "cuboid": (CUBOID, {RECTANGLE, RECTANGLE, RECTANGLE, RECTANGLE, RECTANGLE, RECTANGLE}),
        "triangular_prism": (TRI_PRISM, {TRIANGLE, TRIANGLE, RECTANGLE, RECTANGLE, RECTANGLE})
    }

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


class Laser:
    def __init__(self, x, y, laser):
        self.x = x
        self.y = y
        self.laser_img = laser

    def draw(self, window):
        window.blit(self.laser_img, (self.x, self.y))

def collide(obj1, obj2):
    offset_x = obj2.x - obj1.x
    offset_y = obj2.y - obj1.y
    return obj1.mask.overlap(obj2.mask, (offset_x, offset_y)) != None

def main():
    running = True
    fps = 60
    main_font = pygame.font.SysFont("arial", 50)
    lost_font = pygame.font.SysFont("arial", 60)
    round = 1
    level = 0
    lives = 3
    lost = False
    win = True
    won_round = False
    model, model_shapes = MODEL_MAP[random.choice(["cube", "cuboid", "triangular_prism"])]
    enemies = []
    wave_length = 5
    enemy_vel = 1
    player_vel = 5
    player = Player(300, 650)

    clock = pygame.time.Clock()

    # Function To Handle Drawing
    def redraw_window():
        WIN.blit(BG, (0, 0))
        # draw text
        lives_label = main_font.render(f"Lives: {lives}", 1, (255, 0, 0))
        levels_label = main_font.render(f"Level: {level}", 1, (255, 0, 0))

        WIN.blit(lives_label, (10, 10))
        WIN.blit(model, (WIDTH/2, 10))
        WIN.blit(levels_label, (WIDTH - levels_label.get_width() - 10, 10))

        for e in enemies:
            e.draw(WIN)
        player.draw(WIN)
        pygame.display.update()

    while running:
        clock.tick(fps)

        if lives <= 0 or player.health <= 0:
            lost = True

        if won_round:
            if round > 3:
                win = True
            else:
                model, model_shapes = MODEL_MAP[random.choice(["cube", "cuboid", "triangular_prism"])]
                round += 1

            won_round = False

        # TODO: Need to add in functionality when user reaches no lost state
        if lost:
            lost_label = lost_font.render("Game Over", 1, (255, 255, 255))
            WIN.blit(lost_label, (WIDTH/2 - lost_label.get_width()/2, 350))

        # TODO: Need to make sure that if the user selects the wrong shape then they lose life
        if len(enemies) == 0:
            if level <= 2:
                level += 1
                wave_length += 5
                height = 0
                width = 0
                for i in range(wave_length):
                    for e in enemies:
                        while True:
                            height = random.randrange(-1500, - 100)
                            width = random.randrange(50, WIDTH - 100)
                            new_rect = pygame.Rect(width, height, e.get_width(), e.get_height())

                            if not any(enmey for enmey in enemies if
                                       new_rect.colliderect(enmey.x, enmey.y, enmey.get_width(),enmey.get_height())):
                                break

                    enemy = Enemy(width, height, random.choice(["square", "rectangle", "circle", "triangle"]))
                    enemies.append(enemy)
            else:
                won_round = True
                level = 0
                wave_length = 5



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
            if enemy.y + enemy.get_height() > HEIGHT and enemy.character_img in model_shapes:
                lives -= 1

            if enemy.y + enemy.get_height() > HEIGHT:
                enemies.remove(enemy)

        redraw_window()

if __name__ == "__main__":
    main()