import pygame   # Requires pygame module 'pip install pygame'
import random
"""import math"""
from player_class import Player     # Import classes
from terrain_gen import GenTerrain, GenTrees
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

        tile_sheet = SpriteSheet("tile.png")
        tile_image = tile_sheet.get_image(0, 0, 64, 64)
        tree_sheet = SpriteSheet("plant.png")
        tree_image = tree_sheet.get_image(0, 0, 65, 155), tree_sheet.get_image(128, 289, 97, 125)
        map_size = 100
        tile_size = 64

        # Generates terrain and tree
        font = pygame.font.Font("freesansbold.ttf", 72)  # Generating Terrain
        text = font.render("Generating Terrain", 1, WHITE)
        text_width, text_height = font.size("Generating Terrain")
        screen.blit(text, ((SCREENWIDTH - text_width)/2, (SCREENHEIGHT - text_height)/2))
        pygame.display.flip()
        terrain_gen = GenTerrain(tile_size, map_size, map_size, tile_image)
        tree_gen = GenTrees(tile_size, map_size, tree_image, 0.3)

        tile_list = pygame.sprite.Group()  # Add sprites to sprite groups
        for i in terrain_gen.tile_list:
                tile_list.add(i)
        tree_list = pygame.sprite.Group()
        for i in tree_gen.tree_list:
            tree_list.add(i)

        # Adds player sprite
        player_sprites = pygame.sprite.Group()
        player_sprites.add(player)

        carry_on = True  # Allowing the user to close the window...
        clock = pygame.time.Clock()

        rand_x_pos = random.randint(tile_size, ((map_size-1)*tile_size)-SCREENWIDTH/2)
        rand_y_pos = random.randint(tile_size, ((map_size-1)*tile_size)-SCREENHEIGHT/2)
        for i in tile_list:
            i.movex(-rand_x_pos)
            i.movey(-rand_y_pos)
        for i in tree_list:
            i.movex(-rand_x_pos)
            i.movey(-rand_y_pos)

        xcoord = 0
        ycoord = 0
        speed = 8
        debug = False
        render_tile_list = pygame.sprite.Group()
        render_tree_list = pygame.sprite.Group()

        while carry_on:  # Main game loop
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        carry_on = False

                keys = pygame.key.get_pressed()

                vx = 0
                vy = 0
                if keys[pygame.K_w]:
                    vy = speed
                if keys[pygame.K_a]:
                    vx = speed
                if keys[pygame.K_s]:
                    vy = -speed
                if keys[pygame.K_d]:
                    vx = -speed
                """ bug with diagonal speed code causes tiles and trees to glitch and move weirdly, possibly due to rendering code?
                if vx != 0 and vy != 0:
                    vx /= 1.414
                    vy /= 1.414
                    """
                for i in tree_list:
                    i.movex(vx)
                    i.movey(vy)
                for i in tile_list:
                    i.movex(vx)
                    i.movey(vy)
                    ycoord += vy
                    xcoord += vx

                if keys[pygame.K_F3] and debug is False:
                    debug = True
                    pygame.time.wait(100)
                elif keys[pygame.K_F3] and debug is True:
                    debug = False
                    pygame.time.wait(100)

                pos = xcoord, ycoord
                tile_list.update()  # Update sprite lists
                tree_list.update()
                player_sprites.update()

                # rendering code for terrain
                for i in tile_list:
                    if abs(i.rect.x - player.rect.x) < (SCREENWIDTH/2 + tile_size):
                        if abs(i.rect.y - player.rect.y) < (SCREENHEIGHT/2 + tile_size):
                            render_tile_list.add(i)
                for i in tree_list:
                    if abs(i.rect.x - player.rect.x) < (SCREENWIDTH / 2 + tile_size*2):
                        if abs(i.rect.y - player.rect.y) < (SCREENHEIGHT / 2 + tile_size*2):
                            render_tree_list.add(i)

                screen.fill(BLACK)  # Drawing on Screen

                render_tile_list.draw(screen)  # Draw sprites (order matters)
                player_sprites.draw(screen)
                render_tree_list.draw(screen)

                fps = clock.get_fps()
                if debug:
                    debug_menu(fps, screen, pos, map_size, SCREENWIDTH)

                pygame.display.flip()  # Refresh Screen

                clock.tick(30)  # Number of frames per second e.g. 60
                render_tile_list.empty()
                render_tree_list.empty()

        pygame.quit()


if __name__ == "__main__":
        main()
