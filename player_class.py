import pygame
import math
from spritesheet import SpriteSheet
from animate import Animation


class Player(pygame.sprite.Sprite):
    """Player class that is used to create player sprite as well as control player attributes"""

    def __init__(self):
        """initialisation of class"""

        super().__init__()

        sprite_sheet = SpriteSheet('character.png')

        self.image = sprite_sheet.get_image(0, 0, 128, 128)
        self.image_original = self.image
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect()
        self.rect.x = 540 - self.rect.centerx
        self.rect.y = 360 - self.rect.centery

        self.speed = 5
        self.health = 100
        self.max_health = 100
        self.dead = False
        self.ghost = Animation("ghost.png", 64, 8, 3)

    def rot_center(self):
        """rotate an image while keeping its center and size"""
        x, y = pygame.mouse.get_pos()
        relx, rely = x - self.rect.x, y - self.rect.y
        angle = math.atan2(relx, rely)
        angle = math.degrees(angle)
        orig_rect = self.image_original.get_rect()
        rot_image = pygame.transform.rotate(self.image_original, angle)
        rot_rect = orig_rect.copy()
        rot_rect.center = rot_image.get_rect().center
        rot_image = rot_image.subsurface(rot_rect).copy()
        return rot_image

    def update(self):
        """Rotates the player so that it follows the mouse"""
        if not self.dead:
            self.image = self.rot_center()
            self.mask = pygame.mask.from_surface(self.image)

        if self.health <= 0:
            self.dead = True
            self.image = self.ghost.update()
            self.mask = pygame.mask.from_surface(self.image)
