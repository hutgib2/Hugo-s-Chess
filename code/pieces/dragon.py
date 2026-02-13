from settings import *
from piece import Piece
from pieces.legionary import Legionary


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

    def kill_moves(self, start):
        kill_moves = []
        if self.color == 'white':
            directions = [(-1, -1), (-1, 0), (-1, 1)]
        elif self.color == 'black':
            directions = [(1, -1), (1, 0), (1, 1)]

        for direction in directions:
            row = start[0] + direction[0]
            col = start[1] + direction[1]

            if row < 0 or row > 7 or col < 0 or col > 7:
                continue

            if self.squares[row][col].piece != None:
                if self.squares[row][col].piece.color != self.color:
                    if type(self.squares[row][col].piece) == Legionary:
                        if self.color == 'white' and direction == (-1, 0):
                            continue
                        elif self.color == 'black' and direction == (1, 0):
                            continue
                            
                    kill_moves.append((row, col))
        return kill_moves

    def kill(self, old_coord, kill_coord):
        if self.color == 'white':
            directions = [(-1, -1), (-1, 0), (-1, 1)]
        elif self.color == 'black':
            directions = [(1, -1), (1, 0), (1, 1)]
        
        for direction in directions:
            row = old_coord[0] + direction[0]
            col = old_coord[1] + direction[1]

            if row < 0 or row > 7 or col < 0 or col > 7:
                continue
            
            if self.squares[row][col].piece != None:
                if self.squares[row][col].piece.color != self.color:
                    if type(self.squares[row][col].piece) == Legionary:
                        if self.color == 'white' and direction == (-1, 0):
                            continue
                        elif self.color == 'black' and direction == (1, 0):
                            continue
                    self.squares[row][col].piece = None