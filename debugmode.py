import pygame
import psutil
import os


def debug_menu(fps, screen, pos, map_size, screenwidth=1080):
        """Creates a display of useful numbers"""

        # fps counter
        font = pygame.font.Font("freesansbold.ttf", 12)
        fps = round(fps)
        fps_text = font.render(str(fps), 1, (255, 255, 255))
        screen.blit(fps_text, ((screenwidth - 100), 5))

        # position
        coord = []
        for i in pos:
            i = round(i/(64*map_size**2), 1)  # Don't understand this conversion but it works so ¯\_(ツ)_/¯
            coord.append(i)
        coord_text = font.render(str(coord), 1, (255, 255, 255))
        screen.blit(coord_text, ((screenwidth - 100), 17))
        for i in coord:
            coord.remove(i)

        # RAM usage
        process = psutil.Process(os.getpid())
        ram = round(process.memory_info().rss / 1024 ** 2, 0)
        ram_text = font.render((str(ram) + " MB"), 1, (255, 255, 255))
        screen.blit(ram_text, ((screenwidth - 100), 30))
