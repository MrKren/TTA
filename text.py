import pygame


def add_text(size, text, colour, pos, screen):
    font = pygame.font.Font("freesansbold.ttf", size)
    text = font.render(text, 1, colour)
    screen.blit(text, pos)


def text_size(size, text):
    font = pygame.font.Font("freesansbold.ttf", size)
    text_width, text_height = font.size(text)
    return text_width, text_height
