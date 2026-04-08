from settings import *
from pieces.piece import Piece

class Wizard(Piece):
    def __init__(self, id, color, coord, squares):
        super().__init__(id, "wizard", color, coord, squares)
        self.type = "wizard"
        self.move_directions = self.attack_directions = [(-1, -1), (-1, 1), (1, -1), (1, 1)]
        self.attack_range = (1,2)
        self.move_range = 2
        self.swap_squares = []

    def update_swap_moves(self):
        from pieces.legionary import Legionary

        self.swap_squares = []
        for row in range(8):
            for col in range(8):
                square = self.squares[row][col]
                if not square.piece:
                    continue
                if square in self.attack_squares:
                    continue
                if square.piece.type != 'legionary':
                    continue
                if square.piece.color == "white" and self.coord[0] == 0:
                    continue
                if square.piece.color == 'black' and self.coord[0] == 7:
                    continue
                self.swap_squares.append(square)