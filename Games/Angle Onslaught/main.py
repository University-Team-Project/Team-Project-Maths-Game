import sys
import pygame.time
from pygame import *
from settings import *
from enemy import *


def game_loop():
    """
    Initialized settings
    """

    pygame.display.set_icon(pygame.image.load("resources/enemy/ice_boss/0_specialty_walk_005.png"))

    colour = Colours()
    settings = Settings(colour)
    cursor = Cursor()
    screen = settings.screen

    settings.countdown_overlay()

    questions = Questions()

    # creates a new rectangle on the screen according to the variables given to the class

    category_rectangles = settings.categoryArray
    new_rect = questions.new_question(settings, colour)
    questions.assign_questions(settings, category_rectangles)

    question_text = settings.question_font.render(str(questions.active_question), True, (0, 0, 0))
    question_text_rect = question_text.get_rect(center=(settings.midWidth,
                                                        settings.midWidth))

    score = 0
    settings.questions_array.append(new_rect)

    enemy_event = pygame.USEREVENT + 2
    pygame.time.set_timer(enemy_event, 100)

    game_active = True

    current_boss = IceEnemy(65, 580)
    enemy_group = pygame.sprite.Group(current_boss)

    # game loop
    while True:

        timer = current_boss.progress

        settings.screen_tick(colour, score, timer, game_active)

        if game_active:
            # draw health bar
            pygame.draw.rect(screen, (255, 0, 0), (current_boss.x_pos,
                                                   current_boss.health_y_pos,
                                                   current_boss.width,
                                                   10))
            pygame.draw.rect(screen, (0, 255, 0), (current_boss.x_pos,
                                                   current_boss.health_y_pos,
                                                   current_boss.width * (current_boss.health / 100),
                                                   10))

        # event handler
        for e in pygame.event.get():

            if e.type == QUIT:
                pygame.quit()
                sys.exit()

            elif e.type == enemy_event:
                if game_active:
                    enemy_group.update()
                    boss_status = current_boss.move(screen)
                    if boss_status == "alive":
                        game_active = False
                        settings.end_game(score)

            elif e.type == pygame.MOUSEBUTTONDOWN:
                if e.button == 1:
                    if game_active:
                        for q in settings.questions_array:
                            if q.active:
                                if q.pygameRectangle.collidepoint(e.pos):
                                    q.dragging = True
                                    cursor.set_cursor(q, settings, game_active)
                                    cursor.xPos, cursor.yPos = e.pos
                                    offset_x = q.xPos - cursor.xPos
                                    offset_y = q.yPos - cursor.yPos
                    else:
                        if settings.restartCategory.categoryRectangle.collidepoint(pygame.mouse.get_pos()):
                            # restart game
                            pygame.quit()
                            game_loop()

                        elif settings.exitCategory.categoryRectangle.collidepoint(pygame.mouse.get_pos()):
                            pygame.quit()
                            sys.exit()

            elif e.type == pygame.MOUSEBUTTONUP:
                    if e.button == 1:
                        if game_active:
                            for q in settings.questions_array:
                                if q.dragging:
                                    cursor.set_cursor(q, settings, game_active)
                                    q.dragging = False
                                    for row in category_rectangles:
                                        if row.categoryRectangle.collidepoint(e.pos):
                                            if not settings.defaultCategory.categoryRectangle.collidepoint(e.pos):
                                                if q.category == row.category:
                                                    score += 1
                                                    q.active = False
                                                    boss_status = current_boss.damage()
                                                else:
                                                    current_boss.upgrade()
                                                    q.active = False
                                                if boss_status == 'dead':
                                                    game_active = False
                                                    settings.end_game(score)
                                                else:
                                                    q.active = False
                                                new_rect = questions.new_question(settings, colour)
                                                questions.assign_questions(settings, category_rectangles)
                                                settings.questions_array.append(new_rect)

            elif e.type == pygame.MOUSEMOTION:
                for q in settings.questions_array:
                    if q.dragging:
                        cursor.xPos, cursor.yPos = e.pos
                        q.xPos = cursor.xPos + offset_x
                        q.yPos = cursor.yPos + offset_y

        if game_active:

            for q in settings.questions_array:
                if q.active:
                    settings.screen.blit(questions.loaded_question_image,
                                         (settings.midWidth - 100, settings.midHeight - 150))
                    q.draw_question_rectangle()
                    question_text = settings.question_font.render(str(questions.active_question), True, (0, 0, 0))
                    question_text_rect = question_text.get_rect(center=(q.xPos + 75, q.yPos + 75))
                    settings.screen.blit(question_text, question_text_rect)

            current_boss.write_name(screen)

            enemy_group.draw(screen)

            cursor.set_cursor(q, settings, game_active)

            pygame.display.flip()

            settings.fpsClock.tick(settings.fps)

        else:

            cursor.set_cursor(q, settings, game_active)

            pygame.display.flip()

            settings.fpsClock.tick(settings.fps)


if __name__ == '__main__':
    game_loop()
