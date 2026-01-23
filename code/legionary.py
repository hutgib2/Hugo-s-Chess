from settings import *

class Legionary(pygame.sprite.Sprite):
    def __init__(self, surf, pos, size, groups):
        super().__init__(groups)
        self.image = pygame.transform.smoothscale(surf, (size, size))
        self.rect = self.image.get_frect(center=pos)
        

    def update(self):
        pygame.display.get_surface().blit(self.image, self.rect)