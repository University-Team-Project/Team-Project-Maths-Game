import pygame
import os
from .enemy import Enemy

imgs = []
for x in range(9):
    add_str = str(x)
    if x < 10:
        add_str = "0" + add_str
        imgs.append(pygame.transform.scale(
        pygame.image.load(os.path.join("enemies/3", "1_enemies_1_RUN_0" + add_str + ".png")), (64, 64)))


class Knight(Enemy):
    def __init__(self):
        super(Knight, self).__init__()
        self.name = "Knight"
        self.money = 4
        self.imgs = imgs[:]
        self.max_health = 5
        self.health = self.max_health
