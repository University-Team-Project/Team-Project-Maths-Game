import pygame
import os.path
import time
import math
from opt import blit_rotate_center, scale_image, blit_text_center
pygame.init()
pygame.font.init()

ROAD = pygame.image.load(os.path.join('Assets', 'road.png'))

# LOCATION = scale_image(pygame.image.load(os.path.join('Assets', 'Location1.png')), 2.5)
# LOCATION1 = pygame.image.load(os.path.join('Assets', 'Location1.png'))
LOCATION1 = pygame.image.load(os.path.join('Assets', 'LocationMASK_V2.png'))
LOCATION2 = LOCATION1
BORDER = pygame.image.load(os.path.join('Assets', 'BORDER.png'))
BORDER_MASK = pygame.mask.from_surface(BORDER)

PLAYER_ONE_CAR_IMAGE = pygame.image.load(os.path.join('Assets', 'purple-car.png'))
PLAYER_TWO_CAR_IMAGE = pygame.image.load(os.path.join('Assets', 'white-car.png'))

PLAYER_ONE_COLLIDE = pygame.mask.from_surface(PLAYER_ONE_CAR_IMAGE)

WIDTH, HEIGHT = ROAD.get_width(), ROAD.get_height()
# WIN = pygame.display.set_mode((WIDTH, HEIGHT))
WIN = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
pygame.display.set_caption("Maths Driving Game!")

MAIN_FONT = pygame.font.SysFont("comicsans", 44)

FPS = 60
VEL = 5

TOTAL_QUESTIONS = 10
_QUESTION = 0


class GameInfo:
    ROUNDS = 3

    def __init__(self, game_round=1):
        self.game_round = game_round
        self.started = False
        self.round_start_time = 0

    def next_round(self):
        self.game_round += 1
        self.started = False

    def reset(self):
        self.game_round = 1
        self.started = False
        self.round_start_time = 0

    def game_finish(self):
        return self.game_round > self.ROUNDS

    def start_round(self):
        self.started = True
        self.round_start_time = time.time()

    def get_round_time(self):
        if not self.started:
            return 0
        return round(time.time() - self.round_start_time)


class CarFunctionality:
    def __init__(self, max_vel, rotation_vel):
        self.img = self.IMG
        self.max_vel = max_vel
        self.vel = 0
        self.rotation_vel = rotation_vel
        self.angle = 0
        self.x, self.y = self.START_POS
        self.acceleration = 0.1

    def rotate(self, left=False, right=False):
        if left:
            self.angle += self.rotation_vel
        elif right:
            self.angle -= self.rotation_vel

    def draw(self, win):
        # BELOW IS IN THEN UTILS FILE!!!
        blit_rotate_center(win, self.img, (self.x, self.y), self.angle)

    def move_forward(self):
        self.vel = min(self.vel + self.acceleration, self.max_vel)
        self.move()

    def move_backward(self):
        self.vel = max(self.vel - self.acceleration * 20, -self.max_vel)
        self.move()

    def move(self):
        radians = math.radians(self.angle)
        vertical = math.cos(radians) * self.vel
        horizontal = math.sin(radians) * self.vel

        self.y -= vertical
        self.x -= horizontal

    def reduce_speed(self):
        self.vel = max(self.vel - self.acceleration / 2, 0)
        self.move()

    def bounce(self):
        self.vel = -self.vel * 5
        self.move()

    def reset(self):
        self.x, self.y = self.START_POS
        self.angle = 0
        self.vel = 0

    def collide(self, mask, x=0, y=0):
        car_mask = pygame.mask.from_surface(self.img)
        offset = (int(self.x - x), int(self.y - y))
        poi = mask.overlap(car_mask, offset)
        return poi


class PlayerOneCar(CarFunctionality):
    IMG = PLAYER_ONE_CAR_IMAGE
    START_POS = (700, 500)
    # START_POS = (250, 250)


class PlayerTwoCar(CarFunctionality):
    IMG = PLAYER_TWO_CAR_IMAGE
    START_POS = (750, 500)
    # START_POS = (200, 200)


def draw(win, images, player_one_car, player_two_car):
    for img, pos in images:
        win.blit(img, pos)

    player_one_car.draw(win)
    player_two_car.draw(win)
    pygame.display.update()


def move_player_one(player_one_car):
    keys = pygame.key.get_pressed()
    moved = False

    if keys[pygame.K_a]:
        player_one_car.rotate(left=True)
    if keys[pygame.K_d]:
        player_one_car.rotate(right=True)
    if keys[pygame.K_w]:
        player_one_car.move_forward()
    if keys[pygame.K_s]:
        player_one_car.move_backward()
    if keys[pygame.K_ESCAPE]:
        pygame.quit()

    if not moved:
        player_one_car.reduce_speed()

    print(player_one_car.x, player_one_car.y)


def move_player_two(player_two_car):
    keys = pygame.key.get_pressed()
    moved = False

    if keys[pygame.K_LEFT]:
        player_two_car.rotate(left=True)
    if keys[pygame.K_RIGHT]:
        player_two_car.rotate(right=True)
    if keys[pygame.K_UP]:
        player_two_car.move_forward()
    if keys[pygame.K_DOWN]:
        player_two_car.move_backward()

    if not moved:
        player_two_car.reduce_speed()


def handle_round_end(player_one_car, player_two_car, game_info):
    if player_one_car.x < 190 and player_one_car.y < 200:
        # pygame.time.wait(5000)
        if game_info.game_round < game_info.ROUNDS:
            game_info.next_round()
            player_one_car.reset()
            player_two_car.reset()
        else:
            game_info.game_finish()
            blit_text_center(WIN, MAIN_FONT, "Game over")
            pygame.display.update()


def handle_border(player_one_car, player_two_car, game_info):
    if player_one_car.collide(BORDER_MASK) != None:
        player_one_car.bounce()
    elif player_two_car.collide(BORDER_MASK) != None:
        player_two_car.bounce()

def handle_questions(game_info):
    pass


run = True
clock = pygame.time.Clock()
images = [(ROAD, (0, 0)), (LOCATION1, (0, 0)), (LOCATION2, (BORDER.get_width() - 633, 0)), (BORDER, (0, 0))]
# images = [(LOCATION1, (0, 0)), (LOCATION2, (BORDER.get_width() - 633, 0)), (ROAD, (0, 0)), (BORDER, (0, 0))]
player_one_car = PlayerOneCar(4, 4)
player_two_car = PlayerTwoCar(4, 4)
game_info = GameInfo()

while run:
    clock.tick(FPS)

    draw(WIN, images, player_one_car, player_two_car)

    while not game_info.started:
        blit_text_center(WIN, MAIN_FONT, f"Press enter to start round {game_info.game_round}!")
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                break
            if event.type == pygame.KEYDOWN:
                game_info.start_round()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
            break

    move_player_one(player_one_car)
    move_player_two(player_two_car)

    handle_border(player_one_car, player_two_car, game_info)

    handle_round_end(player_one_car, player_two_car, game_info)

    if game_info.game_finish():
        blit_text_center(WIN, MAIN_FONT, "Game over")
