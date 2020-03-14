import pygame as pg
from pygame.locals import QUIT, KEYUP, K_ESCAPE, Rect
import square
import king
import queen
import rook
import bishop
import knight
import pawn

# Define colours and constants
light_brown = (250, 190, 120)
brown = (150,75,0)
board_width = board_height = 800
squareCenters = []
SQUARE_SIZE = 100

class Board:

    def __init__(self, w, h, name):
        self.width = w
        self.height = h
        self.screen = pg.display.set_mode((w,h))
        pg.display.set_caption(name)
        self.squares = pg.sprite.Group()
        self.pieces = pg.sprite.Group()
        self.white_pieces = pg.sprite.Group()
        self.black_pieces = pg.sprite.Group()
        if name.split()[2] == 'white':
            self.buildBoard(self, 'white')
        else:
            self.buildBoard(self, 'black')
        self.setupBoard(self)

    # Toggles between the two colours 
    def alternate_colours(self):
        while True:
            yield brown
            yield light_brown

        # Create an 8x8 grid
    def buildBoard(self, board, perspective):

        # Create a 'toggler'
        alternator = self.alternate_colours()

        increment = board_width / 8

        if perspective == 'white':
            cur_colour = light_brown

            coords = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H']

            # Starting at the top left-hand corner (0, 0), create the board    
            for column in range(8):
                for row in range(8):
                    new_square = square.Square(Rect(row * increment, column * increment, increment + 1, increment + 1), f'{coords[row]}{8 - column}', cur_colour)
                    if new_square not in squareCenters:
                        squareCenters.append(new_square)
                    self.squares.add(new_square)
                    pg.draw.rect(self.screen, cur_colour, (new_square.x, new_square.y, 100, 100))
                    cur_colour = next(alternator) 
                cur_colour = next(alternator)
        
        else:
            cur_colour = next(alternator)

            coords = ['H', 'G', 'F', 'E', 'D', 'C', 'B', 'A']

            # Starting at the top left-hand corner (0, 0), create the board    
            for column in range(8):
                for row in range(8):
                    new_square = square.Square(Rect(row * increment, column * increment, increment + 1, increment + 1), f'{coords[row]}{column + 1}', cur_colour)
                    if new_square not in squareCenters:
                        squareCenters.append(new_square)
                    self.squares.add(new_square)
                    pg.draw.rect(self.screen, cur_colour, (new_square.x, new_square.y, 100, 100))
                    cur_colour = next(alternator) 
                cur_colour = next(alternator)

    # Places the pieces in their correct starting positions
    def setupBoard(self, board):
        white_king = None
        black_king = None
        
        # Get all squares of interest
        eligible_squares = [square for square in self.squares if square.rank == 1 or square.rank == 2 or square.rank == 7 or square.rank == 8]
        
        for square in eligible_squares:
            
            # Set the colour
            if square.rank == 1 or square.rank == 2:
                colour = 'white'
            else:
                colour = 'black'

            # Determine which piece to be created based on rank and column
            if square.rank == 2 or square.rank == 7:
                piece = pawn.Pawn(square, colour)

            else:
                if square.file == 'A' or square.file == 'H':
                    piece = rook.Rook(square, colour)

                elif square.file == 'B' or square.file == 'G':
                    piece = knight.Knight(square, colour)

                elif square.file == 'C' or square.file == 'F':
                    piece = bishop.Bishop(square, colour)
            
                elif square.file == 'D':
                    piece = queen.Queen(square, colour)

                else:
                    piece = king.King(square, colour)
                    if square.id == 'E1':
                        white_king = piece
                    else:
                        black_king = piece

            self.pieces.add(piece)
            
            # While we are here, set square.isOccupied to be True, since when square objects are created, these are set to be False.
            square.isOccupied = True
            square.occupied_colour = colour

            self.screen.blit(piece.image, piece.rect)
            pg.display.update()  
        
        # Add pieces to appropriate groups
        for piece in self.pieces:
            if piece.colour == 'white':
                self.white_pieces.add(piece)
            else:
                self.black_pieces.add(piece)

        # We need to get the legal moves for each piece on startup, since if a king is selected to move
        # we need to check that no opponent's piece is controlling a given surrounding square of that king.
        # But since knights can move before every other piece has been moved, we account for that by getting every piece's available moves right away.
        for piece in self.pieces:
            
            # Get the legal moves for the current piece.
            if piece.name == 'King':
                piece.get_legal_moves(self.squares, self.pieces, None, None)
                if piece.colour == 'white':
                    white_king = piece
                else:
                    black_king = piece
            else:
                piece.get_legal_moves(self.squares, self.pieces, None, None)
            
            # Update pawn attribute.
            if piece.name == 'Pawn':
                piece.first_move = True

            # Now get each piece's king and its opponent's king.
            for k in [piece for piece in self.pieces if piece.name == 'King']:
                if piece.colour == k.colour:
                    piece.our_king = k
                else:
                    piece.opponents_king = k
        
        return white_king, black_king