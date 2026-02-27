from settings import *
from piece import Piece
from support import get_all_moves
from pieces.legionary import Legionary

class Emperor(Piece):
    def __init(self, surf, color, squares):
        super().__init__(surf, color, squares)

    def update_possible_moves(self, coordinate):
        enemy_attack_squares = []
        self.move_squares = []
        for row in range(8):
            for col in range(8):
                square = self.squares[row][col]
                if not square.piece or square.piece.color == self.color:
                    continue
                enemy_attack_squares += square.piece.attack_squares
        move_squares = get_all_moves(coordinate, 1, self.squares)
        for move in move_squares:
            if move not in enemy_attack_squares:
                self.move_squares.append(move)

    def update_attack_moves(self, start):
        self.attack_squares = []
        DIRECTIONS = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
        for direction in DIRECTIONS:
            i = 1
            while i <= 1:
                row = start[0] + direction[0] * i
                col = start[1] + direction[1] * i
                i += 1

                if row < 0 or row > 7 or col < 0 or col > 7:
                    break
                square = self.squares[row][col]
                if square.piece != None:
                    if square.piece.color != self.color:
                        if type(square.piece) == Legionary:
                            if self.color == 'white' and direction == (-1, 0):
                                break
                            elif self.color == 'black' and direction == (1, 0):
                                break
                            
                        self.attack_squares.append(square)
                    break

    def attack(self, old_coord, attack_coord, round_num=0):
        old_square = self.squares[old_coord[0]][old_coord[1]]
        attack_square = self.squares[attack_coord[0]][attack_coord[1]]
        attack_square.piece = old_square.piece
        old_square.piece = None