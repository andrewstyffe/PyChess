import pygame as pg
from chess_pieces import *

class King(ChessPiece):
    def __init__(self, square, colour):
        super(King, self).__init__(self, square, colour)
        self.name = 'King'

        self.first_move = True
        self.in_check = False
        self.in_check_along_diagonal = False
        self.in_check_along_file = False
        self.in_check_along_rank = False
        self.checking_piece = None

        self.image = pg.image.load(f"./{self.colour}_{self.name.lower()}.png")
        self.image = pg.transform.scale(self.image, (50, 50))
        self.rect = self.image.get_rect(center = self.curSquare.center)


    def get_legal_moves(self, squares, pieces, our_king):

        self.legal_moves = []
        possible_moves = []

        # Get the squares on the same diagonals as the selected queen.
        self.get_diagonal_squares(self.curSquare, squares)  

        # Get the squares on the same file and rank as the selected queen.
        file_squares = [square for square in squares if square.file == self.curSquare.file]
        rank_squares = [square for square in squares if square.rank == self.curSquare.rank]

        rooks = [piece for piece in pieces if piece.name == 'Rook']
        # Selects from these squares the 8 squares immediately surrounding the selected king.
        # We further remove any illegal squares below.
        for square in self.curSquare.diagonals + file_squares + rank_squares:

            # Implement castling.  If its the selected king's first move and its the 
            for rook in rooks:
                if self.first_move and self.colour == 'white' and not self.is_blocked_rank(square, rank_squares) and square.id == 'G1' or square.id == 'C1' and not self.is_blocked_rank(square, rank_squares):
                    if rook.colour == self.colour and rook.first_move and not self.castle_through_check(square, squares, pieces, our_king):
                        if square.id == 'G1' and rook.curSquare.id == 'H1' and not self.castle_through_check(square, squares, pieces, our_king):
                            print('asuhhhh')
                            possible_moves.append(square)
                            self.legal_moves.append(square)
                        elif square.id == 'C1' and rook.curSquare.id == 'A1' and not self.castle_through_check(square, squares, pieces, our_king):
                            possible_moves.append(square)
                            self.legal_moves.append(square)

                elif self.first_move and self.colour == 'black' and not self.is_blocked_rank(square, rank_squares) and square.id == 'G8' or square.id == 'C8':
                    if rook.colour == self.colour and rook.first_move and not self.castle_through_check(square, squares, pieces, our_king):
                        if square.id == 'G8' and rook.curSquare.id == 'H8' and not self.castle_through_check(square, squares, pieces, our_king):
                            possible_moves.append(square)
                            self.legal_moves.append(square)
                        elif square.id == 'C8' and rook.curSquare.id == 'A8' and not self.castle_through_check(square, squares, pieces, our_king):
                            possible_moves.append(square)
                            self.legal_moves.append(square)
            
            # If the square of interest is one file away in either direction or is on the same file as the selected king
            # and it is one rank away in either direction or is on the same rank as the selected king
            # and is not the selected king's current square, then add that square to the list of possible moves.
            if files_dict[square.file] == files_dict[self.curSquare.file] + 1 or files_dict[square.file] == files_dict[self.curSquare.file] - 1 or square.file == self.curSquare.file:
                if square.rank == self.curSquare.rank + 1 or square.rank == self.curSquare.rank - 1 or square.rank == self.curSquare.rank:
                    if square != self.curSquare:
                        possible_moves.append(square)
                        self.legal_moves.append(square)


        # Now sort through those square ids by eliminating the illegal ones.
        for square in possible_moves:

            # If the square of interest is occupied by one of our own pieces, then we cannot move there.
            if square.occupied_colour == self.colour and square in self.legal_moves:
                self.legal_moves.remove(square)

            # Remove any squares that would result in us 'moving into check'.
            for piece in pieces:
                if piece.colour != self.colour:
                    if square in piece.legal_moves and square in self.legal_moves:
                        print(f'Opponents {piece.name} is blocking you from going to {square.id}')
                        self.legal_moves.remove(square)

        # Lastly, if the selected king's current square is in self.legal_moves, remove it.
        if self.curSquare in self.legal_moves:
            self.legal_moves.remove(self.curSquare)

        return [square.id for square in self.legal_moves] 