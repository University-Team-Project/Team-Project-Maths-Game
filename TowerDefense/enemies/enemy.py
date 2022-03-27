import pygame
import math


class Enemy:
    imgs = []

    def __init__(self):
        self.width = 64
        self.height = 64
        self.animation_count = 0
        self.health = 1
        self.path = []
        self.img = None
        self.dis = 0
        self.velocity = 3
        self.path = [(308, 685), (286, 613), (198, 587), (124, 522), (110, 445), (152, 374), (236, 346), (302, 271),
                     (321, 182), (401, 138), (493, 131), (598, 132), (661, 181), (675, 260), (680, 447), (759, 508),
                     (1012, 515), (1194, 515)]
        self.x = self.path[0][0]
        self.y = self.path[0][1]

        self.path_pos = 0
        self.move_count = 0
        self.move_dis = 0
        self.imgs = []
        self.max_health = 0

    def draw(self, win):
        """
        Draws the enemy with the given images
        """

        self.img = self.imgs[self.animation_count // 3]
        self.animation_count += 1
        if self.animation_count >= len(self.imgs) * 3:
            self.animation_count = 0

        win.blit(self.img, (self.x - self.img.get_width() / 2, self.y - self.img.get_height() / 2 - 30))
        self.health_bar(win)
        self.move()

    def health_bar(self, win):
        length = 50
        move_by = round(length / self.max_health)
        health_bar = move_by * self.health
        pygame.draw.rect(win, (255,0,0), (self.x-35, self.y - 70, length, 10), 0)
        pygame.draw.rect(win, (0, 255, 0), (self.x-35, self.y - 70, health_bar, 10), 0)


    def collide(self, X, Y):

        if X <= self.x + self.width and X >= self.x:
            if Y <= self.y + self.height and Y >= self.y:
                return True
        return False

    def move(self):

        x1, y1 = self.path[self.path_pos]
        if self.path_pos + 1 >= len(self.path):
            x2, y2 = (-10, 515)
        else:
            x2, y2 = self.path[self.path_pos + 1]

        dirn = ((x2 - x1) * 2, (y2 - y1) * 2)
        length = math.sqrt((dirn[0]) ** 2 + (dirn[1]) ** 2)
        dirn = (dirn[0] / length, dirn[1] / length)

        move_x, move_y = ((self.x + dirn[0]), (self.y + dirn[1]))
        self.dis += length
        print(self.dis)

        self.x = move_x
        self.y = move_y

        if dirn[0] >= 0:
            if dirn[1] >= 0:
                if self.x >= x2 and self.y >= y2:
                    self.path_pos += 1
            else:
                if self.x >= x2 and self.y <= y2:
                    self.path_pos += 1
        else:
            if dirn[1] >= 0:
                if self.x <= x2 and self.y >= y2:
                    self.path_pos += 1
            else:
                if self.x <= x2 and self.y <= y2:
                    self.path_pos += 1

    def hit(self, damage):
        self.health -= damage
        if self.health <= 0:
            return True
        return False
