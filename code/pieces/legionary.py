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
        elif self.color == 'black' and row < 7:
            front_square = self.squares[row+1][col]
            if front_square.piece == None:
                possible_moves.append((row+1, col))
        
        return possible_moves

    def kill_moves(self, coordinate):
        row, col = coordinate # extracts row and col from the coordinate
        kill_moves = []
        if self.color == 'white' and row > 0:
            front_square = self.squares[row-1][col]
            if front_square.piece and front_square.piece.color != 'white' and type(front_square.piece) != Legionary:
                kill_moves.append(front_square.coord)
        elif self.color == 'black' and row < 7:
            front_square = self.squares[row+1][col]
            if front_square.piece and front_square.piece.color != 'black' and type(front_square.piece) != Legionary:
                kill_moves.append(front_square.coord)
        
        return kill_moves

    def kill(self, old_coord, kill_coord):
        old_square = self.squares[old_coord[0]][old_coord[1]]
        kill_square = self.squares[kill_coord[0]][kill_coord[1]]
        kill_square.piece = old_square.piece
        old_square.piece = None

