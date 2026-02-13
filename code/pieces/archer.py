from settings import *
from piece import Piece
from support import get_all_moves
from pieces.legionary import Legionary

class Archer(Piece):
    def __init(self, surf, color, squares):
        super().__init__(surf, color, squares)

    def possible_moves(self, coordinate):
        return get_all_moves(coordinate, 1, self.squares)

    def kill_moves(self, start):
        directions = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
        kill_moves = []
        for direction in directions:
            i = 1
            while i <= 3:
                row = start[0] + direction[0] * i
                col = start[1] + direction[1] * i
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
                            
                        kill_moves.append((row, col))
                    break
        
        return kill_moves

    def kill(self, old_coord, kill_coord):
        self.squares[kill_coord[0]][kill_coord[1]].piece = None
