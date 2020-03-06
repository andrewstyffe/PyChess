import pygame as pg
from chess_pieces import *

class Bishop(ChessPiece):
    def __init__(self, square, colour):
        super(Bishop, self).__init__(self, square, colour)
        self.name = 'Bishop'
        
        # Assigns a picture to the bishop
        self.image = pg.image.load(f"./{self.colour}_{self.name.lower()}.png")
        self.image = pg.transform.scale(self.image, (50, 50))
        self.rect = self.image.get_rect(center = self.curSquare.center)


    # Returns a list of squares the a given bishop is able to move to.
    # After a bishop is selected, this method does the following.
    # 1. It gets the squares residing on the diagonal(s) in which the selected bishop resides.
    # 1. It adds all of the squares found in step 1 to self.legal_squares.
    # 3. It sorts through all of those squares to determine which ones represent illegal moves.
    def get_legal_moves(self, squares, pieces, selected_piece, our_king):

        # Get the squares on the same diagonals as the selected bishop, and reset our list of legal_moves.
        self.get_diagonal_squares(self.curSquare, squares)  
        self.legal_moves = []
        self.protected_squares = []

        # Now add all of these squares to legal_moves. Next then remove the illegal ones
        for square in self.curSquare.diagonals:
            if square not in self.legal_moves and square not in self.protected_squares:
                self.legal_moves.append(square)
                self.protected_squares.append(square)

        # Now sort through those square ids by eliminating the illegal ones.
        for square in self.curSquare.diagonals:

            # Get the squares on the same diagonals as the square of interest.
            self.get_diagonal_squares(square, squares)
            
            # If the square of interest is occupied by one of our own pieces, then we cannot move there.
            # Don't remove that square from the bishop's protected squares.
            if square.isOccupied and square.occupied_colour == self.colour and square in self.legal_moves:
                self.legal_moves.remove(square)

            # If the selected bishop doesn't reside on the diagonals of the square of interest. Then clearly we cannot move there.
            if self.curSquare not in square.diagonals:
                self.legal_moves.remove(square)
                self.protected_squares.remove(square)

            # If the square of interest is on the same diagonal as the selected bishop, but there is no path from the bishop to that square.
            # I.e. There is a piece inbetween the bishop and that square, then we cannot move there.
            if self.is_blocked_diagonal(square, squares) and square in self.legal_moves:
                self.legal_moves.remove(square)
                self.protected_squares.remove(square)

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