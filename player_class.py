import pygame
import math
from spritesheet import SpriteSheet


class Player(pygame.sprite.Sprite):
    """Player class that is used to create player sprite as well as control player attributes"""

    def __init__(self):
        """initialisation of class"""

        super().__init__()

        sprite_sheet = SpriteSheet('character.png')

        self.image = sprite_sheet.get_image(0, 0, 64, 64)
        self.image_original = self.image
        self.mask = pygame.mask.from_surface(self.image)
        self.speed = 5
        self.rect = self.image.get_rect()
        self.rect.x = 540 - self.rect.centerx
        self.rect.y = 360 - self.rect.centery

    def rot_center(self, angle):
        """rotate an image while keeping its center and size"""
        orig_rect = self.image_original.get_rect()
        rot_image = pygame.transform.rotate(self.image_original, angle)
        rot_rect = orig_rect.copy()
        rot_rect.center = rot_image.get_rect().center
        rot_image = rot_image.subsurface(rot_rect).copy()
        return rot_image

    def update(self):
        """Rotates the player so that it follows the mouse"""
        x, y = pygame.mouse.get_pos()
        relx, rely = x - self.rect.x, y - self.rect.y
        angle = math.atan2(relx, rely)
        angle = math.degrees(angle)
        self.image = self.rot_center(angle)
        self.mask = pygame.mask.from_surface(self.image)
