from settings import *
from pieces.piece import Piece
from support import get_direction_between

class Catapult(Piece):
    def __init__(self, id, color, coord, squares):
        super().__init__(id, 'catapult',  color, coord, squares)
        self.type = "catapult"
        self.attack_directions = self.move_directions = [(-1, 0), (0, 1), (0, -1), (1, 0)]
        self.attack_range = (1, 7)
        self.move_range = 2

    def update_attack_moves(self):
        from pieces.legionary import Legionary
        from pieces.emperor import Emperor

        self.attack_squares = []
        if self.is_reloading:
            return
        for direction in self.attack_directions:
            i = self.attack_range[0]
            while i <= self.attack_range[1]:
                row = self.coord[0] + direction[0] * i
                col = self.coord[1] + direction[1] * i
                i += 1
                if row < 0 or row > 7 or col < 0 or col > 7:
                    break
                
                square = self.squares[row][col]
                if not square.piece:
                    self.attack_squares.append(square)
                    continue
                elif square.piece.color == self.color:
                    break
                elif type(square.piece) == Legionary:
                    if self.color == 'white' and direction == (-1, 0):
                        break
                    elif self.color == 'black' and direction == (1, 0):
                        break
                self.attack_squares.append(square)
                break

    def attack(self, attack_coord, round_num):
        from pieces.legionary import Legionary
        attack_direction = get_direction_between(self.coord, attack_coord)
        i = self.attack_range[0]
        while i <= self.attack_range[1]:
            row = self.coord[0] + attack_direction[0] * i
            col = self.coord[1] + attack_direction[1] * i
            i += 1
            if row < 0 or row > 7 or col < 0 or col > 7:
                break
            square = self.squares[row][col]
            if not square.piece:
                continue
            if square.piece.color == self.color:
                break
            elif type(square.piece) == Legionary and attack_direction == self.attack_directions[0]:
                break
            return [square.piece]

class Boulder(pygame.sprite.Sprite):
    def __init__(self, pos, direction, all_pieces, attacker, groups):
        super().__init__(groups)
        self.original_surf = pygame.transform.smoothscale(BOARD_SURFS['boulder'], (TILE_WIDTH-50, TILE_WIDTH-50)) 
        self.image = self.original_surf
        self.rect = self.image.get_frect(center = pos) 
        self.spawn_time = pygame.time.get_ticks()
        self.lifetime = 1000
        self.direction = direction
        self.speed = 1400
        self.all_pieces = all_pieces
        self.killed_first = False
        self.rotation_speed = 256
        self.rotation = 0
        self.color = attacker.color
        self.attacker = attacker

    def block(self):
        self.speed = 0
        self.rotation_speed *= 0.97
    
    def update(self, dt, round_num):
        from pieces.legionary import Legionary
        from pieces.emperor import Emperor
        if pygame.time.get_ticks() - self.spawn_time >= self.lifetime:
            self.kill()
        self.rotation += self.rotation_speed * dt
        self.image = pygame.transform.rotozoom(self.original_surf, self.rotation, 1)
        self.rect.center += self.direction * self.speed * dt
        pygame.display.get_surface().blit(self.image, self.rect)

        collision_sprites = pygame.sprite.spritecollide(self, self.all_pieces, False, pygame.sprite.collide_mask)
        for piece in collision_sprites:
            if piece.color == self.color and piece != self.attacker:
                self.block()
                break
            if self.killed_first == False:
                if piece.color != self.color:
                    piece.remove_piece()
                    self.killed_first = True
                    continue
            elif type(piece) == Legionary:
                if piece.color == 'white' and self.direction == pygame.Vector2(0, 1):
                    self.block()
                    break
                elif piece.color == 'black' and self.direction == pygame.Vector2(0, -1):
                    self.block()
                    break
            elif type(piece) == Emperor:
                self.block()
                break
            if piece.color != self.color:
                piece.is_stunned = True
                piece.stunned_at = round_num
