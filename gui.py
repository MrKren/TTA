import pygame
from spritesheet import SpriteSheet


class GUI(pygame.sprite.Sprite):

    def __init__(self):

        super().__init__()

        self.sheet = SpriteSheet("GUI.png")
        self.image = self.sheet.get_image(0, 0, 196, 278)
        self.rect = self.image.get_rect()


class HealthBar(pygame.sprite.Sprite):

    def __init__(self, player):

        super().__init__()

        self.length = 144
        self.max_length = 144
        self.height = 16
        self.health = player.health
        self.max_health = player.max_health
        self.image = pygame.Surface([self.length, self.height])
        self.image.fill((64, 64, 64))
        self.rect = self.image.get_rect()
        pygame.draw.rect(self.image, (255, 0, 0), [0, 0, self.length, self.height])
        self.rect.x = 26
        self.rect.y = 146

    def update(self, player):

        self.length = int(player.health/player.max_health * self.max_length)
        self.image = pygame.transform.scale(self.image, (self.length, self.height))


class HealthBarBack(pygame.sprite.Sprite):

    def __init__(self, player):

        super().__init__()

        self.length = 144
        self.max_length = 144
        self.height = 16
        self.health = player.health
        self.max_health = player.max_health
        self.image = pygame.Surface([self.length, self.height])
        self.image.fill((64, 64, 64))
        self.rect = self.image.get_rect()
        pygame.draw.rect(self.image, (64, 64, 64), [0, 0, self.length, self.height])
        self.rect.x = 26
        self.rect.y = 146
