import os.path
import pygame
import time
from enemies.orc import OrcEnemy
from enemies.skeleton import Skeleton
from enemies.knight import Knight
from archerTower.archerTower import ArcherTower
from archerTower.archerTower import ArcherTowerShort
from archerTower.supportTower import RangeTower, DamageTower
import random

pygame.font.init()
lives_img = pygame.image.load(os.path.join("game_assets","heart.png"))
star_img = pygame.image.load(os.path.join("game_assets","star.png"))

class Game:
    def __init__(self):
        self.width = 1200
        self.height = 700
        self.win = pygame.display.set_mode((self.width, self.height))
        self.enemys = []
        self.attack_towers = [ArcherTower(300, 300), ArcherTower(800, 400), ArcherTowerShort(600, 200)]
        self.support_towers = [DamageTower(250, 370)]
        self.lives = 10
        self.money = 100
        self.bg = pygame.image.load(os.path.join("game_assets", "game_background_2.png"))
        self.bg = pygame.transform.scale(self.bg, (self.width, self.height))
        self.timer = time.time()
        self.life_font = pygame.font.SysFont("freesansbold.ttf", 60)
        self.selected_tower = None

    def run(self):
        if time.time() - self.timer > 2:
            self.timer - time.time()

        run = True
        clock = pygame.time.Clock()

        while run:
            if time.time() - self.timer >= random.randrange(1,5)/2:
                self.timer = time.time()
                self.enemys.append(random.choice([Knight(), OrcEnemy(), Skeleton()]))
            clock.tick(60)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False

                pos = pygame.mouse.get_pos()

                if event.type == pygame.MOUSEBUTTONDOWN:

                    btn_clicked = None
                    if self.selected_tower:
                        btn_clicked = self.selected_tower.menu.get_clicked(pos[0], pos[1])
                        if btn_clicked:
                            print(btn_clicked)

                    if not btn_clicked:
                        for tw in self.attack_towers:
                            if tw.click(pos[0], pos[1]):
                                tw.selected = True
                                self.selected_tower = tw
                            else:
                                tw.selected = False

                        for tw in self.support_towers:
                            if tw.click(pos[0], pos[1]):
                                tw.selected = True
                                self.selected_tower = tw
                            else:
                                tw.selected = False

            to_del = []
            for en in self.enemys:
                if en.x < -15:
                    to_del.append(en)

            for d in to_del:
                self.lives -= 1
                self.enemys.remove(d)

            for tw in self.attack_towers:
                tw.attack(self.enemys)

            for tw in self.support_towers:
                tw.support(self.attack_towers)

            if self.lives <= 0:
                print("You Lose")
                run = False

            self.draw()

        pygame.quit()

    def draw(self):
        self.win.blit(self.bg, (0, 0))

        for tw in self.attack_towers:
            tw.draw(self.win)

        for tw in self.support_towers:
            tw.draw(self.win)

        for en in self.enemys:
            en.draw(self.win)

        text = self.life_font.render(str(self.lives), True, (255,255,255))
        life = pygame.transform.scale(lives_img,(50,50))
        start_x = self.width - life.get_width() - 10
        self.win.blit(text, (start_x - text.get_width() - 10, 15))
        self.win.blit(life, (start_x, 10))

        pygame.display.update()

    def draw_menu(self):
        pass


g = Game()
g.run()
