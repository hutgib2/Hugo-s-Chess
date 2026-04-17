from settings import *
from support import get_direction_between
from pieces.archer import Arrow
from pieces.catapult import Boulder

class Animator():
    def __init__(self):
        self.animation_sprites = pygame.sprite.Group()

    def swap(self, rects):
        for rect in rects:
            Animation(rect.center, SMOKE_FRAMES, self.animation_sprites)

    def attack(self, attacker_square, attacked_square, enemy_pieces):
        match attacker_square.piece.type:
            case 'dragon':
                self.dragon_attack(attacker_square.piece.attack_squares)
            case 'catapult':
                self.catapult_attack(attacker_square, attacked_square, enemy_pieces)
            case 'archer':
                self.archer_attack(attacker_square, attacked_square)
    
    def dragon_attack(self, attack_squares):
        for square in attack_squares:
            Animation(square.rect.center, FLAME_FRAMES, self.animation_sprites)

    def catapult_attack(self, attacker_square, attacked_square, enemy_pieces):
        attack_direction = get_direction_between(attacker_square.coord, attacked_square.coord)
        direction = pygame.Vector2(attack_direction[1], attack_direction[0])
        Boulder(attacker_square.rect.center, direction, enemy_pieces, self.animation_sprites)

    def archer_attack(self, attacker_square, attacked_square):
        attack_direction = get_direction_between(attacker_square.coord, attacked_square.coord)
        direction = pygame.Vector2(attack_direction[1], attack_direction[0])

        Arrow(attacked_square, direction, self.animation_sprites)

    def update(self, dt, round_num):
        self.animation_sprites.update(dt, round_num)

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
    
    def update(self, dt, _):
        if pygame.time.get_ticks() - self.spawn_time >= self.lifetime:
            self.kill()
        self.animate(dt)