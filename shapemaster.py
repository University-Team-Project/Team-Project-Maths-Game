import pygame
import os
import time
import random

pygame.font.init()

WIDTH, HEIGHT = 1280, 720
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("3D Model")
#load images

#background
BG = pygame.transform.scale(pygame.image.load(os.path.join("Assets", "background", "background-black.png")),
                            (WIDTH, HEIGHT)
                            )
#
#Load Shapes
SQUARE = pygame.image.load(os.path.join("Assets/shapes", "square.png"))
PENTAGON = pygame.image.load(os.path.join("Assets/shapes", "pentagon.png"))
RECTANGLE = pygame.image.load(os.path.join("Assets/shapes", "rectangle.png"))
CIRCLE = pygame.image.load(os.path.join("Assets/shapes", "circle.png"))
TRIANGLE = pygame.image.load(os.path.join("Assets/shapes", "triangle.png"))

#Load Models
CUBE = pygame.transform.scale(pygame.image.load(os.path.join("Assets/models", "cube.png")), (50, 50))
#SPHERE = pygame.transform.scale(pygame.image.load(os.path.join("Assets/models", "sphere.png")), (50, 50))
OCTAHEDRON = pygame.transform.scale(pygame.image.load(os.path.join("Assets/models", "octahedron.png")), (50, 50))
DODECAHEDRON = pygame.transform.scale(pygame.image.load(os.path.join("Assets/models", "dodecahedron.png")), (50, 50))
ICOSAHEDRON = pygame.transform.scale(pygame.image.load(os.path.join("Assets/models", "icosahedron.png")), (50, 50))
TETRAHEDRON = pygame.transform.scale(pygame.image.load(os.path.join("Assets/models", "tetrahedron.png")), (50, 50))
#CUBOID = pygame.transform.scale(pygame.image.load(os.path.join("Assets/models", "cuboid.png")), (50, 50))
#TRI_PRISM = pygame.transform.scale(pygame.image.load(os.path.join("Assets/models", "triangular_prism.png")), (50, 50))

MODEL_MAP = {
    "cube": (CUBE, [SQUARE, SQUARE, SQUARE, SQUARE, SQUARE, SQUARE]),
    "tetrahedron": (TETRAHEDRON, [TRIANGLE, TRIANGLE, TRIANGLE, TRIANGLE]),
    "octahedron": (OCTAHEDRON, [TRIANGLE, TRIANGLE, TRIANGLE, TRIANGLE, TRIANGLE, TRIANGLE, TRIANGLE, TRIANGLE]),
    "dodecahedron": (DODECAHEDRON, [PENTAGON, PENTAGON, PENTAGON, PENTAGON, PENTAGON, PENTAGON, PENTAGON, PENTAGON, PENTAGON, PENTAGON, PENTAGON, PENTAGON]),
    "icosahedron":(ICOSAHEDRON, [TRIANGLE, TRIANGLE, TRIANGLE, TRIANGLE,TRIANGLE, TRIANGLE, TRIANGLE, TRIANGLE,TRIANGLE, TRIANGLE, TRIANGLE, TRIANGLE, TRIANGLE, TRIANGLE, TRIANGLE, TRIANGLE,TRIANGLE, TRIANGLE, TRIANGLE, TRIANGLE])
    }

#player ship
PLAYER_SHIP = pygame.image.load(os.path.join("Assets/ships", "pixel_ship_yellow.png"))

# lasers
RED_LASER = pygame.image.load(os.path.join("Assets/lasers", "pixel_laser_red.png"))
GREEN_LASER = pygame.image.load(os.path.join("Assets/lasers", "pixel_laser_green.png"))
BLUE_LASER = pygame.image.load(os.path.join("Assets/lasers", "pixel_laser_blue.png"))
YELLOW_LASER = pygame.image.load(os.path.join("Assets/lasers", "pixel_laser_yellow.png"))


