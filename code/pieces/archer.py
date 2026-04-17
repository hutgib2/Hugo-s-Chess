from settings import *
from pieces.piece import Piece

class Archer(Piece):
    def __init__(self, id, color, coord, squares):
        super().__init__(id, 'archer', color, coord, squares)
        self.type = "archer"
        self.attack_directions = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
        self.attack_range = (2, 3)
        self.move_directions = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
        self.move_range = 1

    def attack(self, attack_coord, round_num=0):
        attack_square = self.squares[attack_coord[0]][attack_coord[1]]
        score = PIECE_SCORES[attack_square.piece.type]
        attack_square.piece.remove_piece()
        return score

class Arrow(pygame.sprite.Sprite):
    def __init__(self, attacked_square, direction, groups):
        super().__init__(groups)
        self.image = pygame.transform.smoothscale(BOARD_SURFS['arrow'], (TILE_WIDTH-50, TILE_WIDTH-50)) 
        self.attacked_square = attacked_square
        self.direction = direction
        self.spawn_time = pygame.time.get_ticks()
        self.lifetime = 1000
        self.speed = 2000
        self.set_position_and_angle()
    
    def set_position_and_angle(self,):
        match tuple(self.direction):
            case (0, 1):
                angle = 0
                pos = self.attacked_square.rect.midtop
            case (1, 1):
                angle = 45
                pos = self.attacked_square.rect.topleft
            case (1, 0):
                angle = 90
                pos = self.attacked_square.rect.midleft
            case (1, -1):
                angle = 135
                pos = self.attacked_square.rect.bottomleft
            case (0, -1):
                angle = 180
                pos = self.attacked_square.rect.midbottom
            case (-1, 0):
                angle = -90
                pos = self.attacked_square.rect.midright
            case (-1, -1):
                angle = -135
                pos = self.attacked_square.rect.bottomright
            case (-1, 1):
                angle = -45
                pos = self.attacked_square.rect.topright

        self.image = pygame.transform.rotozoom(self.image, angle, 0.85)
        self.rect = self.image.get_frect(center = pos) 
        self.rect.center += self.direction # adding tiny offset so initial collision is detected at boundary 

    def update(self, dt, _):
        if pygame.time.get_ticks() - self.spawn_time >= self.lifetime:
            self.kill()

        if self.attacked_square.rect.collidepoint(self.rect.center + (self.direction * TILE_WIDTH / 3)):
            self.rect.center += self.direction * self.speed * dt

        pygame.display.get_surface().blit(self.image, self.rect)