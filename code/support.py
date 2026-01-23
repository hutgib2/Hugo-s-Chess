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

def split_string(string):
    i = int(len(string)/2)
    while i < (len(string) - 1) and string[i] != ' ':
        i += 1
    
    if i == (len(string) - 1):
        while i > 0 and string[i] != ' ':
            i -= 1
    if i == 0:
        return string
    else:
        return string[:i] + '\n' + string[i+1:]