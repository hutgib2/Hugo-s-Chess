from settings import *
from piece import Piece
from support import get_all_moves
from pieces.legionary import Legionary

class Catapult(Piece):
    def __init(self, surf, color, squares):
        super().__init__(surf, color, squares)

    def update_possible_moves(self, coordinate):
        self.move_squares = get_all_moves(coordinate, 2, self.squares)

    def update_attack_moves(self, start):
        self.attack_squares = []
        if self.color == 'white':
            direction = (-1, 0)
        elif self.color == 'black':
            direction = (1, 0)

        i = 1
        while i <= 7:
            row = start[0] + direction[0] * i
            col = start[1] + direction[1] * i
            i += 1
            if row < 0 or row > 7 or col < 0 or col > 7:
                break
            
            square = self.squares[row][col]
            if not square.piece:
                self.attack_squares.append(square)
            elif square.piece.color == self.color:
                break
            elif type(square.piece) == Legionary:
                break
            else:
                self.attack_squares.append(square)

    def attack(self, _, __, round_num):
        killed_first = False
        print(self.attack_squares)
        for square in self.attack_squares:
            if not square.piece:
                continue
            if killed_first == False:
                square.piece = None
                killed_first = True
            else:
                square.piece.is_stunned = True
                square.piece.stunned_at = round_num
        self.can_attack = False
        self.attacked_at = round_num