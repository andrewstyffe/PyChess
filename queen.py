import pygame as pg
from chess_pieces import *


class Queen(ChessPiece):
    def __init__(self, square, colour):
        super(Queen, self).__init__(self, square, colour)
        self.name = 'Queen'

        self.image = pg.image.load(f"./{self.colour}_{self.name.lower()}.png")
        self.image = pg.transform.scale(self.image, (100, 100))
        self.rect = self.image.get_rect(center = self.curSquare.center)

    def get_legal_moves(self, squares, pieces, selected_piece, our_king):

        self.legal_moves = []
        possible_moves = []
        self.protected_squares = []

        # Get the squares on the same diagonals as the selected queen.
        self.get_diagonal_squares(self.curSquare, squares)  

        # Get the squares on the same file and rank as the selected queen.
        file_squares = [square for square in squares if square.file == self.curSquare.file]
        rank_squares = [square for square in squares if square.rank == self.curSquare.rank]

        # Now add all of these squares to legal_moves. Then remove the illegal ones.
        for square in self.curSquare.diagonals + file_squares + rank_squares:
            possible_moves.append(square)
            self.legal_moves.append(square)
            self.protected_squares.append(square)

        # Now sort through those square ids by eliminating the illegal ones.
        for square in possible_moves:

            # If the square of interest is occupied by one of our own pieces, then we cannot move there.
            # That square is protected by the knight though, so don't remove it from the knight's list of protected squares.
            if square.occupied_colour == self.colour and square in self.legal_moves:
                self.legal_moves.remove(square)

            # Check the squares on the selected queen's diagonals, and remove any illegal ones.
            if square in self.curSquare.diagonals:
                self.check_diagonals(square, squares)

            # Check the squares on the selected queen's files and ranks, and remove any illegal ones.
            if square in file_squares + rank_squares:
                self.check_files_and_ranks(square, file_squares, rank_squares)
            
        # Lastly, if the selected queen's current square is in self.legal_moves, remove it.
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