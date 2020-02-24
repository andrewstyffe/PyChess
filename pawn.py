import pygame as pg
from chess_pieces import *

# Describes the various attributes of a pawn and enforces the rules of a pawn on the object
# TODO: enforce en-passant
# TODO: Fix all this code... Not great.
class Pawn(ChessPiece):
    def __init__(self, square, colour):
        super(Pawn, self).__init__(self, square, colour)
        self.name = 'Pawn'
        
        # Just for pawns. Initialize to false, so that on startup, it isn't set to false.
        self.first_move = False

        # Assign a picture to the pawn
        self.image = pg.image.load(f"./{self.colour}_{self.name.lower()}.png")
        self.image = pg.transform.scale(self.image, (50, 50))
        self.rect = self.image.get_rect(center = self.curSquare.center)


    # Returns the index that a given square's file has in the list of files
    def get_file_index(self, curSquare):
        index = 0
        for file_index, _file in enumerate(files):
            if _file == curSquare.file:
                index = file_index
                break
        return index

    # Returns True or False corresponding to the square directly above or below curSquare (depending on perspective) being occupied by a piece.
    def get_next_square(self, curSquare, squares):
        for square in squares:
            if self.colour == 'white':
                if square.id == f'{curSquare.file}{self.curSquare.rank + 1}':
                    return square.isOccupied
            if square.id == f'{curSquare.file}{self.curSquare.rank - 1}':
                return square.isOccupied 

    # Deals with taking opponent's pieces, since pawns take differently from how they normally move.
    def take_opponent_piece(self, curSquare, squares):
        index = self.get_file_index(curSquare)

        for square in squares:

            # For white pawns.
            if self.colour == 'white':

                # For the 'A' file, if the square diagonally-up from curSquare is occupied by an opponent's piece, then add that square to legal_moves.
                if curSquare.file == 'A':
                    if square.id == f'{files[index + 1]}{self.curSquare.rank + 1}' and square.isOccupied and square not in self.legal_moves:
                        if square.occupied_colour != self.colour:
                            self.legal_moves.append(square)

                # For the 'H' file, if the square diagonally-up from curSquare is occupied by an opponent's piece, then add that square to legal_moves.
                elif curSquare.file == 'H':
                    if square.id == f'{files[index - 1]}{self.curSquare.rank + 1}' and square.isOccupied and square not in self.legal_moves:
                        if square.occupied_colour != self.colour:
                            self.legal_moves.append(square)
                
                # For any other file, if the squares diagonally-up from curSquare are occupied by an opponent's piece, then add them square to legal_moves.
                else:
                    if square.id == f'{files[index + 1]}{self.curSquare.rank + 1}' or square.id == f'{files[index - 1]}{self.curSquare.rank + 1}':
                        if square.isOccupied and square.occupied_colour != self.colour and square not in self.legal_moves:
                            self.legal_moves.append(square)


            # For black pawns.
            else:

                # For the 'A' file, if the square diagonally-down from curSquare is occupied by an opponent's piece, then add that square to legal_moves
                if curSquare.file == 'A':
                    if square.id == f'{files[index + 1]}{self.curSquare.rank - 1}' and square.isOccupied and square not in self.legal_moves:
                        if square.occupied_colour != self.colour:
                            self.legal_moves.append(square)

                # For the 'H' file, if the square diagonally-down from curSquare is occupied by an opponent's piece, then add that square to legal_moves
                elif curSquare.file == 'H':
                    if square.id == f'{files[index - 1]}{self.curSquare.rank - 1}' and square.isOccupied and square not in self.legal_moves:
                        if square.occupied_colour != self.colour:
                            self.legal_moves.append(square)
                
                # For any other file, if the squares diagonally-down from curSquare are occupied by an opponent's piece, then add them square to legal_moves.
                else:
                    if square.id == f'{files[index + 1]}{self.curSquare.rank - 1}' or square.id == f'{files[index - 1]}{self.curSquare.rank - 1}':
                        if square.isOccupied and square.occupied_colour != self.colour and square not in self.legal_moves:
                            self.legal_moves.append(square)


    # Returns a list of squares available for a given pawn to move to
    # Takes into account everything except for en-passant
    # TODO: Incorporate an en-passant feature
    # TODO: Incorporate a promotion feature.
    def get_legal_moves(self, squares, our_king):

        self.legal_moves = []
        index = self.get_file_index(self.curSquare)

        # First, check diagonals for any taking-opportunities.
        self.take_opponent_piece(self.curSquare, squares)

        # White pieces
        if self.colour == 'white':

            # Check first move rule for pawns
            if self.first_move:

                # If the selected pawn hasn't moved yet and both the squares one square up and two squares up are unoccupied, then add the square two square up to legal_moves.
                one_square_up = self.get_square(f'{self.curSquare.file}{self.curSquare.rank + 1}', squares)
                two_squares_up = self.get_square(f'{self.curSquare.file}{self.curSquare.rank + 2}', squares)
                
                if not two_squares_up.isOccupied and not one_square_up.isOccupied:
                    self.legal_moves.append(two_squares_up)

            # If one square up from curSquare isn't in legal_moves and that square isn't occupied then add it to legal_moves
            one_square_up = self.get_square(f'{self.curSquare.file}{self.curSquare.rank + 1}', squares)
            
            if one_square_up not in self.legal_moves and not one_square_up.isOccupied:
                self.legal_moves.append(one_square_up)
            
            # If one or two squares down from curSquare is in legal_moves, then remove it from legal_moves since pawns can't move backwards
            one_square_down = self.get_square(f'{self.curSquare.file}{self.curSquare.rank - 1}', squares)
            two_squares_down = self.get_square(f'{self.curSquare.file}{self.curSquare.rank - 2}', squares)
            
            if one_square_down in self.legal_moves:
                self.legal_moves.remove(one_square_down)
            if two_squares_down in self.legal_moves:
                self.legal_moves.remove(two_squares_down)
        
        # Black pieces
        else:

            if self.first_move:
                
                # If the selected pawn hasn't moved yet and both the squares one square up and two squares up are unoccupied, then add the square two square up to legal_moves.
                one_square_down = self.get_square(f'{self.curSquare.file}{self.curSquare.rank - 1}', squares)
                two_squares_down = self.get_square(f'{self.curSquare.file}{self.curSquare.rank - 2}', squares)
                
                if not two_squares_down.isOccupied and not one_square_down.isOccupied:
                    self.legal_moves.append(two_squares_down)
            
            # If one square down from curSquare isn't in legal_moves and that square isn't occupied then add it to legal_moves
            one_square_down = self.get_square(f'{self.curSquare.file}{self.curSquare.rank - 1}', squares)

            if one_square_down not in self.legal_moves and not self.get_next_square(self.curSquare, squares):
                self.legal_moves.append(one_square_down)
            
            # If one or two squares up from curSquare is in legal_moves, then remove it from legal_moves since pawns can't move backwards
            one_square_up = self.get_square(f'{self.curSquare.file}{self.curSquare.rank + 1}', squares)
            two_squares_up = self.get_square(f'{self.curSquare.file}{self.curSquare.rank + 2}', squares)

            if one_square_up in self.legal_moves:
                self.legal_moves.remove(one_square_up)
            if two_squares_up in self.legal_moves:
                self.legal_moves.remove(two_squares_up)

        # If the selected pawn's current square is in legal_moves then remove it.
        if self.curSquare in self.legal_moves:
            self.legal_moves.remove(self.curSquare)

        return [square.id for square in self.legal_moves]