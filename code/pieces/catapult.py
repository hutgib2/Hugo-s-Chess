from settings import *
from pieces.legionary import Piece
from pieces.legionary import Legionary

class Catapult(Piece):
    def __init__(self, surf, color, squares):
        super().__init__(surf, color, squares)
        if self.color == 'white':
            self.attack_directions = [(-1, 0), (0, 1), (0, -1)]
        elif self.color == 'black':
            self.attack_directions = [(1, 0), (0, 1), (0, -1)]
        self.attack_range = 7
        self.move_directions = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
        self.move_range = 2


    def update_attack_moves(self, start):
        self.attack_squares = []
        for direction in self.attack_directions:
            i = 1
            while i <= self.attack_range:
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
                elif type(square.piece) == Legionary and direction == self.attack_directions[0]:
                    break
                else:
                    self.attack_squares.append(square)
            
    def attack(self, start, attack_square, round_num):
        drow = attack_square[0] - start[0]
        dcol = attack_square[1] - start[1]
        if drow != 0:
            drow = drow / abs(drow)
        if dcol != 0:
            dcol = dcol / abs(dcol)

        attack_direction = (int(drow), int(dcol))
        killed_first = False
        i = 1
        while i <= self.attack_range:
            row = start[0] + attack_direction[0] * i
            col = start[1] + attack_direction[1] * i
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
        self.can_attack = False
        self.attacked_at = round_num