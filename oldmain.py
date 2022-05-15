import random
import sys

import pygame
import os.path
import time
import math
from opt import blit_rotate_center, scale_image, blit_text_center, blit_text_top, blit_text_top_left, blit_text_top_right, blit_text_bottom_left, blit_text_bottom_right, blit_text_player_one_score, blit_text_player_two_score, blit_timer_text, blit_player1_scoreboard, blit_player2_scoreboard, blit_question_top, blit_question_text_top
pygame.init()
pygame.font.init()


ROAD = pygame.image.load(os.path.join('Assets', 'Car_park.png'))
WIDTH, HEIGHT = ROAD.get_width(), ROAD.get_height()
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Maths Driving Game!")

# Creation of all locations

LOCATION_1 = pygame.image.load(os.path.join('Assets', 'LocationMASK_V5.png'))
LOCATION_1_WIDTH, LOCATION_1_HEIGHT = LOCATION_1.get_width(), LOCATION_1.get_height()

LOCATION2 = LOCATION_1
LOCATION_2_WIDTH, LOCATION_2_HEIGHT = ROAD.get_width() - LOCATION_1.get_width(), LOCATION_1.get_height()

LOCATION3 = LOCATION_1
LOCATION_3_WIDTH, LOCATION_3_HEIGHT = LOCATION_1.get_width(), ROAD.get_height() - LOCATION_1.get_height()

LOCATION4 = LOCATION_1
LOCATION_4_WIDTH, LOCATION_4_HEIGHT = ROAD.get_width() - LOCATION_1.get_width(), ROAD.get_height() - LOCATION_1.get_height()

# Creation of the border - prevents players leaving screen
BORDER = pygame.image.load(os.path.join('Assets', 'BORDER3.png'))
BORDER_MASK = pygame.mask.from_surface(BORDER)

# Loading of player car images

PLAYER_ONE_CAR_IMAGE = pygame.image.load(os.path.join('Assets', 'purple-car.png'))
PLAYER_TWO_CAR_IMAGE = pygame.image.load(os.path.join('Assets', 'white-car.png'))

PLAYER_ONE_COLLIDE = pygame.mask.from_surface(PLAYER_ONE_CAR_IMAGE)

MAIN_FONT = pygame.font.Font("Tokyo 2097.otf", 44)
QUESTION_FONT = pygame.font.SysFont("arial.ttf", 80)
ANSWER_FONT = pygame.font.Font("Tokyo 2097.otf", 105)
SCORE_FONT = pygame.font.Font("Tokyo 2097.otf", 33)
TIMER_FONT = pygame.font.SysFont("freesansbold.ttf", 33)

FPS = 60
VEL = 5

TOTAL_QUESTIONS = 10
_QUESTION = 0

QUESTIONS = ["320m/s in 16s", "1450m/s in 29s", "884m/s in 26s", "437m/s in 19s", "738m/s in 18s", "832m/s in 16s", "1170m/s in 18s", "696m/s in 12s"]
QUESTION_NUM = 1
CORRECT_ANSWERS = ["20", "50", "34", "23", "41", "52", "65", "58"]
RANDOM_ANSWERS = ["25", "75", "48", "81", "61", "37", "11", "14", "24", "93", "44", "27", "64", "79", "86", "99"]


class GameInfo:
    ROUNDS = 5

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
        pygame.time.set_timer(timer_event, 1000)

    def get_round_time(self):
        pygame.time.set_timer(timer_event, 1000)


class CarFunctionality:
    def __init__(self, max_vel, rotation_vel):
        self.img = self.IMG
        self.max_vel = max_vel
        self.vel = 0
        self.rotation_vel = rotation_vel
        self.angle = 0
        self.x, self.y = self.START_POS
        self.acceleration = 0.1
        self.current_location = None
        self.current_points = 0

    def rotate(self, left=False, right=False):
        if left:
            self.angle += self.rotation_vel
        elif right:
            self.angle -= self.rotation_vel

    def draw(self, win):
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
    START_POS = (ROAD.get_width()/2 - 50, ROAD.get_height()/2)


class PlayerTwoCar(CarFunctionality):
    IMG = PLAYER_TWO_CAR_IMAGE
    START_POS = (ROAD.get_width()/2, ROAD.get_height()/2)


