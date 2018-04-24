import pygame   # Requires pygame module 'pip install pygame'
import random
from player_class import Player     # Import classes
from terrain_gen import GenTerrain
from spritesheet import SpriteSheet
from debugmode import debug_menu


GREEN = (20, 255, 140)  # useful colours
GREY = (210, 210, 210)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
PURPLE = (255, 0, 255)
YELLOW = (255, 255, 0)
CYAN = (0, 255, 255)
BLUE = (100, 100, 255)
BLACK = (0, 0, 0)


SCREENWIDTH = 1080   # screen resolution
SCREENHEIGHT = 720


def main():
        """Main game function"""   # docstring because I keep forgetting the word

        pygame.init()      # Starts pygame

        size = (SCREENWIDTH, SCREENHEIGHT)
        screen = pygame.display.set_mode(size)  # Creates window
        pygame.display.set_caption("Through The Ages")

        player = Player()  # Sprite and terrain generation

        tile_sheet = SpriteSheet("Graphics/tile.png")
        tile_image = tile_sheet.get_image(0, 0, 64, 64)
        map_size = 20
        tile_size = 64
        
        font = pygame.font.Font(None, 72)  # Generating Terrain
        text = font.render("Generating Terrain", 1, WHITE)
        screen.blit(text, (0, SCREENHEIGHT/2))
        pygame.display.flip()
        terrain_gen = GenTerrain(tile_size, map_size, map_size, tile_image)

        tile_list = pygame.sprite.Group()  # Add sprites to sprite groups
        for i in terrain_gen.tile_list:
                tile_list.add(i)
        
        player_sprites = pygame.sprite.Group()
        player_sprites.add(player)

        carry_on = True  # Allowing the user to close the window...
        clock = pygame.time.Clock()

        rand_x_pos = random.randint(tile_size, ((map_size-1)*tile_size)-SCREENWIDTH/2)
        rand_y_pos = random.randint(tile_size, ((map_size-1)*tile_size)-SCREENHEIGHT/2)
        for i in tile_list:
            i.right(rand_x_pos)
            i.down(rand_y_pos)

        xcoord = 0
        ycoord = 0
        speed = 4
        debug = False

        while carry_on:  # Main game loop
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        carry_on = False

                keys = pygame.key.get_pressed()
                if keys[pygame.K_w]:
                        for i in tile_list:
                            i.up(speed)
                            ycoord += speed/64
                if keys[pygame.K_a]:
                        for i in tile_list:
                            i.left(speed)
                            xcoord -= speed/64
                if keys[pygame.K_s]:
                        for i in tile_list:
                            i.down(speed)
                            ycoord -= speed/64
                if keys[pygame.K_d]:
                        for i in tile_list:
                            i.right(4)
                            xcoord += speed/64
                if keys[pygame.K_F3] and debug is False:
                    debug = True
                    pygame.time.wait(100)
                elif keys[pygame.K_F3] and debug is True:
                    debug = False
                    pygame.time.wait(100)

                pos = xcoord, ycoord
                tile_list.update()  # Update sprite lists
                player_sprites.update()

                screen.fill(BLACK)  # Drawing on Screen

                tile_list.draw(screen)  # Draw sprites (order matters)
                player_sprites.draw(screen)

                fps = clock.get_fps()
                if debug:
                    debug_menu(fps, screen, pos, SCREENWIDTH)

                pygame.display.flip()  # Refresh Screen

                clock.tick(60)  # Number of frames per second e.g. 60

        pygame.quit()


if __name__ == "__main__":
        main()
