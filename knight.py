import pygame as pg
from chess_pieces import *

class Knight(ChessPiece):
    def __init__(self, square, colour):
        super(Knight, self).__init__(self, square, colour)
        self.name = 'Knight'

        self.image = pg.image.load(f"./{self.colour}_{self.name.lower()}.png")
        self.image = pg.transform.scale(self.image, (50, 50))
        self.rect = self.image.get_rect(center = self.curSquare.center)


    def get_legal_moves(self, squares, pieces, selected_piece, our_king):

        possible_squares = []
        self.legal_moves = []
        self.protected_squares = []

        # Get all possible squares that lie in the 'L-shape' that a knight travels in.
        self.vertically_first(possible_squares, squares)
        self.horizontally_first(possible_squares, squares)
        
        # Append all of those squares to self.legal_moves.
        for square in possible_squares:
            self.legal_moves.append(square)
            self.protected_squares.append(square)

        # Remove those squares that correspond to illegal moves.
        # The only illegal move for a knight is if the square of interest is occupied by a piece from our own team. 
        # Do not remove those squares from the list of protected squares.
        for square in possible_squares:
            if square.occupied_colour == self.colour:
                self.legal_moves.remove(square)

        # Remove our current square as a potential move.
        if self.curSquare in self.legal_moves:
            self.legal_moves.remove(self.curSquare)

        # Remove all instances of self.curSquare
        while True:
            if self.curSquare in self.protected_squares:
                self.protected_squares.remove(self.curSquare)
            else:
                break
            
        # Now that we have a working list of legal moves for the selected rook.  We need to deal with what happens if our king is in check.
        # Go through all squares legally available to the selected rook.  If our king is in check and the selected rook cannot either take 
        # the piece or block the check, then remove those squares from its legal moves.
        self.legal_move_copy = []
        for square in self.legal_moves:
            self.legal_move_copy.append(square)

        # Check for pins
        self.check_for_pins(pieces, squares, our_king)

        self.check_remaining_squares(our_king, self.legal_move_copy)

        # If the selected bishop has legal moves that wouldn't block or take the checking piece, then we must remove those pieces from its legal moves.
        self.our_king_in_check(None, our_king)

        return [square.id for square in self.legal_moves]