def draw(win, images, player_one_car, player_two_car, current_question, answers_for_draw, current_question_answer, timer):
    for img, pos in images:
        win.blit(img, pos)

    player_one_car.draw(win)
    player_two_car.draw(win)

    blit_question_top(WIN, QUESTION_FONT, f"{current_question}")


    if len(answers_for_draw) > 0:
        blit_text_top_left(WIN, ANSWER_FONT, answers_for_draw[0])
        blit_text_top_right(WIN, ANSWER_FONT, answers_for_draw[1])
        blit_text_bottom_left(WIN, ANSWER_FONT, answers_for_draw[2])
        blit_text_bottom_right(WIN, ANSWER_FONT, answers_for_draw[3])
        blit_timer_text(WIN, TIMER_FONT, f"Time Left: {str(timer)}")
        blit_text_top(WIN, SCORE_FONT, f"Round {game_info.game_round}")
        blit_question_text_top(WIN, TIMER_FONT, "Increase of speed by:")

    blit_text_player_one_score(WIN, SCORE_FONT, "P1: " + str(player_one_car.current_points))
    blit_text_player_two_score(WIN, SCORE_FONT, "P2: " + str(player_two_car.current_points))

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
        pygame.display.quit()
        pygame.quit()
        sys.exit()

    if not moved:
        player_one_car.reduce_speed()


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

    if player_one_car.x < LOCATION_1_WIDTH and player_one_car.y < LOCATION_1_HEIGHT:
        player_one_car.current_location = 1
    elif player_one_car.x > LOCATION_2_WIDTH and player_one_car.y < LOCATION_2_HEIGHT:
        player_one_car.current_location = 2
    elif player_one_car.x < LOCATION_3_WIDTH and player_one_car.y > LOCATION_3_HEIGHT:
        player_one_car.current_location = 3
    elif player_one_car.x > LOCATION_4_WIDTH and player_one_car.y > LOCATION_4_HEIGHT:
        player_one_car.current_location = 4
    else:
        player_one_car.current_location = None

    if player_two_car.x < LOCATION_1_WIDTH and player_two_car.y < LOCATION_1_HEIGHT:
        player_two_car.current_location = 1
    elif player_two_car.x > LOCATION_2_WIDTH and player_two_car.y < LOCATION_2_HEIGHT:
        player_two_car.current_location = 2
    elif player_two_car.x < LOCATION_3_WIDTH and player_two_car.y > LOCATION_3_HEIGHT:
        player_two_car.current_location = 3
    elif player_two_car.x > LOCATION_4_WIDTH and player_two_car.y > LOCATION_4_HEIGHT:
        player_two_car.current_location = 4
    else:
        player_two_car.current_location = None


def next_game_round(player_one_car, player_two_car, game_info, players_scored):
    # PASS IN ARRAY OF PLAYERS WHO HAVE SCORED
    # LOOP THROUGH THE ARRAY AND GIVE POINTS TO EACH PLAYER IN THE ARRAY
    # THEN PRINT OUT EACH PLAYER IN THE ARRAY THAT HAS SCORED
    # ARRAY WILL NEED TO BE CLEARED AFTER EACH ROUND - PLACE ARRAY UNDER Run AND CLEAR WITH Handle_Reset
    if player_one_car in players_scored and player_two_car in players_scored:
        blit_text_center(WIN, MAIN_FONT, "Both players scored!")
        player_one_car.current_points = player_one_car.current_points + 1
        player_two_car.current_points = player_two_car.current_points + 1
        pygame.display.update()
    elif player_one_car in players_scored:
        blit_text_center(WIN, MAIN_FONT, "Player 1 scores!")
        player_one_car.current_points = player_one_car.current_points + 1
        pygame.display.update()
    elif player_two_car in players_scored:
        blit_text_center(WIN, MAIN_FONT, "Player 2 scores!")
        player_two_car.current_points = player_two_car.current_points + 1
        pygame.display.update()
    pygame.time.wait(1500)
    game_info.next_round()
    player_one_car.reset()
    player_two_car.reset()


def handle_border(player_one_car, player_two_car, game_info):
    if player_one_car.collide(BORDER_MASK) != None:
        player_one_car.bounce()
    elif player_two_car.collide(BORDER_MASK) != None:
        player_two_car.bounce()


def handle_questions(game_info, questions_asked):
    asking = True
    while asking:
        current_question = random.choice(QUESTIONS)
        if current_question in questions_asked:
            asking = True
        else:
            questions_asked.append(current_question)
            asking = False

    return current_question


def handle_answer(current_question, location_1_answer, location_2_answer, location_3_answer, location_4_answer):
    answer_location = QUESTIONS.index(current_question)
    answer = CORRECT_ANSWERS[answer_location]
    # Choose random location
    locations = ["location_1_answer", "location_2_answer", "location_3_answer", "location_4_answer"]
    correct_answer_location = random.choice(locations)
    locations.remove(correct_answer_location)
    return answer_location, answer, locations


def handle_all_answers(current_question_answer_location, location_1_answer, location_2_answer, location_3_answer, location_4_answer, locations, incorrect_answers):
    for i in locations:
        i = random.choice(RANDOM_ANSWERS)
        incorrect_answers.append(i)
    return locations, incorrect_answers


