from settings import *

class Piece(pygame.sprite.Sprite):
    def __init__(self, surf, color, squares):
        super().__init__()
        self.image = pygame.transform.smoothscale(surf, (TILE_WIDTH, TILE_WIDTH))
        self.color = color
        self.attack_squares = []
        self.squares = squares
        self.is_stunned = False
        self.stunned_at = None
        self.can_attack = True
        self.attacked_at = 0

    def attack_moves(self, coordinate):
        return []
    
    def attack(self, old_coord, attack_coord, round_num=0):
        pass
