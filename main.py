import pygame   # Requires pygame module 'pip install pygame'
import random
from player_class import Player     # Import classes
from terrain_gen import GenTerrain, GenTrees
from spritesheet import SpriteSheet
from debugmode import debug_menu
from npc_class import Enemy
from text import add_text, text_size
from weapon_class import Weapon
from gui import GUI, HealthBar, HealthBarBack

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

enemy_sheet = ["enemy_animation.png", "enemy.png"]
weapon_axe_sheet = ["weapon_axe_idle.png", "weapon_axe_idle.png", "weapon_axe_idle.png"]


def movexy(group, vx, vy, xcoord, ycoord):
    """Moves objects"""
    for i in group:
        for j in i:
            j.movex(vx)
            j.movey(vy)
    ycoord += vy
    xcoord -= vx
    return ycoord, xcoord


def main():
        """Main game function"""   # docstring because I keep forgetting the word

        pygame.init()      # Starts pygame

        size = (SCREENWIDTH, SCREENHEIGHT)
        screen = pygame.display.set_mode(size)  # Creates window
        pygame.display.set_caption("Through The Ages")

        # important variable
        xcoord = 0
        ycoord = 0
        speed = 8
        debug = False
        render_tile_list = pygame.sprite.Group()
        render_tree_list = pygame.sprite.Group()

        # Sprite and terrain generation

        tile_sheet = SpriteSheet("tile.png")
        tile_image = tile_sheet.get_image(0, 0, 64, 64)
        tree_sheet = SpriteSheet("plant.png")
        tree_image = tree_sheet.get_image(0, 0, 65, 155), tree_sheet.get_image(128, 289, 97, 125)
        trunk_image = tree_sheet.get_image(9, 435, 65, 155), tree_sheet.get_image(102, 469, 97, 125)
        map_size = 100
        tile_size = 64

        # Generates terrain and tree
        font = pygame.font.Font("freesansbold.ttf", 72)  # Generating Terrain
        text = font.render("Generating Terrain", 1, WHITE)
        text_width, text_height = font.size("Generating Terrain")
        screen.blit(text, ((SCREENWIDTH - text_width)/2, (SCREENHEIGHT - text_height)/2))
        pygame.display.flip()
        terrain_gen = GenTerrain(tile_size, map_size, map_size, tile_image)
        tree_gen = GenTrees(tile_size, map_size, tree_image, trunk_image, 0.1)

        tile_list = pygame.sprite.Group()  # Add sprites to sprite groups
        for i in terrain_gen.tile_list:
            tile_list.add(i)
        tree_list = pygame.sprite.Group()
        for i in tree_gen.tree_list:
            tree_list.add(i)

        # Adds player sprite
        player = Player()
        player_sprites = pygame.sprite.Group()
        player_sprites.add(player)

        weapon = Weapon(10, "Axe", weapon_axe_sheet)
        weapon_sprites = pygame.sprite.Group()
        weapon_sprites.add(weapon)

        enemy_list = pygame.sprite.Group()
        for i in range(5):
            i = Enemy(speed, enemy_sheet)
            i.rect.x = random.randint(player.rect.x, player.rect.x + tile_size*4)
            i.rect.y = random.randint(player.rect.y, player.rect.y + tile_size*4)
            enemy_list.add(i)
        print("Enemies", enemy_list)

        rand_x_pos = random.randint(tile_size, ((map_size-1)*tile_size)-SCREENWIDTH/2)
        rand_y_pos = random.randint(tile_size, ((map_size-1)*tile_size)-SCREENHEIGHT/2)
        for i in tile_list:
            i.movex(-rand_x_pos)
            i.movey(-rand_y_pos)
        for i in tree_list:
            i.movex(-rand_x_pos)
            i.movey(-rand_y_pos)

        # Creating GUI
        health_bar_back = HealthBarBack(player)
        health_bar = HealthBar(player)
        gui = GUI()
        gui_sprites = pygame.sprite.Group()
        gui_sprites.add(health_bar_back)
        gui_sprites.add(health_bar)
        gui_sprites.add(gui)


        carry_on = True  # Allowing the user to close the window...
        clock = pygame.time.Clock()

        move_sprites = (tile_list, tree_list, enemy_list)
        vulnerability = True
        vul_count = 0
        weapon_dead = False
        weapon_hit_list = []

        while carry_on:  # Main game loop
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        carry_on = False
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        buttons_pressed = pygame.mouse.get_pressed()
                        if buttons_pressed[0] and not player.dead:
                            weapon.state = "attack"

                screen.fill(BLACK)  # Drawing on Screen

                # Movement code
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

                ycoord, xcoord = movexy(move_sprites, vx, vy, xcoord, ycoord)

                if keys[pygame.K_F3] and debug is False:
                    debug = True
                    pygame.time.wait(100)
                elif keys[pygame.K_F3] and debug is True:
                    debug = False
                    pygame.time.wait(100)

                pos = xcoord, ycoord

                # other keyboard and mouse input

                # rendering code for terrain
                for i in tile_list:
                    if abs(i.rect.x - player.rect.x) < (SCREENWIDTH / 2 + tile_size):
                        if abs(i.rect.y - player.rect.y) < (SCREENHEIGHT / 2 + tile_size):
                            render_tile_list.add(i)
                for i in tree_list:
                    if abs(i.rect.x - player.rect.x) < (SCREENWIDTH / 2 + tile_size * 2):
                        if abs(i.rect.y - player.rect.y) < (SCREENHEIGHT / 2 + tile_size * 2):
                            render_tree_list.add(i)

                # collision code

                """Tree Collisions"""
                tree_hit_list = pygame.sprite.spritecollide(player, render_tree_list, False, pygame.sprite.collide_mask)
                if not player.dead:
                    for _ in tree_hit_list:
                        ycoord, xcoord = movexy(move_sprites, -vx, -vy, xcoord, ycoord)

                """Enemy Collisions"""
                enemy_hit_list = pygame.sprite.spritecollide(player, enemy_list, False, pygame.sprite.collide_mask)
                for _ in enemy_hit_list:
                    if vulnerability:
                        player.health -= 10
                        vulnerability = False

                if not vulnerability:
                    vul_count += 1
                    if vul_count > 10:
                        vul_count = 0
                        vulnerability = True

                """Weapon Collisions"""
                if not player.dead:
                    weapon_hit_list = pygame.sprite.spritecollide(weapon, enemy_list, False, pygame.sprite.collide_mask)
                for enemy in weapon_hit_list:
                    if not player.dead:
                        if not enemy.vulnerability and weapon.state == "attack":
                            enemy.damaged(weapon.damage)
                            print("damaged")

                for enemy in enemy_list:
                    if enemy.dead:
                        enemy.kill()
                        enemy = "Dead"
                        print(enemy)

                # Update sprite lists
                tile_list.update()
                tree_list.update()
                player_sprites.update()
                enemy_list.update(player)
                weapon_sprites.update(player)
                gui_sprites.update(player)

                render_tile_list.draw(screen)  # Draw sprites (order matters)
                enemy_list.draw(screen)
                player_sprites.draw(screen)
                weapon_sprites.draw(screen)
                render_tree_list.draw(screen)
                gui_sprites.draw(screen)

                fps = clock.get_fps()

                # debug menu
                if debug:
                    debug_menu(fps, screen, pos, SCREENWIDTH)

                # Inventory
                add_text(10, ("Health:" + " " + str(round(player.health))), WHITE, (70, 149), screen)

                # endgame
                if player.dead:
                    text_width, text_height = text_size(72, "Game Over")
                    add_text(72, "Game Over", WHITE,
                             ((SCREENWIDTH - text_width)/2, (SCREENHEIGHT - text_height - 200)/2),
                             screen)
                    vulnerability = False
                    if not weapon_dead:
                        weapon_dead = True
                        weapon.kill()
                        weapon = None

                pygame.display.flip()  # Refresh Screen

                clock.tick(30)  # Number of frames per second e.g. 60
                render_tile_list.empty()
                render_tree_list.empty()

        pygame.quit()


if __name__ == "__main__":
        main()
