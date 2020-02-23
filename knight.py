import pygame as pg
from chess_pieces import *

class Knight(ChessPiece):
    def __init__(self, square, colour):
        super(Knight, self).__init__(self, square, colour)
        self.name = 'Knight'

        self.image = pg.image.load(f"./{self.colour}_{self.name.lower()}.png")
        self.image = pg.transform.scale(self.image, (50, 50))
        self.rect = self.image.get_rect(center = self.curSquare.center)


    def get_legal_moves(self, squares, our_king):
        possible_squares = []
        self.legal_moves = []

        # Get all possible squares that lie in the 'L-shape' that a knight travels in.
        self.vertically_first(possible_squares, squares)
        self.horizontally_first(possible_squares, squares)
        
        # Append all of those squares to self.legal_moves.
        for square in possible_squares:
            self.legal_moves.append(square)

        # Remove those squares that correspond to illegal moves.
        # The only illegal move for a knight is if the square of interest is occupied by a piece from our own team. 
        for square in possible_squares:
            if square.occupied_colour == self.colour:
                self.legal_moves.remove(square)

        # Now that we have a working list of legal moves for the selected rook.  We need to deal with what happens if our king is in check.
        # Go through all squares legally available to the selected rook.  If our king is in check and the selected rook cannot either take 
        # the piece or block the check, then remove those squares from its legal moves.
        legal_move_copy = []
        for square in self.legal_moves:
            legal_move_copy.append(square)

        # If the selected bishop has legal moves that wouldn't block or take the checking piece, then we must remove those pieces from its legal moves.
        if our_king:
            for square in legal_move_copy:
                
                # In check along a diagonal.
                if square in self.legal_moves and our_king.in_check_along_diagonal:
                    print('Diag check')

                    # If the selected knight is pinned to the king, then we can't move it at all.
                    if self.is_pinned(self, our_king):
                        print('we are pinned')
                        print('hjsdfasdfj s jsdjd ')
                        self.legal_moves.clear()
                        break

                    # The case when the selected bishop isn't pinned to the king, but we are in check, so it's only available move is to block the king.
                    #our_king.checking_piece.curSquare.rank <= square.rank <= our_king.curSquare.rank or our_king.curSquare.rank < square.rank < our_king.checking_piece.rank
                    if our_king.in_check and files_dict[square.file] > files_dict[our_king.curSquare.file] > files_dict[our_king.checking_piece.curSquare.file] or files_dict[square.file] < files_dict[our_king.curSquare.file] < files_dict[our_king.checking_piece.curSquare.file] or files_dict[square.file] < files_dict[our_king.checking_piece.curSquare.file] < files_dict[our_king.curSquare.file] or files_dict[square.file] > files_dict[our_king.checking_piece.curSquare.file] > files_dict[our_king.curSquare.file]:
                        self.legal_moves.remove(square)

        return [square.id for square in self.legal_moves]