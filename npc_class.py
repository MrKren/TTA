import pygame
import math
from spritesheet import SpriteSheet


class NPC(pygame.sprite.Sprite):

    def __init__(self, player, speed):

        super().__init__()

        sprite_sheet = SpriteSheet("enemy.png")
        self.image_original = sprite_sheet.get_image(0, 0, 64, 64)
        self.image = self.image_original
        self.rect = self.image.get_rect()
        self.player = player
        self.player_pos = player.rect.centerx, player.rect.centery
        self.speed = speed

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
        self.player_pos = player.rect.centerx, player.rect.centery
        x, y = self.player_pos
        relx, rely = x-self.rect.x, y-self.rect.y
        angle = math.atan2(relx, rely)
        angle = math.degrees(angle)
        self.image = self.rot_center(angle)
        self.move_to_player(angle)

    def movex(self, speed):
        self.rect.x += speed

    def movey(self, speed):
        self.rect.y += speed

    def move_to_player(self, angle):
        xspeed, yspeed = self.speed*math.cos(angle), self.speed*math.sin(angle)
        if abs(angle) > 90:
            xspeed = -xspeed
        if angle > 0:
            yspeed = -yspeed
        self.rect.centerx += xspeed
        self.rect.centery += yspeed
