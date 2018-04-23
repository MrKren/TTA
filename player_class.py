#Player class
import pygame, math, os, sys
from spritesheet import SpriteSheet


class Player(pygame.sprite.Sprite):
    """Player class that is used to create player sprite as well as control player attributes"""

    def __init__(self):
        #initialisation of class

        super().__init__()

        sprite_sheet = SpriteSheet('Graphics/character.png')
        
        self.image = sprite_sheet.get_image(0,0,64,64)
        self.original_image = self.image
        self.speed = 5
        self.rect = self.image.get_rect()
        self.rect.x = 540 - self.rect.centerx
        self.rect.y = 360 - self.rect.centery

    def rot_center(self, angle, image):
        #rotate an image while keeping its center and size
        orig_rect = image.get_rect()
        rot_image = pygame.transform.rotate(image, angle)
        rot_rect = orig_rect.copy()
        rot_rect.center = rot_image.get_rect().center
        rot_image = rot_image.subsurface(rot_rect).copy()
        return rot_image

    def update(self):
        #Roatates the player so that it follows the mouse
        x,y = pygame.mouse.get_pos()
        relx,rely = x-self.rect.x, y-self.rect.y
        angle = math.atan2(relx, rely)
        angle = math.degrees(angle)
        self.image = self.rot_center(angle, self.original_image)
        

