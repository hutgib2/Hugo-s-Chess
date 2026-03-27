from settings import *
from pieces.piece import Piece


class Dragon(Piece):
    def __init__(self, surf, color, coord, squares, groups, is_stunned=False, stunned_at=0, is_reloading=False, attacked_at=0):
        super().__init__(surf, color, coord, squares, groups, is_stunned, stunned_at, is_reloading, attacked_at)
        self.attack_range = (1,1)
        if self.color == 'white':
            self.attack_directions = [(-1, -1), (-1, 0), (-1, 1), (0, 1), (0, -1)]
        elif self.color == 'black':
            self.attack_directions = [(1, -1), (1, 0), (1, 1), (0, 1), (0, -1)]
        
        self.move_directions = [(1, -2), (1, 2), (-1, 2), (-1, -2,), (2, 1), (2, -1), (-2, 1), (-2, -1)]
        self.move_range = 1

    def attack(self, old_coord, attack_coord, round_num=0):
        for square in self.attack_squares:
            square.piece = None
    
    def animate_attack(self):
        for square in self.attack_squares:
            Flame(square.rect.center, self.groups)

class Flame(pygame.sprite.Sprite):
    def __init__(self, pos, groups):
        super().__init__(groups)
        self.frames = FLAME_ANIMATION
        self.image = self.frames[0]
        self.rect = self.image.get_frect(center = pos)
        self.spawn_time = pygame.time.get_ticks()
        self.lifetime = 1000
        self.frame_index = 0
        self.animation_speed = 15

    def animate(self, dt):
        self.frame_index += self.animation_speed * dt
        self.image = self.frames[int(self.frame_index) % len(self.frames)]
        pygame.display.get_surface().blit(self.image, self.rect)
    
    def update(self, dt):
        if pygame.time.get_ticks() - self.spawn_time >= self.lifetime:
            self.kill()
        self.animate(dt)