from settings import *
from piece import Piece
from support import get_all_moves
from pieces.legionary import Legionary

class Wizard(Piece):
    def __init(self, surf, color, squares):
        super().__init__(surf, color, squares)

    def possible_moves(self, coordinate):
        return get_all_moves(coordinate, 1, self.squares)

    def attack_moves(self, start):
        directions = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
        for direction in directions:
            row = start[0] + direction[0]
            col = start[1] + direction[1]

            if row < 0 or row > 7 or col < 0 or col > 7:
                continue
            
            square = self.squares[row][col]
            if square.piece != None:
                if square.piece.color != self.color:
                    if type(square.piece) == Legionary:
                        if self.color == 'white' and direction == (-1, 0):
                            continue
                        elif self.color == 'black' and direction == (1, 0):
                            continue
                        
                    square.is_attack_move = True

    def attack(self, old_coord, attack_coord):
        old_square = self.squares[old_coord[0]][old_coord[1]]
        attack_square = self.squares[attack_coord[0]][attack_coord[1]]
        attack_square.piece = old_square.piece
        old_square.piece = None