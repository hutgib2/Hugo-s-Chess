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

class InteractiveText(TextSprite):
    def __init__(self, text, pos, color, size, callback, groups):
        super().__init__(text, pos, color, size, groups)
        self.image_hover = self.font.render(text, True, color)
        self.image_hover.set_alpha(128)
        self.callback = callback

    def is_clicked(self):
        self.callback()

    def update(self):
        if self.rect.collidepoint(pygame.mouse.get_pos()):
            pygame.display.get_surface().blit(self.image_hover, self.rect)
        else:
            pygame.display.get_surface().blit(self.image, self.rect)