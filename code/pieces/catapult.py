from settings import *
from piece import Piece
from support import get_all_moves
from pieces.legionary import Legionary

class Catapult(Piece):
    def __init(self, surf, color, squares):
        super().__init__(surf, color, squares)

    def possible_moves(self, coordinate):
        return get_all_moves(coordinate, 2, self.squares)

    def attack_moves(self, start):
        if self.color == 'white':
            direction = (-1, 0)
        elif self.color == 'black':
            direction = (1, 0)

        i = 1
        while i < 7:
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
                            
                    square.is_attack_move = True

    def attack(self, old_coord, attack_coord, round_num):
        if self.color == 'white':
            direction = (-1, 0)
        elif self.color == 'black':
            direction = (1, 0)

        i = 1
        while i < 7:
            row = old_coord[0] + direction[0] * i
            col = old_coord[1] + direction[1] * i
            i += 1
            if row < 0 or row > 7 or col < 0 or col > 7:
                break
            
            if self.squares[row][col].piece != None:
                if self.squares[row][col].piece.color != self.color:
                    if type(self.squares[row][col].piece) == Legionary:
                        if self.color == 'white' and direction == (-1, 0):
                            break
                        elif self.color == 'black' and direction == (1, 0):
                            break
                    self.squares[row][col].piece.is_stunned = True
                    self.squares[row][col].piece.stunned_at = round_num
        self.can_attack = False
        self.attacked_at = round_num