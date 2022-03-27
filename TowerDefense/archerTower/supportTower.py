import pygame
from .tower import Tower
import os
import math
import time

range_imgs = [pygame.image.load(os.path.join("game_assets/range_towers", "5.png")),
              pygame.image.load(os.path.join("game_assets/range_towers", "6.png"))]


class RangeTower(Tower):
    def __init__(self, x, y):
        super(RangeTower, self).__init__(x, y)
        self.range = 150
        self.tower_imgs = range_imgs[:]

    def draw(self, win):
        super(RangeTower, self).draw_radius(win)
        super(RangeTower, self).draw(win)

    def support(self, towers):
        pass


damage_imgs = [pygame.image.load(os.path.join("game_assets/damage_towers", "8.png")),
               pygame.image.load(os.path.join("game_assets/damage_towers", "9.png"))]


class DamageTower(RangeTower):

    def __init__(self, x, y):
        super().__init__(x, y)
        self.range = 150
        self.tower_imgs = damage_imgs[:]
        self.effect = [1, 2]

    def support(self, towers):
        pass
