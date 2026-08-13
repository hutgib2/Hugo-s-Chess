import pygame
from os.path import join
from os import walk
from utils.file_importer import load_images_named, load_images

DIRECTIONS = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]

pygame.init()
screen = pygame.display.set_mode((1280, 720))
WINDOW_WIDTH, WINDOW_HEIGHT = screen.get_size()
BOARD_SIZE = WINDOW_HEIGHT - 100
TILE_WIDTH = BOARD_SIZE / 8
BOARD_POS = (WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2)

WHITE_GRAVEYARD = [[], [], [], []]
BLACK_GRAVEYARD = [[], [], [], []]

PIECE_SURFS = {
    "white": load_images_named("assets", "images", "white_pieces"),
    "black": load_images_named("assets", "images", "black_pieces"),
}

FLAME_FRAMES = load_images("assets", "animations", "flame")
SMOKE_FRAMES = load_images("assets", "animations", "smoke")
SPLAT_FRAMES = load_images("assets", "animations", "splat")
BOARD_SURFS = load_images_named("assets", "images", "board")

PIECE_SCORES = {
    "legionary": 1,
    "wizard": 3,
    "dragon": 3,
    "catapult": 3,
    "archer": 5,
    "emperor": 10,
}
