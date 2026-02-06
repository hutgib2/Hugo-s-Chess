from settings import *
from piece import Piece

class Dragon(Piece):
    def __init(self, surf, color, squares):
        super().__init__(surf, color, squares)

    def possible_moves(self, coordinate):
        row, col = coordinate # extracts row and col from the coordinate
        possible_moves = []
        for new_row in (row-2, row, row+2):
            for new_col in (col-2, col, col+2):
                if (new_row,new_col) == (row,col):
                    continue
                if new_row < 0 or new_row > 7 or new_col < 0 or new_col > 7:
                    continue
                if self.squares[new_row][new_col].piece != None:
                    continue
                possible_moves.append((new_row, new_col))
        return possible_moves

    