def handle_reset():
    current_question = ""
    current_question_answer = ""
    location_1_answer = ""
    location_2_answer = ""
    location_3_answer = ""
    location_4_answer = ""
    locations = []
    incorrect_answers = []
    answers_for_draw = []
    correct_answer_location = None
    players_scored = []
    timer = 30

    return current_question, current_question_answer, location_1_answer, location_2_answer, location_3_answer, location_4_answer, locations, incorrect_answers, answers_for_draw, correct_answer_location, players_scored, timer


def handle_game_over(player_one_car, player_two_car, game_info):
    if player_one_car.current_points > player_two_car.current_points:
        blit_text_center(WIN, MAIN_FONT, "Player 1 has won the game!")
    elif player_two_car.current_points > player_one_car.current_points:
        blit_text_center(WIN, MAIN_FONT, "Player 2 has won the game!")
    elif player_one_car.current_points == player_two_car.current_points:
        blit_text_center(WIN, MAIN_FONT, "The game is a tie!")

    blit_player1_scoreboard(WIN, MAIN_FONT, "Player 1:  " + str(player_one_car.current_points))
    blit_player2_scoreboard(WIN, MAIN_FONT, "Player 2:  " + str(player_two_car.current_points))
    pygame.display.update()



run = True
clock = pygame.time.Clock()
images = [(BORDER, (0, 0)), (LOCATION_1, (0, 0)), (LOCATION2, (ROAD.get_width() - LOCATION_1_WIDTH, 0)), (LOCATION3, (0, ROAD.get_height() - LOCATION_1_HEIGHT)), (LOCATION4, (ROAD.get_width() - LOCATION_1_WIDTH, ROAD.get_height() - LOCATION_1_HEIGHT)), (ROAD, (0, 0))]
player_one_car = PlayerOneCar(4, 4)
player_two_car = PlayerTwoCar(4, 4)
game_info = GameInfo()
questions_asked = []

timer_event = pygame.USEREVENT + 1


current_question, current_question_answer, location_1_answer, location_2_answer, location_3_answer, location_4_answer, locations, incorrect_answers, answers_for_draw, correct_answer_location, players_scored, timer = handle_reset()

while run:
    clock.tick(FPS)

    draw(WIN, images, player_one_car, player_two_car, current_question, answers_for_draw, current_question_answer, timer)

    while not game_info.started:
        if game_info.game_finish():
            handle_game_over(player_one_car, player_two_car, game_info)
            pygame.time.wait(4500)
            pygame.display.quit()
            pygame.quit()
            sys.exit()
        else:
            blit_text_center(WIN, MAIN_FONT, f"Press enter to start round {game_info.game_round}!")
            pygame.display.update()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.display.quit()
                    pygame.quit()
                    sys.exit()
                    break
                if event.type == pygame.KEYDOWN:
                    current_question = handle_questions(game_info, questions_asked)
                    current_question_answer_location, current_question_answer, locations = handle_answer(
                        current_question, location_1_answer, location_2_answer,
                        location_3_answer, location_4_answer)
                    locations, incorrect_answers = handle_all_answers(current_question_answer_location,
                                                                      location_1_answer, location_2_answer,
                                                                      location_3_answer,
                                                                      location_4_answer, locations, incorrect_answers)
                    answers_for_draw = incorrect_answers
                    answers_for_draw.append(current_question_answer)
                    random.shuffle(answers_for_draw)
                    correct_answer_location = answers_for_draw.index(current_question_answer)

                    game_active = True
                    game_info.start_round()


    for event in pygame.event.get():
        if event.type == timer_event:
            if game_info.started == True:
                if timer >= 0:
                    timer -= 1
                else:
                    pygame.time.set_timer(timer_event, 0)
                    game_active = False
        if event.type == pygame.QUIT:
            run = False
            break

    move_player_one(player_one_car)
    move_player_two(player_two_car)

    handle_border(player_one_car, player_two_car, game_info)

    handle_round_end(player_one_car, player_two_car, game_info)


    if timer < 0:
        player_one_checked = False
        player_two_checked = False
        while player_one_checked == False and player_two_checked == False:
            if player_one_car.current_location != None and player_one_car.current_location - 1 == correct_answer_location:
                players_scored.append(player_one_car)
                player_one_checked = True
            else:
                player_one_checked = True

            if player_two_car.current_location != None and player_two_car.current_location - 1 == correct_answer_location:
                players_scored.append(player_two_car)
                player_two_checked = True

            else:
                player_two_checked = True

        if player_one_checked == True and player_two_checked == True:
            next_game_round(player_one_car, player_two_car, game_info, players_scored)
            current_question, current_question_answer, location_1_answer, location_2_answer, location_3_answer, location_4_answer, locations, incorrect_answers, answers_for_draw, correct_answer_location, players_scored, timer = handle_reset()
