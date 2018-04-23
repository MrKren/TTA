import pygame, random, os, sys, psutil, time
from player_class import Player
from terrain_gen import GenTerrain
from spritesheet import SpriteSheet
#Import classes

GREEN = (20, 255, 140)
GREY = (210, 210 ,210)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
PURPLE = (255, 0, 255)
YELLOW = (255, 255, 0)
CYAN = (0, 255, 255)
BLUE = (100, 100, 255)
BLACK = (0, 0, 0)
        
SCREENWIDTH=1080
SCREENHEIGHT=720

def main(mapx, mapy):
        pygame.init()

        size = (SCREENWIDTH, SCREENHEIGHT)
        screen = pygame.display.set_mode(size)
        pygame.display.set_caption("Through The Ages")

        #This will be a list that will contain all the sprites we intend to use in our game.
        player = Player()

        tile_sheet = SpriteSheet("Graphics/tile.png")
        tile_image = tile_sheet.get_image(0,0,64,64)
        
        font = pygame.font.Font(None, 72)
        text = font.render("Generating Terrain", 1, WHITE)
        screen.blit(text, (0, SCREENHEIGHT/2))
        pygame.display.flip()

        starttime = time.time()
        TerrainGen = GenTerrain(64, mapx, mapy, tile_image)
        endtime = time.time()

        totaltime = endtime- starttime

        # Add the car to the list of objects

        


        
        tile_list = pygame.sprite.Group()
        for i in TerrainGen.tile_list:
                tile_list.add(i)
        
        all_sprites_list = pygame.sprite.Group()
        all_sprites_list.add(player)

        


        #Allowing the user to close the window...
        carryOn = True
        clock=pygame.time.Clock()
        
        count = 0
        while carryOn:
                count += 1
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
                all_sprites_list.update()

                #Drawing on Screen
                screen.fill(BLACK)
                
                #Draw sprites (order matters)
                tile_list.draw(screen)
                all_sprites_list.draw(screen)

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
                process = psutil.Process(os.getpid())

                if count == 20:
                        carryOn = False
                
        
        pygame.quit()

        print("Time taken to generate:", totaltime, "FPS:", fps, "Memory used:", (process.memory_info().rss)/1024**2)
        return(totaltime, fps, (process.memory_info().rss)/1024**2)

test_space = [(x+1)*10 for x in range(100)]

print(test_space)

input()

f = open("output.dat", 'w')

for i in test_space:
        value = main(i,i)
        f.write(str(value) + '\n')


f.close()

input()


