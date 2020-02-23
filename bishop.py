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
    def get_legal_moves(self, squares, our_king):

        # Get the squares on the same diagonals as the selected bishop, and reset our list of legal_moves.
        self.get_diagonal_squares(self.curSquare, squares)  
        self.legal_moves = []

        # Now add all of these squares to legal_moves. Next then remove the illegal ones
        for square in self.curSquare.diagonals:
            if square not in self.legal_moves:
                self.legal_moves.append(square)

        # Now sort through those square ids by eliminating the illegal ones.
        for square in self.curSquare.diagonals:

            # Get the squares on the same diagonals as the square of interest.
            self.get_diagonal_squares(square, squares)

            # If the selected bishop doesn't reside on the diagonals of the square of interest. Then clearly we cannot move there.
            if self.curSquare not in square.diagonals:
                self.legal_moves.remove(square)

            # If the square of interest is occupied by one of our own pieces, then we cannot move there.
            if square.isOccupied and square.occupied_colour == self.colour and square in self.legal_moves:
                self.legal_moves.remove(square)

            # If the square of interest is on the same diagonal as the selected bishop, but there is no path from the bishop to that square.
            # I.e. There is a piece inbetween the bishop and that square, then we cannot move there.
            if self.is_blocked_diagonal(square, squares) and square in self.legal_moves:
                self.legal_moves.remove(square)

        # Remove our current square as a potential move.
        if self.curSquare in self.legal_moves:
            self.legal_moves.remove(self.curSquare)

        # Now that we have a working list of legal moves for the selected rook.  We need to deal with what happens if our king is in check.
        # Go through all squares legally available to the selected rook.  If our king is in check and the selected rook cannot either take 
        # the piece or block the check, then remove those squares from its legal moves.
        legal_move_copy = []
        for square in self.legal_moves:
            legal_move_copy.append(square)

        # If the selected bishop has legal moves that wouldn't block or take the checking piece, then we must remove those pieces from its legal moves.
        if our_king:
            for square in legal_move_copy:

                if square in self.legal_moves and our_king.in_check_along_diagonal:
                    print('Diag check')
                    if self.is_pinned(self, our_king):
                        print('we are pinned')
                        print('maybe here???')
                        for square in legal_move_copy:
                            if square not in our_king.curSquare.diagonals:
                                self.legal_moves.remove(square)

                        print([square.id for square in self.legal_moves])
                        break

                    # The case when the selected bishop isn't pinned to the king, but we are in check, so it's only available move is to block the king.
                    if our_king.in_check and files_dict[square.file] > files_dict[our_king.curSquare.file] > files_dict[our_king.checking_piece.curSquare.file] or files_dict[square.file] < files_dict[our_king.curSquare.file] < files_dict[our_king.checking_piece.curSquare.file] or files_dict[square.file] < files_dict[our_king.checking_piece.curSquare.file] < files_dict[our_king.curSquare.file] or files_dict[square.file] > files_dict[our_king.checking_piece.curSquare.file] > files_dict[our_king.curSquare.file]:
                        print('we are over here now')
                        self.legal_moves.remove(square)

                elif square in self.legal_moves and our_king.in_check_along_file:
                    print('File check')
                    if square.file != our_king.checking_piece.curSquare.file:
                        self.legal_moves.remove(square)

                elif square in self.legal_moves and our_king.in_check_along_rank:
                    print('Rank check')
                    if square.rank != our_king.checking_piece.curSquare.rank:
                        self.legal_moves.remove(square)
                

        return [square.id for square in self.legal_moves]