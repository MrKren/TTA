import pygame
import math
import random
from spritesheet import SpriteSheet


class NPC(pygame.sprite.Sprite):

    def __init__(self, player, speed, screensize=(1080, 720)):

        super().__init__()

        sprite_sheet = SpriteSheet("enemy.png")
        self.image_original = sprite_sheet.get_image(0, 0, 64, 64)
        self.image_original = pygame.transform.flip(self.image_original, False, True)
        self.image = self.image_original
        self.rect = self.image.get_rect()
        self.player = player
        self.player_pos = player.rect.centerx, player.rect.centery
        self.speed = speed
        self.time = 0
        self.move = "L"
        self.screensize = screensize

    def rot_center(self, angle):
        """rotate an image while keeping its center and size"""
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
        self.player_pos = player.rect.centerx, player.rect.centery
        x, y = self.player_pos
        relx, rely = x-self.rect.x, y-self.rect.y
        angle = math.atan2(relx, rely)
        angle = math.degrees(angle)
        self.image = self.rot_center(angle)

        if self.time > 10:
            self.move = random.choice(["L", "R", "U", "D"])
            self.time = 0
        else:
            self.ai_move(8, self.move)
        if (0 < self.rect.centerx < self.screensize[0]) or (0 < self.rect.centery < self.screensize[1]):
            self.ai_move(-8, self.move)

    def movex(self, speed):
        self.rect.x += speed

    def movey(self, speed):
        self.rect.y += speed

    def ai_move(self, speed, x):
        if x == "L":
            self.movex(-speed)
        if x == "R":
            self.movex(speed)
        if x == "U":
            self.movey(-speed)
        if x == "D":
            self.movey(speed)
