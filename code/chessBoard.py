from settings import *
from enum import Enum
from textSprite import TextSprite

class ChessBoard(pygame.sprite.Sprite):
    def __init__(self, surf, pos, width, groups):
        super().__init__(groups)
        self.image = pygame.transform.smoothscale(surf, (width, width))
        self.rect = self.image.get_frect(center=pos)
        self.width = width
        self.tile_width = self.width / 8
        self.gen_coordinates()
        self.groups = groups

    # creates a 2d list of rects representing the individual squares on the board
    def gen_coordinates(self):
        self.coordinates = [[], [], [], [], [], [], [], []] # creates a 2d list of empty coords and each list represent rows
        pos_x, pos_y = self.rect.topleft # starting the rows and columns from the top left

        for row in range(8):
            for col in range(8): 
                square = pygame.Rect(pos_x + (col * self.tile_width), pos_y, self.tile_width, self.tile_width) # creates a rect that specifies the area of a square
                self.coordinates[row].append(square) # appends the rect of the square to the coordinates list
            pos_y += self.tile_width # shifts to the next row


    def test_coordinates(self):
        for row in range(8):
            for col in range(8):
                square = self.coordinates[row][col]
                coordinate = f'({row}, {col})'
                TextSprite(coordinate, square.center, 'black', 50, self.groups)

    def update(self):
        pygame.display.get_surface().blit(self.image, self.rect)