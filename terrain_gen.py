import pygame


class Tile(pygame.sprite.Sprite):
    """Tile class that acts as a sprite"""

    #Creates sprite tile with image
    def __init__(self, original_image):

        super().__init__()
        
        self.image = original_image
        self.rect = self.image.get_rect()

    #Adds movement to the game
    def Left(self, speed):
        self.rect.x += speed

    def Right(self, speed):
        self.rect.x -= speed

    def Up(self, speed):
        self.rect.y += speed

    def Down(self, speed):
        self.rect.y -= speed

class GenTerrain(object):
    """Generates all tiles within a specified range"""

    def __init__(self, tile_size, l_x, l_y, image):
        
        #List of tiles that can be added to sprite Group
        self.tile_list = []

        #For loop that generates each sprite for each tile on the map
        for i in range(l_x):
            for j in range(l_y):
                xpos = i*tile_size
                ypos = j*tile_size
                pos = xpos, ypos
                tile = Tile(image)
                tile.rect.x, tile.rect.y = pos
                self.tile_list.append(tile)

        print("Tiles Added:", len(self.tile_list))

        

        

        
