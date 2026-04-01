from settings import *
from pieces.piece import Piece

class Catapult(Piece):
    def __init__(self, surf, color, coord, squares, groups, is_stunned=False, stunned_at=0, is_reloading=False, attacked_at=0):
        super().__init__(surf, color, coord, squares, groups, is_stunned, stunned_at, is_reloading, attacked_at)
        if self.color == 'white':
            self.attack_directions = [(-1, 0), (0, 1), (0, -1)]
        elif self.color == 'black':
            self.attack_directions = [(1, 0), (0, 1), (0, -1)]
        self.attack_range = (1, 7)
        self.move_directions = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
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
                elif square.piece.color == self.color:
                    break
                elif type(square.piece) == Legionary and direction == self.attack_directions[0]:
                    break
                else:
                    self.attack_squares.append(square)


    def get_attack_direction(self, attack_square):
        drow = attack_square[0] - self.coord[0]
        dcol = attack_square[1] - self.coord[1]
        if drow != 0:
            drow = drow / abs(drow)
            
        if dcol != 0:
            dcol = dcol / abs(dcol)

        attack_direction = (int(drow), int(dcol))
        return attack_direction

    # def animate_attack(self, attack_square):
    #     attack_direction = self.get_attack_direction(attack_square)
    #     direction = pygame.Vector2(attack_direction[1], attack_direction[0])
    #     square = self.squares[self.coord[0]][self.coord[1]]
    #     Boulder(square.rect.center, direction, self.groups)
        
            
    def attack(self, attack_square, round_num):
        from pieces.legionary import Legionary

        attack_direction = self.get_attack_direction(attack_square)
        killed_first = False
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
            if killed_first == False:
                square.piece = None
                killed_first = True
            else:
                square.piece.is_stunned = True
                square.piece.stunned_at = round_num

class Boulder(pygame.sprite.Sprite):
    def __init__(self, pos, direction, groups):
        super().__init__(groups)
        self.image = pygame.transform.smoothscale(BOARD_SURFS['boulder'], (TILE_WIDTH, TILE_WIDTH))
        print(self.image)
        self.rect = self.image.get_frect(center = pos) 
        self.spawn_time = pygame.time.get_ticks()
        self.lifetime = 1000
        self.direction = direction
        self.speed = 1200
    
    def update(self, dt):
        if pygame.time.get_ticks() - self.spawn_time >= self.lifetime:
            self.kill()
        self.rect.center += self.direction * self.speed * dt
        pygame.display.get_surface().blit(self.image, self.rect)
