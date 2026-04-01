from settings import *

class Animator():
    def __init__(self):
        self.duration = 1000
        self.animation_sprites = pygame.sprite.Group()

    def swap(self, rects):
        for rect in rects:
            Animation(rect.center, SMOKE_FRAMES, self.animation_sprites)

    def attack(self, attacker_square, attacked_square):
        match type(attacker_square.piece).__name__:
            case 'Dragon':
                self.dragon_attack(attacker_square.piece.attack_squares)
            case 'Catapult':
                pass
    
    def dragon_attack(self, attack_squares):
        for square in attack_squares:
            Animation(square.rect.center, FLAME_FRAMES, self.animation_sprites)


    def catapult_attack(self):
        pass

    def update(self, dt):
        self.animation_sprites.update(dt)

class Animation(pygame.sprite.Sprite):
    def __init__(self, pos, frames, groups):
        super().__init__(groups)
        self.frames = frames
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