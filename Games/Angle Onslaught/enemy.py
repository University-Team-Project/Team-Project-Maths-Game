import pygame
import glob


# parent class to create an enemy

class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()

        self.name = None
        self.start_x = x
        self.x_pos = x
        self.y_pos = y
        self.width = 100
        self.height = 100

        self.health_y_pos = self.y_pos + 110
        self.health = 0
        self.speed = 1

        self.distance_traveled = 0
        self.progress = 0

        self.font = pygame.font.Font("resources/font/static/Inter-SemiBold.ttf", 15)

        self.images = []

        # index value to get the image from the array
        # initially it is 0
        self.index = 0

        # creating a rect at position x,y (5,5) of size (150,198) which is the size of sprite
        self.rect = pygame.Rect(self.x_pos, self.y_pos, self.width, self.height)

    def update(self):
        # when the update method is called, we will increment the index
        self.index += 1

        # if the index is larger than the total images
        if self.index >= len(self.images):
            # we will make the index to 0 again
            self.index = 0

        # finally, we will update the image that will be displayed
        self.image = self.images[self.index]

    # method to move the enemy to the right by 1 pixel

    def move(self, screen):
        if self.x_pos <= (0.83203125 * screen.get_width()):
            self.x_pos += self.speed
            self.distance_traveled += self.speed
            self.rect = pygame.Rect(self.x_pos, self.y_pos, self.width, self.height)

            self.progress = int((self.distance_traveled / 10) - 1)
        else:
            self.kill()
            return "alive"

    # method to damage the enemy

    def damage(self):
        if self.health > 10:
            self.health -= 10
            print(self.health)
        else:
            self.kill()
            return "dead"

    # method to write the enemy name

    def write_name(self, screen):
        # we will get the name of the enemy and write it on the screen
        name = self.name
        name_image = self.font.render(name, True, (255, 255, 255))
        screen.blit(name_image, (0.03125 * screen.get_width(), 0.741666667 * screen.get_height()))

    # method to upgrade enemy speed by 2x

    def upgrade(self):
        self.speed *= 2


# class to inherit from enemy to create an ice enemy

class IceEnemy(Enemy):
    def __init__(self, x, y):
        super().__init__(x, y)

        for filename in glob.glob('resources/enemy/ice_boss/*.png'):
            self.images.append(pygame.transform.scale(pygame.image.load(filename), (self.width, self.height)))

        # now the image that we will display will be the index from the image array
        self.image = self.images[self.index]

        self.name = "The Grand Ice Master"
        self.health = 100


# class to inherit from enemy to create a yeti enemy

class YetiEnemy(Enemy):
    def __init__(self, x, y):
        super().__init__(x, y)

        for filename in glob.glob('resources/enemy/yeti_boss/*.png'):
            self.images.append(pygame.transform.scale(pygame.image.load(filename), (self.width, self.height)))

        # now the image that we will display will be the index from the image array
        self.image = self.images[self.index]

        self.name = "Cthulhu, King of the Yetis"
        self.health = 150


# class you inherit from enemy to create a knight enemy

class KnightEnemy(Enemy):
    def __init__(self, x, y):
        super().__init__(x, y)

        for filename in glob.glob('resources/enemy/knight_boss/*.png'):
            self.images.append(pygame.transform.scale(pygame.image.load(filename), (self.width, self.height)))

        # now the image that we will display will be the index from the image array
        self.image = self.images[self.index]

        self.name = "Sir Alienor the Warrior"
        self.health = 200
