from settings import *
from piece import Piece
from support import get_all_moves
from pieces.legionary import Legionary
from pieces.emperor import Emperor

class Wizard(Piece):
    def __init(self, surf, color, squares):
        super().__init__(surf, color, squares)

    def possible_moves(self, coordinate):
        get_all_moves(coordinate, 1, self.squares)

    def attack_moves(self, start):
        DIRECTIONS = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
        for direction in DIRECTIONS:
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
                if square.piece and type(square.piece) != Emperor and type(square.piece) != Wizard and (row, col) not in surroundings:
                    square.is_swappable = True

    def attack(self, old_coord, attack_coord, round_num=0):
        old_square = self.squares[old_coord[0]][old_coord[1]]
        attack_square = self.squares[attack_coord[0]][attack_coord[1]]
        attack_square.piece = old_square.piece
        old_square.piece = None