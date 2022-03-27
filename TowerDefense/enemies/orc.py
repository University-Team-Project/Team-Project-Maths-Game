import pygame
import os
from .enemy import Enemy

imgs = []

for x in range(20):
    add_str = str(x)
    if x < 10:
        add_str = "0" + add_str
        imgs.append(pygame.transform.scale(
        pygame.image.load(os.path.join("enemies/1", "7_enemies_1_run_0" + add_str + ".png")), (64, 64)))

class OrcEnemy(Enemy):

    def __init__(self):
        super(OrcEnemy, self).__init__()
        self.max_health = 5
        self.health = self.max_health
        self.imgs = imgs[:]

