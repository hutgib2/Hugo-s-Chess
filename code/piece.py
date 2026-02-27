from settings import *

class Piece(pygame.sprite.Sprite):
    def __init__(self, surf, color, squares):
        super().__init__()
        self.image = pygame.transform.smoothscale(surf, (TILE_WIDTH, TILE_WIDTH))
        self.color = color
        self.attack_squares = []
        self.move_squares = []
        self.squares = squares
        self.is_stunned = False
        self.stunned_at = None
        self.can_attack = True
        self.attacked_at = 0


