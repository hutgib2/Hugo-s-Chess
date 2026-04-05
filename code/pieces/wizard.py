from settings import *
from pieces.piece import Piece

class Wizard(Piece):
    def __init__(self, id, surf, color, coord, squares):
        super().__init__(surf, id, color, coord, squares)
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