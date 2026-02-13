from settings import *

class Piece(pygame.sprite.Sprite):
    def __init__(self, surf, color, squares):
        super().__init__()
        self.image = pygame.transform.smoothscale(surf, (TILE_WIDTH, TILE_WIDTH))
        self.color = color
        self.squares = squares
        self.is_stunned = False

    def kill_moves(self, coordinate):
        return []
    
    def kill(self, old_coord, kill_coord):
        pass
