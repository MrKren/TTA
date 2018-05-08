import pygame
from animate import Animation
import math


class Weapon(pygame.sprite.Sprite):

    def __init__(self, damage, w_type, sprite_sheets):

        super().__init__()

        self.idle = Animation(sprite_sheets[0], 128, 8, 1)
        self.attack = Animation(sprite_sheets[1], 128, 8, 4)
        self.block = Animation(sprite_sheets[2], 128, 8, 1)
        self.state = "idle"
        self.count = 0

        self.image = self.idle.images[0]
        self.mask = pygame.mask.from_surface(self.image)
        self.image_original = self.idle.images[0]
        self.rect = self.image.get_rect()

        self.damage = damage
        self.type = w_type

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

    def special_ability(self):
        pass

    def update(self, player):
        self.count += 1

        if self.state == "idle":
            self.image_original = self.idle.images[0]
            self.count = 0
        if self.state == "attack":
            self.image_original = self.attack.update()
            if self.count >= self.attack.frame_loop:
                self.state = "idle"
        if self.state == "block":
            self.image_original = self.block.update()
            if self.count >= self.block.frame_loop:
                self.state = "idle"

        self.image = self.rot_center()
        self.rect.centerx = player.rect.centerx
        self.rect.centery = player.rect.centery
        self.mask = pygame.mask.from_surface(self.image)
