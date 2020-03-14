import pygame as pg
from chess_pieces import *

# Describes the various attributes of a rook and enforces the rules of a rook on the object
# TODO: implement castling
class Rook(ChessPiece):
    def __init__(self, square, colour):
        super(Rook, self).__init__(self, square, colour)
        self.name = 'Rook'

        self.first_move = True

        # Assigns a picture to the rook
        self.image = pg.image.load(f"./{self.colour}_{self.name.lower()}.png")

        self.image = pg.transform.scale(self.image, (50, 50))
        self.rect = self.image.get_rect(center = self.curSquare.center)
        
    # Returns a list of squares the a given rook is able to move to.
    def get_legal_moves(self, squares, pieces, selected_piece, our_king):

        # Reset self.legal_moves after every move.
        self.legal_moves = []
        self.protected_squares = []

        # Get the squares in the same file, and rank as our selected piece
        file_squares = [square for square in squares if square.file == self.curSquare.file]
        rank_squares = [square for square in squares if square.rank == self.curSquare.rank]

        # Start by adding every square to legal_moves, then remove those squares that are illegal
        for square in file_squares + rank_squares:
            if square not in self.legal_moves:
                self.legal_moves.append(square)
                self.protected_squares.append(square)

        # Now sort through those squares by eliminating the illegal ones.
        for square in file_squares + rank_squares:

            # If the square of interest is occupied by one of our own pieces, then we cannot move there.
            # However, while we cannot move there, that square is currently protected by the rook, which is important.
            if square.occupied_colour == self.colour and square in self.legal_moves:
                self.legal_moves.remove(square)

            # If the square of interest is not in the same file and it is not in the same rank as the square of interest, then we cannot move there.
            if square.file != self.curSquare.file and square.rank != self.curSquare.rank and square in self.legal_moves:
                self.legal_moves.remove(square)
                self.protected_squares.remove(square)

            # If the square of interest is on the same file as the selected rook, but there is no path from the rook to that square.
            # I.e. There is a piece inbetween the rook and that square, then we cannot move there.
            if self.is_blocked_file(square, file_squares) and square in self.legal_moves:
                self.legal_moves.remove(square)
                self.protected_squares.remove(square)

            # If the square of interest is on the same rank as the selected rook, but there is no path from the rook to that square.
            # I.e. There is a piece inbetween the rook and that square, then we cannot move there.
            if self.is_blocked_rank(square, rank_squares) and square in self.legal_moves:
                self.legal_moves.remove(square)
                self.protected_squares.remove(square)

        # Lastly, if the current square of the selected rook is in legal_moves, then we cannot move there.
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