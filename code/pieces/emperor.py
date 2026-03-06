from settings import *
from pieces.legionary import Piece
from pieces.legionary import Legionary

class Emperor(Piece):
    def __init__(self, surf, color, squares):
        super().__init__(surf, color, squares)
        in_check = False
        self.attack_directions = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
        self.attack_range = 1

    def get_all_moves(self, start, range, squares):
        move_squares = []
        DIRECTIONS = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
        for direction in DIRECTIONS:
            i = 1
            while i <= range:
                row = start[0] + direction[0] * i
                col = start[1] + direction[1] * i
                i += 1

                if row < 0 or row > 7 or col < 0 or col > 7:
                    break
                
                if squares[row][col].piece != None:
                    break
                
                move_squares.append(squares[row][col])
        return move_squares

    def update_possible_moves(self, coordinate):
        enemy_attack_squares = []
        self.move_squares = []
        for row in range(8):
            for col in range(8):
                square = self.squares[row][col]
                if not square.piece or square.piece.color == self.color:
                    continue
                enemy_attack_squares += square.piece.attack_squares
        
        move_squares = self.get_all_moves(coordinate, 1, self.squares)
        for move in move_squares:
            if move not in enemy_attack_squares:
                self.move_squares.append(move)