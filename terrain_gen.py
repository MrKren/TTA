import pygame
import random


class Tile(pygame.sprite.Sprite):
    """Tile class that acts as a sprite"""

    # Creates sprite tile with image
    def __init__(self, original_image, mask_image):

        super().__init__()
        
        self.image = original_image
        self.mask_image = mask_image
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.mask_image)

    # Adds movement to the game
    def movex(self, speed):
        self.rect.x += speed

    def movey(self, speed):
        self.rect.y += speed


class GenTerrain(object):
    """Generates all tiles within a specified range"""

    def __init__(self, tile_size, l_x, l_y, image):
        
        # List of tiles that can be added to sprite Group
        self.tile_list = []

        # For loop that generates each sprite for each tile on the map
        for i in range(l_x):
            for j in range(l_y):
                xpos = i*tile_size
                ypos = j*tile_size
                pos = xpos, ypos
                tile = Tile(image, image)
                tile.rect.x, tile.rect.y = pos
                self.tile_list.append(tile)

        print("Tiles Added:", len(self.tile_list))


class GenTrees(object):

    def __init__(self, tile_size, map_size, images, mask_images, percentage):

        global mask_image
        self.tree_list = []

        for i in range(map_size-2):
            for j in range(map_size-3):
                if random.randrange(0, 10000, 1)/10000 < percentage:
                    xpos = (i+1)*tile_size
                    ypos = (j+1)*tile_size
                    pos = xpos, ypos
                    tree_image = random.choice(images)
                    if tree_image == images[0]:
                        mask_image = mask_images[0]
                    if tree_image == images[1]:
                        mask_image = mask_images[1]
                    tree = Tile(tree_image, mask_image)
                    tree.rect.x, tree.rect.y = pos
                    self.tree_list.append(tree)

        print("Trees Added:", len(self.tree_list))
