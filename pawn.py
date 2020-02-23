import pygame as pg
from chess_pieces import *

# Describes the various attributes of a pawn and enforces the rules of a pawn on the object
# TODO: enforce en-passant
# TODO: Fix all this code... Not great.
class Pawn(ChessPiece):
    def __init__(self, square, colour):
        super(Pawn, self).__init__(self, square, colour)
        self.name = 'Pawn'
        
        # Just for pawns
        self.first_move = True

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

    # Returns the corresponding square given a square id
    def get_square(self, chess_coord, squares):
        for square in squares:
            if square.id == chess_coord:
                return square

    # Returns True or False corresponding to the square directly above or below curSquare (depending on perspective) being occupied by a piece.
    def get_next_square(self, curSquare, squares):
        curRank = int(self.curSquare.rank)

        for square in squares:
            if self.colour == 'white':
                if square.id == f'{curSquare.file}{curRank + 1}':
                    return square.isOccupied
            if square.id == f'{curSquare.file}{curRank - 1}':
                return square.isOccupied 

    # Deals with taking opponent's pieces, since pawns take differently from how they normally move.
    def take_opponent_piece(self, curSquare, squares):
        curRank = int(self.curSquare.rank)
        index = self.get_file_index(curSquare)

        for square in squares:

            # For white pawns
            if self.colour == 'white':

                # For the 'A' file, if the square diagonally-up from curSquare is occupied by an opponent's piece, then add that square to legal_moves
                if curSquare.file == 'A':
                    if square.id == f'{files[index + 1]}{curRank + 1}' and square.isOccupied and f'{files[index + 1]}{curRank + 1}' not in self.legal_moves:
                        print(f'{square.id} is {square.isOccupied} by a {square.occupied_colour} piece! Take it!')
                        self.legal_moves.append(square.id)

                    if square.id in self.legal_moves and square.isOccupied and square.rank < self.curSquare.rank:
                        self.legal_moves.remove(square.id)

                # For the 'H' file, if the square diagonally-up from curSquare is occupied by an opponent's piece, then add that square to legal_moves
                elif curSquare.file == 'H':
                    if square.id == f'{files[index - 1]}{curRank + 1}' and square.isOccupied and square.occupied_colour != self.colour:
                        self.legal_moves.append(square.id)

                    if square.id in self.legal_moves and square.isOccupied and square.rank < self.curSquare.rank:
                        self.legal_moves.remove(square.id)
                
                # For any other file, if the squares diagonally-up from curSquare are occupied by an opponent's piece, then add them square to legal_moves
                else:
                    if square.id == f'{files[index + 1]}{curRank + 1}' or square.id == f'{files[index - 1]}{curRank + 1}':
                        if square.isOccupied and square.occupied_colour != self.colour and square.id not in self.legal_moves:
                            self.legal_moves.append(square.id)
                        
                        # For when an opponent's piece was eligible to be taken, but wasn't, and has now moved.  That square needs to be removed from legal_moves.    
                        else:
                            if square.id in self.legal_moves and not square.isOccupied:
                                self.legal_moves.remove(square.id)


            # For black pawns
            else:

                # For the 'A' file, if the square diagonally-down from curSquare is occupied by an opponent's piece, then add that square to legal_moves
                if curSquare.file == 'A':
                    if square.id == f'{files[index + 1]}{curRank - 1}' and square.isOccupied and square.occupied_colour != self.colour:
                        self.legal_moves.append(square.id)

                    if square.id in self.legal_moves and square.isOccupied and square.rank > self.curSquare.rank:
                        self.legal_moves.remove(square.id)

                # For the 'H' file, if the square diagonally-up from curSquare is occupied by an opponent's piece, then add that square to legal_moves
                elif curSquare.file == 'H':
                    if square.id == f'{files[index - 1]}{curRank - 1}' and square.isOccupied and square.occupied_colour != self.colour:
                        self.legal_moves.append(square.id)

                    if square.id in self.legal_moves and square.isOccupied and square.rank > self.curSquare.rank:
                        self.legal_moves.remove(square.id)
                
                # For any other file, if the squares diagonally-up from curSquare are occupied by an opponent's piece, then add them square to legal_moves
                else:
                    if square.id == f'{files[index + 1]}{curRank - 1}' or square.id == f'{files[index - 1]}{curRank - 1}':
                        if square.isOccupied and square.occupied_colour != self.colour and square.id not in self.legal_moves:
                            self.legal_moves.append(square.id)
                        
                        # For when an opponent's piece was eligible to be taken, but wasn't, and has now moved.  That square needs to be removed from legal_moves.    
                        else:
                            if square.id in self.legal_moves and not square.isOccupied:
                                self.legal_moves.remove(square.id)



    # Returns a list of squares available for a given pawn to move to
    # Takes into account everything except for en-passant
    # TODO: Incorporate an en-passant feature
    def get_legal_moves(self, squares, our_king):

        curRank = int(self.curSquare.rank)
        index = self.get_file_index(self.curSquare)

        # First, check diagonals for taking-opportunities
        self.take_opponent_piece(self.curSquare, squares)

        # White pieces
        if self.colour == 'white':

            # Check first move rule for pawns
            if self.first_move:

                # For the case that a pawn has advanced to 2 squares in front of a pawn that hasn't yet moved. We can't add that sqaure to legal_moves.
                # If that square is not occupied then no issue.
                if not self.get_square(f'{self.curSquare.file}{curRank + 2}', squares).isOccupied:
                    self.legal_moves.append(f'{self.curSquare.file}{curRank + 2}')
                    self.first_move = False
                
                # If it is occupied then simply set first_move to false since one square up from curSquare will be added to legal_moves in a check below.
                else:
                    self.first_move = False

            # If one square up from curSquare isn't in legal_moves and that square isn't occupied then add it to legal_moves
            if f'{self.curSquare.file}{curRank + 1}' not in self.legal_moves and not self.get_next_square(self.curSquare, squares):
                self.legal_moves.append(f'{self.curSquare.file}{curRank + 1}')
            
            # If one or two squares down from curSquare is in legal_moves, then remove it from legal_moves since pawns can't move backwards
            if f'{self.curSquare.file}{curRank - 1}' in self.legal_moves:
                self.legal_moves.remove(f'{self.curSquare.file}{curRank - 1}')
            if f'{self.curSquare.file}{curRank - 2}' in self.legal_moves:
                self.legal_moves.remove(f'{self.curSquare.file}{curRank - 2}')

            # If the square on either side of curSquare is in legal_moves, then remove it from legal_moves since pawns can't move sideways
            if index < 7 and f'{files[index + 1]}{curRank}' in self.legal_moves:
                self.legal_moves.remove(f'{files[index + 1]}{curRank}')
            if index > 0 and f'{files[index - 1]}{curRank}' in self.legal_moves:
                self.legal_moves.remove(f'{files[index - 1]}{curRank}')

            # If our current square is in legal_moves, then remove it 
            if f'{self.curSquare.file}{self.curSquare.rank}' in self.legal_moves:
                self.legal_moves.remove(f'{self.curSquare.file}{self.curSquare.rank}')
        
        # Black pieces
        else:

            if self.first_move:
                
                # For the case that a pawn has advanced to 2 squares in front of a pawn that hasn't yet moved. We can't add that sqaure to legal_moves.
                # If that square is not occupied then no issue.
                if not self.get_square(f'{self.curSquare.file}{curRank - 2}', squares).isOccupied:
                    self.legal_moves.append(f'{self.curSquare.file}{curRank - 2}')
                    self.first_move = False
                
                # If it is occupied then simply set first_move to false since one square up from curSquare will be added to legal_moves in a check below.
                else:
                    self.first_move = False
            
            # If one square down from curSquare isn't in legal_moves and that square isn't occupied then add it to legal_moves
            if f'{self.curSquare.file}{curRank - 1}' not in self.legal_moves and not self.get_next_square(self.curSquare, squares):
                self.legal_moves.append(f'{self.curSquare.file}{curRank - 1}')
            
            # If one or two squares up from curSquare is in legal_moves, then remove it from legal_moves since pawns can't move backwards
            if f'{self.curSquare.file}{curRank + 1}' in self.legal_moves:
                self.legal_moves.remove(f'{self.curSquare.file}{curRank + 1}')
            if f'{self.curSquare.file}{curRank + 2}' in self.legal_moves:
                self.legal_moves.remove(f'{self.curSquare.file}{curRank + 2}')

            # If the square on either side of curSquare is in legal_moves, then remove it from legal_moves since pawns can't move sideways
            if index < 7 and f'{files[index + 1]}{curRank}' in self.legal_moves:
                self.legal_moves.remove(f'{files[index + 1]}{curRank}')
            if index > 0 and f'{files[index - 1]}{curRank}' in self.legal_moves:
                self.legal_moves.remove(f'{files[index - 1]}{curRank}')

            # If our current square is in legal_moves, then remove it 
            if f'{self.curSquare.file}{self.curSquare.rank}' in self.legal_moves:
                self.legal_moves.remove(f'{self.curSquare.file}{self.curSquare.rank}')

        return self.legal_moves