class Character:
    COOLDOWN = 30

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
        for laser in self.lasers:
            laser.draw(window)

    def move_lasers(self, vel, obj):
        self.cooldown()
        for laser in self.lasers:
            laser.move(vel)
            if laser.off_screen(HEIGHT):
                self.lasers.remove(laser)
            elif laser.collision(obj):
                obj.health -= 10
                self.lasers.remove(laser)

    def cooldown(self):
        if self.cool_down_counter >= self.COOLDOWN:
            self.cool_down_counter = 0
        elif self.cool_down_counter > 0:
            self.cool_down_counter += 1

    def shoot(self):
        if self.cool_down_counter == 0:
            laser = Laser(self.x, self.y, self.laser_img)
            self.lasers.append(laser)
            self.cool_down_counter = 1

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
        self.lives = 3

    def move_lasers(self, vel, objs, shapes_score, model_shapes):
        self.cooldown()
        for laser in self.lasers:
            laser.move(vel)
            if laser.off_screen(HEIGHT):
                self.lasers.remove(laser)
            else:
                for obj in objs:
                    if laser.collision(obj):
                        if obj.character_img in model_shapes:
                            shapes_score += 1
                            model_shapes.remove(obj.character_img)
                        else:
                            self.lives -= 1
                        objs.remove(obj)
                        if laser in self.lasers:
                            self.lasers.remove(laser)
        return (shapes_score, model_shapes, )

    def draw(self, window):
        super().draw(window)
        self.healthbar(window)

    def healthbar(self, window):
        pygame.draw.rect(window, (255,0,0), (self.x, self.y + self.character_img.get_height() + 10, self.character_img.get_width(), 10))
        pygame.draw.rect(window, (0,255,0), (self.x, self.y + self.character_img.get_height() + 10, self.character_img.get_width() * (self.health/self.max_health), 10))


class Enemy(Character):
    SHAPE_MAP = {
        "square": (SQUARE, RED_LASER),
        "triangle": (TRIANGLE, GREEN_LASER),
        "pentagon": (PENTAGON, BLUE_LASER)
    }

    def __init__(self, x, y, shape, health=100):
        super().__init__(x, y, health)
        self.character_img, self.laser_img = self.SHAPE_MAP[shape]
        self.mask = pygame.mask.from_surface(self.character_img)

    def move(self, vel):
        self.y += vel

    def shoot(self):
        if self.cool_down_counter == 0:
            laser = Laser(self.x-20, self.y, self.laser_img)
            self.lasers.append(laser)
            self.cool_down_counter = 1

class Laser:
    def __init__(self, x, y, laser):
        self.x = x
        self.y = y
        self.img = laser
        self.mask = pygame.mask.from_surface(self.img)

    def draw(self, window):
        window.blit(self.img, (self.x, self.y))

    def move(self, vel):
        self.y += vel

    def off_screen(self, height):
        return not(self.y <= height and self.y >= 0)

    def collision(self, obj):
        return collide(self, obj)

def collide(obj1, obj2):
    offset_x = obj2.x - obj1.x
    offset_y = obj2.y - obj1.y
    return obj1.mask.overlap(obj2.mask, (offset_x, offset_y)) != None

