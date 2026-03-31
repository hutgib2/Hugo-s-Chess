from settings import *
from pieces.piece import Piece

class Wizard(Piece):
    def __init__(self, surf, color, coord, squares, groups, is_stunned=False, stunned_at=0, is_reloading=False, attacked_at=0):
        super().__init__(surf, color, coord, squares, groups, is_stunned, stunned_at, is_reloading, attacked_at)
        self.move_directions = self.attack_directions = [(-1, -1), (-1, 1), (1, -1), (1, 1)]
        self.attack_range = (1,1)
        self.move_range = 1
        self.swap_squares = []

    def update_swap_moves(self):
        from pieces.emperor import Emperor
        from pieces.archer import Archer
        from pieces.legionary import Legionary
        from pieces.catapult import Catapult
        
        DIRECTIONS = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
        surroundings = []
        for direction in DIRECTIONS:
            row = self.coord[0] + direction[0]
            col = self.coord[1] + direction[1]
            if row < 0 or row > 7 or col < 0 or col > 7:
                continue
            surroundings.append((row, col))

        self.swap_squares = []
        for row in range(8):
            for col in range(8):
                square = self.squares[row][col]
                if not square.piece:
                    continue
                if square.coord in surroundings:
                    continue
                if type(square.piece) == Emperor or type(square.piece) == Wizard or type(square.piece) == Archer:
                    continue
                if type(square.piece) == Legionary:
                    if square.piece.color == "white" and self.coord[0] == 0:
                        continue
                    if square.piece.color == 'black' and self.coord[0] == 7:
                        continue
                self.swap_squares.append(square)

class Smoke(pygame.sprite.Sprite):
    def __init__(self, pos, groups):
        super().__init__(groups)
        self.frames = SMOKE_ANIMATION
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