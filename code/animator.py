from settings import *
from support import get_direction_between

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

class Boulder(pygame.sprite.Sprite):
    def __init__(self, pos, direction, enemy_pieces, groups):
        super().__init__(groups)
        self.original_surf = pygame.transform.smoothscale(BOARD_SURFS['boulder'], (TILE_WIDTH-50, TILE_WIDTH-50)) 
        self.image = self.original_surf
        self.rect = self.image.get_frect(center = pos) 
        self.spawn_time = pygame.time.get_ticks()
        self.lifetime = 1000
        self.direction = direction
        self.speed = 1400
        self.enemy_pieces = enemy_pieces
        self.killed_first = False
        self.rotation_speed = 256
        self.rotation = 0
    
    def update(self, dt, round_num):
        if pygame.time.get_ticks() - self.spawn_time >= self.lifetime:
            self.kill()
        self.rotation += self.rotation_speed * dt
        self.image = pygame.transform.rotozoom(self.original_surf, self.rotation, 1)
        self.rect.center += self.direction * self.speed * dt
        pygame.display.get_surface().blit(self.image, self.rect)

        collision_sprites = pygame.sprite.spritecollide(self, self.enemy_pieces, False, pygame.sprite.collide_mask)

        for piece in collision_sprites:
            if self.killed_first == False:
                piece.remove_piece()
                self.killed_first = True
            else:
                piece.is_stunned = True
                piece.stunned_at = round_num

class Arrow(pygame.sprite.Sprite):
    def __init__(self, attacked_square, direction, groups):
        super().__init__(groups)
        self.image = pygame.transform.smoothscale(BOARD_SURFS['arrow'], (TILE_WIDTH-50, TILE_WIDTH-50)) 
        self.spawn_time = pygame.time.get_ticks()
        self.lifetime = 1000
        self.direction = direction
        self.speed = 1400
        self.set_position_and_angle(attacked_square, direction)
    
    def set_position_and_angle(self, attacked_square, direction):
        match tuple(direction):
            case (0, 1):
                angle = 0
                pos = attacked_square.rect.midtop
            case (1, 1):
                angle = 45
                pos = attacked_square.rect.topleft
            case (1, 0):
                angle = 90
                pos = attacked_square.rect.midleft
            case (1, -1):
                angle = 135
                pos = attacked_square.rect.bottomleft
            case (0, -1):
                angle = 180
                pos = attacked_square.rect.midbottom
            case (-1, 0):
                angle = -90
                pos = attacked_square.rect.midright
            case (-1, -1):
                angle = -135
                pos = attacked_square.rect.bottomright
            case (-1, 1):
                angle = -45
                pos = attacked_square.rect.topright

        self.image = pygame.transform.rotozoom(self.image, angle, 1)
        self.rect = self.image.get_frect(center = pos) 
    
    def update(self, dt, _):
        if pygame.time.get_ticks() - self.spawn_time >= self.lifetime:
            self.kill()
    #     self.rect.center += self.direction * self.speed * dt
        pygame.display.get_surface().blit(self.image, self.rect)