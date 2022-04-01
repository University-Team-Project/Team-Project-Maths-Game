import os.path
import pygame
import time
from enemies.orc import OrcEnemy
from enemies.skeleton import Skeleton
from enemies.knight import Knight
from archerTower.archerTower import ArcherTower, ArcherTowerShort
from archerTower.supportTower import RangeTower, DamageTower
from menu.menu import VerticalMenu
import random

# Constants
pygame.font.init()
lives_img = pygame.image.load(os.path.join("game_assets", "heart.png"))
star_img = pygame.image.load(os.path.join("game_assets", "star.png"))
side_img = pygame.transform.scale(pygame.image.load(os.path.join("game_assets", "side.png")), (120, 500))

# Game constants
buy_archer = pygame.transform.scale(pygame.image.load(os.path.join("game_assets", "buy_archer.png")), (75, 75))
buy_crossbow = pygame.transform.scale(pygame.image.load(os.path.join("game_assets", "buy_crossbow.png")), (75, 75))
buy_damage = pygame.transform.scale(pygame.image.load(os.path.join("game_assets", "buy_damage.png")), (75, 75))
buy_range = pygame.transform.scale(pygame.image.load(os.path.join("game_assets", "buy_range.png")), (75, 75))

attack_tower_names = ["archer", "crossbow"]
support_tower_names = ["RangeTower", "DamageTower"]

class Game:
    def __init__(self):
        self.width = 1350
        self.height = 700
        self.win = pygame.display.set_mode((self.width, self.height))
        self.enemys = []
        self.attack_towers = [ArcherTower(300, 300), ArcherTower(700, 600), ArcherTowerShort(600, 200)]
        self.support_towers = [DamageTower(250, 370)]
        self.lives = 10
        self.money = 3000
        self.bg = pygame.image.load(os.path.join("game_assets", "game_background_2.png"))
        self.bg = pygame.transform.scale(self.bg, (self.width, self.height))
        self.timer = time.time()
        self.life_font = pygame.font.SysFont("freesansbold.ttf", 50)
        self.selected_tower = None
        self.menu = VerticalMenu(self.width - side_img.get_width() + 70, 250, side_img)
        self.menu.add_btn(buy_archer, "buy_archer", 500)
        self.menu.add_btn(buy_crossbow, "buy_crossbow", 750)
        self.menu.add_btn(buy_damage, "buy_damage", 1000)
        self.menu.add_btn(buy_range, "buy_range", 1000)
        self.moving_object = None

    def run(self):
        if time.time() - self.timer > 2:
            self.timer - time.time()

        run = True
        clock = pygame.time.Clock()

        while run:
            clock.tick(60)
            if time.time() - self.timer >= random.randrange(1, 5) / 2:
                self.timer = time.time()
                self.enemys.append(random.choice([Knight(), OrcEnemy(), Skeleton()]))

            pos = pygame.mouse.get_pos()

            if self.moving_object:
                self.moving_object.move(pos[0], pos[1])

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False

                if event.type == pygame.MOUSEBUTTONDOWN:
                    if self.moving_object:
                        if self.moving_object.name in attack_tower_names:
                            self.attack_towers.append(self.moving_object)
                        elif self.moving_object.name in support_tower_names:
                            self.support_towers.append(self.moving_object)

                        self.moving_object.moving = False
                        self.moving_object = None
                    else:
                        side_menu_button = self.menu.get_clicked(pos[0], pos[1])
                        if side_menu_button:
                            cost = self.menu.get_item_cost(side_menu_button)
                            if self.money >= cost:
                                self.money -= cost
                                self.add_tower(side_menu_button)

                        btn_clicked = None
                        if self.selected_tower:
                            btn_clicked = self.selected_tower.menu.get_clicked(pos[0], pos[1])
                            if btn_clicked:
                                if btn_clicked == "Upgrade":
                                    cost = self.selected_tower.get_upgrade_cost()
                                    if self.money >= cost:
                                        self.money -= cost
                                        self.selected_tower.upgrade()

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
                self.money += tw.attack(self.enemys)

            for tw in self.support_towers:
                tw.support(self.attack_towers)

            if self.lives <= 0:
                print("You Lose")
                run = False

            self.draw()

        pygame.quit()

    def draw(self):
        self.win.blit(self.bg, (0, 0))

        # Draw Attack Towers
        for tw in self.attack_towers:
            tw.draw(self.win)

        # Draw support towers
        for tw in self.support_towers:
            tw.draw(self.win)

        # Draw enemy's
        for en in self.enemys:
            en.draw(self.win)

        # Draw moving object
        if self.moving_object:
            self.moving_object.draw(self.win)

        self.menu.draw(self.win)

        # Draw lives
        text = self.life_font.render(str(self.lives), True, (255, 255, 255))
        life = pygame.transform.scale(lives_img, (50, 50))
        start_x = self.width - life.get_width() - 10

        self.win.blit(text, (start_x - text.get_width() - 10, 17))
        self.win.blit(life, (start_x, 10))

        # Draw money
        text = self.life_font.render(str(self.money), True, (255, 255, 255))
        money = pygame.transform.scale(star_img, (50, 50))
        start_x = self.width - life.get_width() - 10

        self.win.blit(text, (start_x - text.get_width() - 10, 82))
        self.win.blit(money, (start_x, 70))

        pygame.display.update()

    def add_tower(self, name):
        x, y = pygame.mouse.get_pos()
        name_list = ["buy_archer", "buy_crossbow", "buy_damage", "buy_range"]
        object_list = [ArcherTower(x, y), ArcherTowerShort(x, y), DamageTower(x, y), RangeTower(x, y)]

        try:
            obj = object_list[name_list.index(name)]
            self.moving_object = obj
            obj.moving = True
        except Exception as e:
            print(str(e) + " is not a valid tower name")


g = Game()
g.run()
