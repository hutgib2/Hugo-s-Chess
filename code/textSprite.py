from settings import *

class TextSprite(pygame.sprite.Sprite):
    def __init__(self, text, pos, color, size, groups):
        super().__init__(groups)
        self.text = text
        self.font = pygame.font.Font(None, int(size))
        self.image = self.font.render(text, True, color)
        self.rect = self.image.get_frect(center=pos)
    
    def update(self):
        pygame.display.get_surface().blit(self.image, self.rect)

class Notification(TextSprite):
    def __init__(self, text, pos, color, size, groups):
        super().__init__(text, pos, color, size, groups)
        self.is_drawn = False
    
    def show(self):
        self.is_drawn = True

    def hide(self):
        self.is_drawn = False

    def update(self):
        if self.is_drawn:
            pygame.display.get_surface().blit(self.image, self.rect)