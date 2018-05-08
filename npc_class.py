import pygame
import math
import random
from animate import Animation


class NPC(pygame.sprite.Sprite):

    def __init__(self, speed, sprite_sheets, screensize=(1080, 720)):

        super().__init__()

        self.idle = Animation(sprite_sheets[0], 64, 6, 3)
        self.image = self.idle.images[0]
        self.image_original = self.idle.images[0]
        self.rect = self.image.get_rect()
        self.speed = speed
        self.time = 0
        self.move = "L"
        self.screensize = screensize

    def update(self, player):
        """General updates for NPC"""
        self.image = self.idle.update()

    def movex(self, speed):
        self.rect.x += speed

    def movey(self, speed):
        self.rect.y += speed


class Enemy(NPC):

    def rot_center(self, player_pos):
        """rotate an image while keeping its center and size"""
        x, y = player_pos
        relx, rely = x - self.rect.x, y - self.rect.y
        angle = math.atan2(relx, rely)
        angle = math.degrees(angle)
        orig_rect = self.image_original.get_rect()
        rot_image = pygame.transform.rotate(self.image_original, angle)
        rot_rect = orig_rect.copy()
        rot_rect.center = rot_image.get_rect().center
        rot_image = rot_image.subsurface(rot_rect).copy()
        return rot_image

    def update(self, player):
        """General updates for NPC"""
        # rotating player
        self.time += 1
        player_pos = player.rect.centerx, player.rect.centery
        self.image_original = self.idle.update()
        self.image = self.rot_center(player_pos)

        if self.time > 15:
            self.move = random.choice(["L", "R", "U", "D"])
            self.time = 0

        self.ai_move(2, self.move)

        if (0 < self.rect.centerx < self.screensize[0]) or (0 < self.rect.centery < self.screensize[1]):
            pass
        else:
            self.ai_move(-2, self.move)

    def ai_move(self, speed, x):
        if x == "L":
            self.movex(-speed)
        if x == "R":
            self.movex(speed)
        if x == "U":
            self.movey(-speed)
        if x == "D":
            self.movey(speed)
