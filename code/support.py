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

def folder_importer_list(*path):
    surf_list = []
    for folder_path, _, file_names in walk(join(*path)):
        for file_name in sorted(file_names, key = lambda name: int(name.split('.')[0])):
            full_path = join(folder_path, file_name)
            surf = pygame.transform.scale(pygame.image.load(full_path), (128, 128)).convert_alpha()
            surf_list.append(surf)
    return surf_list


def audio_importer(*path):
    audio_dict = {}
    for folder_path, _, file_names in walk(join(*path)):
        for file_name in file_names:
            audio_dict[file_name.split('.')[0]] = pygame.mixer.Sound(join(folder_path, file_name))
    return audio_dict

def get_direction_between(start, end):
    drow = end[0] - start[0]
    dcol = end[1] - start[1]
    if drow != 0:
        drow = drow / abs(drow)
        
    if dcol != 0:
        dcol = dcol / abs(dcol)

    return (int(drow), int(dcol))