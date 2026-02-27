from os.path import join
from os import walk
from settings import pygame

def folder_importer(*path):
    surfs = {}
    for folder_path, _, file_names in walk(join(*path)):
        for file_name in file_names:
            full_path = join(folder_path, file_name)
            surfs[file_name.split('.')[0]] = pygame.image.load(full_path).convert_alpha()
    return surfs

def audio_importer(*path):
    audio_dict = {}
    for folder_path, _, file_names in walk(join(*path)):
        for file_name in file_names:
            audio_dict[file_name.split('.')[0]] = pygame.mixer.Sound(join(folder_path, file_name))
    return audio_dict

def get_all_moves(start, range, squares):
    move_squares = []
    DIRECTIONS = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
    for direction in DIRECTIONS:
        i = 1
        while i <= range:
            row = start[0] + direction[0] * i
            col = start[1] + direction[1] * i
            i += 1

            if row < 0 or row > 7 or col < 0 or col > 7:
                break
            
            if squares[row][col].piece != None:
                break
            
            move_squares.append(squares[row][col])
    return move_squares