from settings import *

class Piece(pygame.sprite.Sprite):
    def __init__(self, surf, color):
        super().__init__()
        self.image = pygame.transform.smoothscale(surf, (TILE_WIDTH, TILE_WIDTH))
        self.color = color

class Legionary(Piece):
    def __init(self, surf, color):
        super().__init__(surf, color)

    def possible_moves(self, coordinate):
        row, col = coordinate # extracts row and col from the coordinate
        possible_moves = []
        if self.color == 'white':
            # validate moves and append if valid
            if row > 0:
                possible_moves.append((row-1, col)) # returns the position in front of the legionary
        else:
            # validate moves and append if valid
            if row < 7:
                possible_moves.append((row+1, col))
        return possible_moves
    