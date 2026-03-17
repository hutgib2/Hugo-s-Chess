from settings import *

class Button(pygame.sprite.Sprite):
    def __init__(self, surf, pos, size, groups):
        super().__init__(groups)
        self.image = pygame.transform.smoothscale(surf, size)
        self.image_disabled = pygame.transform.smoothscale(surf, size)
        self.rect = self.image.get_frect(center=pos)
        self.is_active = True

    def deactivate(self):
        self.is_active = False

    def reactivate(self):
        self.is_active = True
    
    def update(self):
        if not self.is_active:
            pygame.display.get_surface().blit(self.image_disabled, self.rect)
        else:   
            pygame.display.get_surface().blit(self.image, self.rect)

class InteractiveButton(Button):
    def __init__(self, surf, pos, size, groups, callback):
        super().__init__(surf, pos, size, groups)
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
        