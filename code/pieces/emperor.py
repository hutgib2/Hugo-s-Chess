from settings import *
from piece import Piece
from support import get_all_moves

class Emperor(Piece):
    def __init(self, surf, color, squares):
        super().__init__(surf, color, squares)

    def possible_moves(self, coordinate):
        return get_all_moves(coordinate, 7,self.squares)