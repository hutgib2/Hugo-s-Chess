from settings import *

class Piece(pygame.sprite.Sprite):
    def __init__(self, surf, color, squares):
        super().__init__()
        self.image = pygame.transform.smoothscale(surf, (TILE_WIDTH, TILE_WIDTH))
        self.color = color
        self.squares = squares

