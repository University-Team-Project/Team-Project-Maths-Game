import pygame
import os
from .enemy import Enemy

imgs = []

for x in range(10):
    add_str = str(x)
    if x < 10:
        add_str = "0" + add_str
        imgs.append(pygame.transform.scale(
            pygame.image.load(os.path.join("enemies/2", "2_enemies_1_RUN_0" + add_str + ".png")), (64, 64)))


class Skeleton(Enemy):

    def __init__(self):
        super(Skeleton, self).__init__()
        self.name = "Skeleton"
        self.money = 2  # How much money the enemy drops
        self.max_health = 3  # Max health
        self.health = self.max_health
        self.imgs = imgs[:]
