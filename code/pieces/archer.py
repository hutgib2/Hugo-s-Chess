from settings import *
from piece import Piece
from support import get_all_moves
from pieces.legionary import Legionary

class Archer(Piece):
    def __init(self, surf, color, squares):
        super().__init__(surf, color, squares)

    def update_possible_moves(self, coordinate):
        self.move_squares = get_all_moves(coordinate, 1, self.squares)

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
                        if self.color == 'white':
                            if direction == (-1, 0):
                                break
                            elif direction == (-1, -1):
                                row = square.coord[0]
                                col = square.coord[1] + 1
                                if col <= 7:
                                    defending_square = self.squares[row][col]
                                    if defending_square.piece and type(defending_square.piece) == Legionary and defending_square.piece.color != self.color:
                                        break

                            elif direction == (-1, 1):
                                row = square.coord[0]
                                col = square.coord[1] - 1
                                if col >= 0:
                                    defending_square = self.squares[row][col]
                                    if defending_square.piece and type(defending_square.piece) == Legionary and defending_square.piece.color != self.color:
                                        break

                        elif self.color == 'black':
                            if direction == (1, 0):
                                break
                                
                            elif direction == (1, -1):
                                row = square.coord[0]
                                col = square.coord[1] + 1
                                if col <= 7:
                                    defending_square = self.squares[row][col]
                                    if defending_square.piece and type(defending_square.piece) == Legionary and defending_square.piece.color != self.color:
                                        break
                            elif direction == (1, 1):
                                row = square.coord[0]
                                col = square.coord[1] - 1
                                if col >= 0:
                                    defending_square = self.squares[row][col]
                                    if defending_square.piece and type(defending_square.piece) == Legionary and defending_square.piece.color != self.color:
                                        break
                        
                    self.attack_squares.append(square)
                    break

    def attack(self, old_coord, attack_coord, round_num=0):
        self.squares[attack_coord[0]][attack_coord[1]].piece = None
