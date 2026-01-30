from settings import *

class Piece(pygame.sprite.Sprite):
    def __init__(self, surf, color):
        super().__init__()
        self.image = pygame.transform.smoothscale(surf, (TILE_WIDTH, TILE_WIDTH))
        self.is_selected = False
        self.color = color
    


class Legionary(Piece):
    def __init(self, surf, color):
        super().__init__(surf, color)

    def possible_moves(self, coordinate):
        row, col = coordinate # extracts row and col from the coordinate
        if self.color == 'white':
            return [(row-1, col)] # returns the position in front of the legionary
        else:
            return [(row+1, col)]
    

