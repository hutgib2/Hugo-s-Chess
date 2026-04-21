from settings import *
from textSprite import TextSprite

class Button(pygame.sprite.Sprite):
    def __init__(self, surf, pos, size, groups, text=''):
        super().__init__(groups)
        self.image = pygame.transform.smoothscale(surf, size)
        self.image_disabled = pygame.transform.smoothscale(surf, size)
        self.rect = self.image.get_frect(center=pos)
        self.is_active = True
        self.text_sprite = TextSprite(text, self.rect.center, "darkcyan", self.rect.width / 6, ())

    def deactivate(self):
        self.is_active = False

    def reactivate(self):
        self.is_active = True
    
    def update(self):
        if not self.is_active:
            pygame.display.get_surface().blit(self.image_disabled, self.rect)
        else:   
            pygame.display.get_surface().blit(self.image, self.rect)
        pygame.display.get_surface().blit(self.text_sprite.image, self.text_sprite.rect)

class InteractiveButton(Button):
    def __init__(self, surf, pos, size, groups, callback, text=''):
        super().__init__(surf, pos, size, groups, text)
        self.image_hover = pygame.transform.smoothscale(surf, size)
        self.image_hover.set_alpha(180)
        self.callback = callback

    def is_clicked(self):
        if self.is_active:
            self.callback()
    
    def update(self):
        if not self.is_active:
            pygame.display.get_surface().blit(self.image_disabled, self.rect)
        elif self.rect.collidepoint(pygame.mouse.get_pos()):
            pygame.display.get_surface().blit(self.image_hover, self.rect)
        else:   
            pygame.display.get_surface().blit(self.image, self.rect)
        pygame.display.get_surface().blit(self.text_sprite.image, self.text_sprite.rect)
        