from settings import *
from pieces.legionary import Piece
from pieces.legionary import Legionary
from pieces.emperor import Emperor
from pieces.archer import Archer

class Wizard(Piece):
    def __init__(self, surf, color, squares):
        super().__init__(surf, color, squares)
        self.attack_directions = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
        self.attack_range = (1,1)
        self.move_directions = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
        self.move_range = 1

    def swap_moves(self, coordinate):
        DIRECTIONS = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
        surroundings = []
        for direction in DIRECTIONS:
            row = coordinate[0] + direction[0]
            col = coordinate[1] + direction[1]
            if row < 0 or row > 7 or col < 0 or col > 7:
                continue
            surroundings.append((row, col))

        for row in range(8):
            for col in range(8):
                square = self.squares[row][col]
                if square.piece and type(square.piece) != Emperor and type(square.piece) != Wizard and type(square.piece) != Archer and (row, col) not in surroundings:
                    square.is_swappable = True