def main():
    running = True
    fps = 60
    main_font = pygame.font.SysFont("arial", 50)
    shape_font = pygame.font.SysFont("arial", 20)
    lost_font = pygame.font.SysFont("arial", 60)
    round = 1
    level = 1
    start = True
    lost = False
    win = False
    won_round = False
    model, model_shapes = MODEL_MAP["tetrahedron"]
    num_of_shapes = len(model_shapes)
    shapes_score = 0
    score = 0
    enemies = []
    prev_enemy_type = ""
    wave_length = 5
    enemy_vel = 1
    player_vel = 5
    laser_vel = 5
    player = Player(WIDTH/2 - PLAYER_SHIP.get_width()/2, 600)

    clock = pygame.time.Clock()

    # Function To Handle Drawing
    def redraw_window():
        WIN.blit(BG, (0, 0))
        # draw text
        start_label = lost_font.render("Press Any Key To Start", 1, (255,255,255))
        lives_label = main_font.render(f"Lives: {player.lives}", 1, (255, 0, 0))
        shapes_score_label = shape_font.render(f"Faces: {shapes_score} / {num_of_shapes}", 1, (255, 0, 0))
        levels_label = main_font.render(f"Level: {level}", 1, (255, 0, 0))
        lost_label = lost_font.render("Game Over", 1, (255, 255, 255))
        win_label = lost_font.render("You Win!", 1, (255, 255, 255))

        WIN.blit(lives_label, (10, 10))
        WIN.blit(model, ((WIDTH - model.get_width())/2, 10))
        WIN.blit(shapes_score_label, ((WIDTH-shapes_score_label.get_width())/2, model.get_height()+5))
        WIN.blit(levels_label, (WIDTH - levels_label.get_width() - 10, 10))

        if start:
            WIN.blit(start_label, (WIDTH/2 - start_label.get_width()/2, 350))

        for e in enemies:
            e.draw(WIN)

        if win:
            WIN.blit(win_label,  (WIDTH/2 - win_label.get_width()/2, 350))

        if lost:
            WIN.blit(lost_label, (WIDTH/2 - lost_label.get_width()/2, 350))


        player.draw(WIN)
        pygame.display.update()

    while running:
        clock.tick(fps)
        redraw_window()
        # Event Checker
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        if start:
            if any(pygame.key.get_pressed()):
                start = False
        else:
            if player.lives <= 0:
                lost = True

            if player.health <= 0:
                player.lives -= 1
                player.health = player.max_health

            if shapes_score >= num_of_shapes:
                won_round = True
                score += 1
                shapes_score = 0

            if won_round:
                if round == 3:
                    win = True
                else:
                    enemies.clear()
                    level = 1
                    prev_model = model
                    while True:
                        model, model_shapes = MODEL_MAP[random.choice(["tetrahedron", "cube", "octahedron", "icosahedron", "dodecahedron"])]
                        if model is not prev_model:
                            break
                    num_of_shapes = len(model_shapes)
                    if num_of_shapes > 4:
                        wave_length = 10
                    round += 1

                won_round = False

            # TODO: Need to add in functionality when user reaches no lost state
            if lost or win:
                enemies.clear()
            else:
                # TODO: Need to make sure that if the user selects the wrong shape then they lose life

                if len(enemies) == 0:
                    level += 1
                    wave_length += 5
                    height = 0
                    width = 0
                    enemy_type = ""
                    for i in range(wave_length):
                        for e in enemies:
                            while True:
                                height = random.randrange(-1500, - 100)
                                width = random.randrange(50, WIDTH - 100)
                                new_rect = pygame.Rect(width, height, e.get_width(), e.get_height())
                                enemy_type = random.choice(["square", "triangle", "pentagon"])
                                if len(model_shapes) > 0:
                                    if len(enemies) % 3 == 0 and len(enemies) != 0:
                                        if model_shapes[0] == SQUARE:
                                            enemy_type = "square"
                                        elif model_shapes[0] == TRIANGLE:
                                            enemy_type = "triangle"
                                        elif model_shapes[0] == PENTAGON:
                                            enemy_type = "pentagon"

                                if not any(enmey for enmey in enemies if
                                           new_rect.colliderect(enmey.x, enmey.y, enmey.get_width(),enmey.get_height())):
                                    break
                        if len(enemies) > 0:
                            enemy = Enemy(width, height, enemy_type)
                        else:
                            enemy = Enemy(width, height, random.choice(["square", "triangle", "pentagon"]))
                        enemies.append(enemy)

                keys = pygame.key.get_pressed()

                if keys[pygame.K_LEFT] and player.x - player_vel > 0:
                    player.x -= player_vel

                if keys[pygame.K_RIGHT] and player.x + player_vel + player.get_width() < WIDTH:
                    player.x += player_vel

                if keys[pygame.K_UP] and HEIGHT * 0.65 < player.y - player_vel > 0:
                    player.y -= player_vel

                if keys[pygame.K_DOWN] and player.y + player_vel + player.get_height() < HEIGHT:
                    player.y += player_vel

                if keys[pygame.K_SPACE]:
                    player.shoot()


                for enemy in list(enemies):
                    enemy.move(enemy_vel)
                    enemy.move_lasers(laser_vel, player)

                    if random.randrange(0, 2 * 60) == 1:
                        enemy.shoot()

                    if collide(enemy, player):
                        if enemy.character_img in model_shapes:
                            player.health -= 50
                        else:
                            player.health -= 10
                        enemies.remove(enemy)

                    if enemy.y + enemy.get_height() > HEIGHT and enemy.character_img in model_shapes:
                        player.lives -= 1

                    if enemy.y + enemy.get_height() > HEIGHT:
                        enemies.remove(enemy)

                shapes_score, model_shapes = player.move_lasers(-laser_vel, enemies, shapes_score, model_shapes)


if __name__ == "__main__":
    main()