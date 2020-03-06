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
        self.in_check_from_knight = False
        self.checking_piece = None
        self.list_of_checking_pieces = []
        self.pinned_pieces = []

        self.image = pg.image.load(f"./{self.colour}_{self.name.lower()}.png")
        self.image = pg.transform.scale(self.image, (50, 50))
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

        rooks = [piece for piece in pieces if piece.name == 'Rook']
        # Selects from these squares the 8 squares immediately surrounding the selected king.
        # We further remove any illegal squares below.
        for square in self.curSquare.diagonals + file_squares + rank_squares:

            # Implement castling.  If its the selected king's first move and its the 
            for rook in rooks:
                if self.first_move and self.colour == 'white' and square.id == 'G1' or square.id == 'C1' and not self.is_blocked_rank(square, rank_squares):
                    if rook.colour == self.colour and rook.first_move and not self.castle_through_check(square, squares, pieces, selected_piece, our_king):
                        if not self.in_check:
                            if square.id == 'G1' and rook.curSquare.id == 'H1' and not self.castle_through_check(square, squares, pieces, selected_piece, our_king):                            
                                possible_moves.append(square)
                                self.legal_moves.append(square)
                                break
                            elif square.id == 'C1' and rook.curSquare.id == 'A1' and not self.get_square('B1', squares).isOccupied and not self.castle_through_check(square, squares, pieces, selected_piece, our_king):
                                possible_moves.append(square)
                                self.legal_moves.append(square)
                                break

                elif self.first_move and self.colour == 'black' and square.id == 'G8' or square.id == 'C8' and not self.is_blocked_rank(square, rank_squares):
                    if rook.colour == self.colour and rook.first_move and not self.castle_through_check(square, squares, pieces, selected_piece, our_king):
                        if not self.in_check:
                            if square.id == 'G8' and rook.curSquare.id == 'H8' and not self.castle_through_check(square, squares, pieces, selected_piece, our_king):
                                possible_moves.append(square)
                                self.legal_moves.append(square)
                                break
                            elif square.id == 'C8' and rook.curSquare.id == 'A8' and not self.get_square('B8', squares).isOccupied and not self.castle_through_check(square, squares, pieces, selected_piece, our_king):
                                possible_moves.append(square)
                                self.legal_moves.append(square)
                                break
            
            # If the square of interest is one file away in either direction or is on the same file as the selected king
            # and it is one rank away in either direction or is on the same rank as the selected king
            # and is not the selected king's current square, then add that square to the list of possible moves.
            if files_dict[square.file] == files_dict[self.curSquare.file] + 1 or files_dict[square.file] == files_dict[self.curSquare.file] - 1 or square.file == self.curSquare.file:
                if square.rank == self.curSquare.rank + 1 or square.rank == self.curSquare.rank - 1 or square.rank == self.curSquare.rank:
                    if square != self.curSquare:
                        possible_moves.append(square)
                        self.legal_moves.append(square)
                        self.protected_squares.append(square)


        # Now sort through those square ids by eliminating the illegal ones.
        for square in possible_moves:

            # If the square of interest is occupied by one of our own pieces, then we cannot move there.
            if square.occupied_colour == self.colour and square in self.legal_moves:
                self.legal_moves.remove(square)

            # Remove any squares that would result in us 'moving into check'.
            for piece in pieces:
                if piece.colour != self.colour:
                    
                    # Need a separate case for pawns since they capture pieces in a different way than they move.
                    if piece.name == 'Pawn':
                        if square in piece.taking_squares and square in self.legal_moves:
                            self.legal_moves.remove(square)
                    else:
                        
                        # Additionally, however, since piece.legal_moves does not include the piece of interest's current square.
                        # We need to check if the king is able to capture the piece of interest or not.
                        if square in self.legal_moves:

                            if piece.name == 'Pawn':
                                if square in piece.taking_squares or square == piece.curSquare or square in piece.protected_squares:
                                    if square.occupied_colour and square.occupied_colour != self.colour:
                                        for cur_piece in [piece for piece in pieces if piece.colour != self.colour]:
                                            if cur_piece.name == 'Pawn':
                                                if square in cur_piece.taking_squares and square in self.legal_moves:
                                                    self.legal_moves.remove(square)
                                                    break
                                            else:
                                                if square in cur_piece.legal_moves and square in self.legal_moves:
                                                    self.legal_moves.remove(square)
                                                    break
                                    else:
                                        self.legal_moves.remove(square)
                            
                            else:
                                if square in piece.legal_moves or square == piece.curSquare or square in piece.protected_squares:
                                    if square.occupied_colour and square.occupied_colour != self.colour:
                                        for cur_piece in [piece for piece in pieces if piece.colour != self.colour]:
                                            if cur_piece.name == 'Pawn':
                                                if square in cur_piece.taking_squares and square in self.legal_moves:
                                                    self.legal_moves.remove(square)
                                                    break
                                            else:
                                                if square in cur_piece.protected_squares and square in self.legal_moves:
                                                    self.legal_moves.remove(square)
                                                    break
                                    else:
                                        self.legal_moves.remove(square)

        # Now, remove all squares that would result in us 'moving-into' check.
        # Or, if we are already in check, remove any squares that would result in us still being in check.
        # I.e. If we are in check along a diagonal, file or rank, we cannot simply move to the next square on that
        # diagonal/file/rank.
        if self.in_check:
            
            # For each of the squares around the king, we need to check if that square represents a legal move for any of the opponent's pieces.
            for square in possible_moves:
                for piece in pieces:
                    if piece.colour != self.colour and square in self.legal_moves:
                        
                        # If we are in check along a diaogonal or the square of interest is in the current opponent's piece's legal moves.
                        # Then if the square of interest is on the same diagonal as the checking piece, we must remove that square - unless
                        # the square is the checking piece's current square and it is not defended by any of it's own pieces.
                        if piece.name != 'Pawn':
                            if self.in_check_along_diagonal or square in piece.legal_moves:
                                if square in self.checking_piece.curSquare.diagonals:
                                    if square != self.checking_piece.curSquare:
                                        print(f'Removing {square.id} from king"s legal moves')
                                        self.legal_moves.remove(square)
                                    
                                    # Square of interest is the checking piece's current square.  Check if that piece is defended at all.
                                    # If it is, remove the square of interest from the selected king's legal moves.
                                    else:
                                        for cur_piece in [piece for piece in pieces if piece.colour != self.colour]:
                                            if piece.curSquare in cur_piece.legal_moves:
                                                print(f'Checking piece is defended by {cur_piece}.  Cannot capture the checking piece.')
                                                self.legal_moves.remove(square)
                        
                        else:
                            if square in piece.taking_squares:
                                print(f'{piece.name} {piece.curSquare.id}')
                                if square in self.checking_piece.curSquare.diagonals:
                                    if square != self.checking_piece.curSquare:
                                        print(f'Removing {square.id} from king"s legal moves')
                                        self.legal_moves.remove(square)
                                    
                                    # Square of interest is the checking piece's current square.  Check if that piece is defended at all.
                                    # If it is, remove the square of interest from the selected king's legal moves.
                                    else:
                                        for cur_piece in [piece for piece in pieces if piece.colour != self.colour]:
                                            if piece.curSquare in cur_piece.legal_moves:
                                                print(f'Checking piece is defended by {cur_piece}.  Cannot capture the checking piece.')
                                                self.legal_moves.remove(square)


            if len(self.legal_moves) == 0:
                print('Our king has no legal moves!')
            else:
                print(f'Our kings available moves are {[square.id for square in self.legal_moves]}')
            #print([square.id for square in self.legal_moves])
                # If we are in check along a diagonal, then remove those squares that lie on the same diagonal as the 
                # piece currently checking the king.
                # if self.in_check_along_diagonal:
                #     for square in possible_moves:
                #         if square in self.legal_moves:
                #             if square.id != self.checking_piece.curSquare.id: 
                #                 if square in self.checking_piece.curSquare.pos_diagonal or square in self.checking_piece.curSquare.neg_diagonal:
                #                     print(f'Removing {square.id}')
                #                     self.legal_moves.remove(square)
                
                # # If we are in check along a file, then remove those squares that lie on the same file as the 
                # # piece currently checking the king.
                # elif self.in_check_along_file:
                #     for square in possible_moves:
                #         if square in self.legal_moves:
                #             if square.id != self.checking_piece.curSquare.id: 
                #                 if square in [square for square in squares if square.file == self.checking_piece.curSquare.file]:
                #                     print(f'Removing {square.id}')
                #                     self.legal_moves.remove(square)

                # # If we are in check along a rank, then remove those squares that lie on the same rank as the 
                # # piece currently checking the king.
                # else:
                #     for square in possible_moves:
                #         if square in self.legal_moves:
                #             if square.id != self.checking_piece.curSquare.id: 
                #                 if square in [square for square in squares if square.rank == self.checking_piece.curSquare.rank]:
                #                     print(f'Removing {square.id}')
                #                     self.legal_moves.remove(square)



        # Lastly, if the selected king's current square is in self.legal_moves, remove it.
        if self.curSquare in self.legal_moves:
            self.legal_moves.remove(self.curSquare)

        return [square.id for square in self.legal_moves] 