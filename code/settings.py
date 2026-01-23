import pygame
from os.path import join 
from os import walk
from support import folder_importer

pygame.init()
screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
WINDOW_WIDTH, WINDOW_HEIGHT = screen.get_size()

SURFS = folder_importer('assets', 'images')