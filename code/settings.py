import pygame
from os.path import join 
from os import walk
from support import folder_importer, folder_importer_list

DIRECTIONS = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]

pygame.init()
screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
WINDOW_WIDTH, WINDOW_HEIGHT = screen.get_size()
BOARD_SIZE = WINDOW_HEIGHT - 100
TILE_WIDTH = BOARD_SIZE / 8

PIECE_SURFS = {
    'white': folder_importer('assets', 'images', 'white_pieces'),
    'black': folder_importer('assets', 'images', 'black_pieces'),
}

FLAME_FRAMES = folder_importer_list('assets', 'animations', 'flame')
SMOKE_FRAMES = folder_importer_list('assets', 'animations', 'smoke')
BOARD_SURFS = folder_importer('assets', 'images', 'board')

PIECE_SCORES = {
    "Legionary": 1,
    "Wizard": 3,
    "Dragon": 3,
    "Catapult": 5,
    "Archer": 9,
}