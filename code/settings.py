import pygame
from os.path import join 
from os import walk
from support import folder_importer

DIRECTIONS = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]

pygame.init()
screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
WINDOW_WIDTH, WINDOW_HEIGHT = screen.get_size()
BOARD_SIZE = WINDOW_HEIGHT - 100
TILE_WIDTH = BOARD_SIZE / 8

WHITE_SURFS = folder_importer('assets', 'images', 'white_pieces')
BLACK_SURFS = folder_importer('assets', 'images', 'black_pieces')
BOARD_SURFS = folder_importer('assets', 'images', 'board')
