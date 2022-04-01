import pygame
from .tower import Tower
import os
import math
import time

range_imgs = [pygame.transform.scale(pygame.image.load(os.path.join("game_assets/range_towers", "5.png")), (100, 100)),
              pygame.transform.scale(pygame.image.load(os.path.join("game_assets/range_towers", "6.png")), (100, 100))]


class RangeTower(Tower):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.range = 75
        self.tower_imgs = range_imgs[:]
        self.effect = [0.5, 1]
        self.width = self.height = 90
        self.name = "RangeTower"

    def draw(self, win):
        super().draw_radius(win)
        super().draw(win)

    def support(self, towers):
        effected = []
        for tower in towers:
            x = tower.x
            y = tower.y

            dis = math.sqrt((self.x - x) ** 2 + (self.y - y) ** 2)

            if dis <= self.range + tower.width / 2:
                effected.append(tower)

        for tower in effected:
            tower.range = tower.original_range + round(tower.range * self.effect[self.level - 1])


damage_imgs = [
    pygame.transform.scale(pygame.image.load(os.path.join("game_assets/damage_towers", "8.png")), (100, 100)),
    pygame.transform.scale(pygame.image.load(os.path.join("game_assets/damage_towers", "9.png")), (100, 100))]


class DamageTower(RangeTower):

    def __init__(self, x, y):
        super().__init__(x, y)
        self.range = 100
        self.tower_imgs = damage_imgs[:]
        self.effect = [0.2, 0.4]
        self.name = "DamageTower"

    def support(self, towers):

        effected = []
        for tower in towers:
            x = tower.x
            y = tower.y

            dis = math.sqrt((self.x - x) ** 2 + (self.y - y) ** 2)

            if dis <= self.range + tower.width / 2:
                effected.append(tower)

        for tower in effected:
            tower.damage = tower.original_damage + round(tower.original_damage * self.effect[self.level - 1])
