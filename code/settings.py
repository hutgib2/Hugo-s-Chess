import pygame
from os.path import join 
from os import walk
from support import folder_importer

pygame.init()
screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
WINDOW_WIDTH, WINDOW_HEIGHT = screen.get_size()

WHITE_SURFS = folder_importer('assets', 'images', 'white_pieces')
BLACK_SURFS = folder_importer('assets', 'images', 'black_pieces')
board_surf = pygame.image.load(join('assets', 'images', 'chess_board.jpg')).convert_alpha()
square_surf = pygame.image.load(join('assets', 'images', 'yellow_square.png')).convert_alpha()