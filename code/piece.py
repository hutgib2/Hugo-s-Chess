from settings import *

class Piece(pygame.sprite.Sprite):
    def __init__(self, surf, size):
        super().__init__()
        self.image = pygame.transform.smoothscale(surf, (size, size))
        self.is_selected = False