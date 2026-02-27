from settings import *
from piece import Piece

class Legionary(Piece):
    def __init(self, surf, color, squares):
        super().__init__(surf, color, squares)
        self.attack_squares = []

    def update_possible_moves(self, coordinate):
        self.move_squares = []
        row, col = coordinate # extracts row and col from the coordinate

        if self.color == 'white' and row > 0:
            front_square = self.squares[row-1][col]
        elif self.color == 'black' and row < 7:
            front_square = self.squares[row+1][col]
        else:
            front_square = None
        
        if front_square and front_square.piece == None:
            self.move_squares.append(front_square)

    def update_attack_moves(self, coordinate):
        self.attack_squares = []
        row, col = coordinate # extracts row and col from the coordinate
        if self.color == 'white' and row > 0:
            front_square = self.squares[row-1][col]
        elif self.color == 'black' and row < 7:
            front_square = self.squares[row+1][col]
        else:
            front_square = None
        
        if front_square and front_square.piece and front_square.piece.color != self.color and type(front_square.piece) != Legionary:
            self.attack_squares.append(front_square)

    def attack(self, old_coord, attack_coord, round_num=0):
        old_square = self.squares[old_coord[0]][old_coord[1]]
        attack_square = self.squares[attack_coord[0]][attack_coord[1]]
        attack_square.piece = old_square.piece
        old_square.piece = None

