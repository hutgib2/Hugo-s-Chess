from settings import *
from piece import Piece

class Legionary(Piece):
    def __init(self, surf, color, squares):
        super().__init__(surf, color, squares)

    def possible_moves(self, coordinate):
        row, col = coordinate # extracts row and col from the coordinate
        possible_moves = []
        if self.color == 'white' and row > 0:
            front_square = self.squares[row-1][col]
            if front_square.piece == None:
                possible_moves.append((row-1, col))
            elif front_square.piece.color != 'white' and type(front_square.piece) != Legionary:
                possible_moves.append((row-1, col)) # returns the position in front of the legionary
        elif row < 7:
            front_square = self.squares[row+1][col]
            if front_square.piece == None:
                possible_moves.append((row+1, col))
            elif self.squares[row+1][col].piece.color != 'black' and type(front_square.piece) != Legionary:
                possible_moves.append((row+1, col))
        return possible_moves
    