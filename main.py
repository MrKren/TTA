import pygame, random, os, sys
#Requires pygame module 'pip install pygame'

#Import classes
from player_class import Player
from terrain_gen import GenTerrain
from spritesheet import SpriteSheet

#useful colours
GREEN = (20, 255, 140)
GREY = (210, 210 ,210)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
PURPLE = (255, 0, 255)
YELLOW = (255, 255, 0)
CYAN = (0, 255, 255)
BLUE = (100, 100, 255)
BLACK = (0, 0, 0)

#screen resolution       
SCREENWIDTH=1080
SCREENHEIGHT=720


def main():
        """Main game function""" #docstring because I keep forgetting the word
        
        #Starts pygame
        pygame.init()

        #Creates window
        size = (SCREENWIDTH, SCREENHEIGHT)
        screen = pygame.display.set_mode(size)
        pygame.display.set_caption("Through The Ages")

        #Sprite and terrain generation
        player = Player()

        tile_sheet = SpriteSheet("Graphics/tile.png")
        tile_image = tile_sheet.get_image(0,0,64,64)
        map_size = 20
        
        font = pygame.font.Font(None, 72)
        text = font.render("Generating Terrain", 1, WHITE)
        screen.blit(text, (0, SCREENHEIGHT/2))
        pygame.display.flip()
        TerrainGen = GenTerrain(64, map_size, map_size, tile_image)


        #Add sprites to sprite groups
        
        tile_list = pygame.sprite.Group()
        for i in TerrainGen.tile_list:
                tile_list.add(i)
        
        player_sprites = pygame.sprite.Group()
        player_sprites.add(player)

        


        #Allowing the user to close the window...
        carryOn = True
        clock=pygame.time.Clock()

        #Main game loop
        while carryOn:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        carryOn = False

                keys = pygame.key.get_pressed()
                if keys[pygame.K_w]:
                        for i in tile_list:
                                i.Up(4)
                if keys[pygame.K_a]:
                        for i in tile_list:
                                i.Left(4)
                if keys[pygame.K_s]:
                        for i in tile_list:
                                i.Down(4)
                if keys[pygame.K_d]:
                        for i in tile_list:
                                i.Right(4)

                
                #Game Logic
                tile_list.update()
                player_sprites.update()

                #Drawing on Screen
                screen.fill(BLACK)
                
                #Darw sprites (order matters)
                tile_list.draw(screen)
                player_sprites.draw(screen)

                #fps counter
                font = pygame.font.Font(None, 12)
                fps = clock.get_fps()
                fps = round(fps, 0)
                text = font.render(str(fps), 1, (255, 255, 255))
                screen.blit(text, ((SCREENWIDTH-20), 5))

                #Refresh Screen
                pygame.display.flip()

                #Number of frames per secong e.g. 60
                clock.tick(60)

                

        pygame.quit()

if __name__ == "__main__":
        main()
