from settings import *
from pieces.legionary import Piece
from pieces.legionary import Legionary

class Archer(Piece):
    def __init(self, surf, color, squares):
        super().__init__(surf, color, squares)

    def update_possible_moves(self, coordinate):
        self.move_squares = self.get_all_moves(coordinate, 1, self.squares)

    def attack(self, old_coord, attack_coord, round_num=0):
        self.squares[attack_coord[0]][attack_coord[1]].piece = None



    def update_attack_moves(self, start):
        self.attack_squares = []
        DIRECTIONS = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
        for direction in DIRECTIONS:
            i = 1
            while i <= 3:
                row = start[0] + direction[0] * i
                col = start[1] + direction[1] * i
                i += 1

                if row < 0 or row > 7 or col < 0 or col > 7:
                    break
                
                square = self.squares[row][col]
                if square.piece == None:
                    self.attack_squares.append(square)
                elif square.piece.color != self.color:
                    if type(square.piece) == Legionary:
                        if direction == (-1, 0) and self.color == 'white':
                            break
                        elif direction == (1, 0) and self.color == 'black':
                            break
                        elif self.has_adjacent_legionary(square, direction):
                            break

                    self.attack_squares.append(square)
                    break
