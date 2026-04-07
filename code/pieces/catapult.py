from settings import *
from pieces.piece import Piece
from support import get_direction_between

class Catapult(Piece):
    def __init__(self, id, surf, color, coord, squares):
        super().__init__(id, surf, color, coord, squares)
        if self.color == 'white':
            self.attack_directions = [(-1, 0), (0, 1), (0, -1)]
        elif self.color == 'black':
            self.attack_directions = [(1, 0), (0, 1), (0, -1)]
        self.attack_range = (1, 7)
        self.move_directions = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
        self.move_range = 2

    def update_attack_moves(self):
        from pieces.legionary import Legionary
        from pieces.emperor import Emperor

        self.attack_squares = []
        if self.is_reloading:
            return
        for direction in self.attack_directions:
            i = self.attack_range[0]
            while i <= self.attack_range[1]:
                row = self.coord[0] + direction[0] * i
                col = self.coord[1] + direction[1] * i
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
                    break  
            
    def attack(self, attack_coord, round_num):
        pass
    #     from pieces.legionary import Legionary

    #     attack_direction = get_direction_between(self.coord, attack_coord)
    #     killed_first = False
    #     i = self.attack_range[0]
    #     while i <= self.attack_range[1]:
    #         row = self.coord[0] + attack_direction[0] * i
    #         col = self.coord[1] + attack_direction[1] * i
    #         i += 1
    #         if row < 0 or row > 7 or col < 0 or col > 7:
    #             break
    #         square = self.squares[row][col]
    #         if not square.piece:
    #             continue
    #         if square.piece.color == self.color:
    #             break
    #         elif type(square.piece) == Legionary and attack_direction == self.attack_directions[0]:
    #             break
    #         if killed_first == False:
    #             square.piece = None
    #             killed_first = True
    #         else:
    #             square.piece.is_stunned = True
    #             square.piece.stunned_at = round_num