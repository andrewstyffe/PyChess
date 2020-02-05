import pygame as pg
from pygame.locals import QUIT, KEYUP, K_ESCAPE, Rect
from pygame.draw import rect
import chess_pieces
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
selected_piece = None

# Initialize pygame
pg.init()

# Create the board and caption
board = pg.display.set_mode((800, 800))
pg.display.set_caption("Chessboard")

pieces = pg.sprite.Group()
squares = pg.sprite.Group()

def main():

    # Build the board and set the pieces
    buildBoard(board)
    setupBoard(board)

    # Main game loop
    done = False
    while not done:
        for event in pg.event.get():
            # Keep the board live until the game window is exited
            if event.type == pg.QUIT: 
                done = True

            elif event.type == pg.MOUSEBUTTONDOWN:
                mouse_position = pg.mouse.get_pos()
                for piece in pieces:
                    #print(piece.rect)
                    if piece.rect.collidepoint(mouse_position):
                        print(piece.name)
                        piece.clicked = True
                        #print('asuh')
                # for square in squares:
                #     if square.coords.collidepoint(mouse_position):
                #         print(square.coords.topleft)
                #         #print(square.rank)

            elif event.type == pg.MOUSEBUTTONUP:
                for piece in pieces:
                    piece.clicked = False
            

            for piece in pieces:
                if piece.clicked == True:
                    mouse_position = pg.mouse.get_pos()
                    #before_move_square = piece.square
                    piece.rect.x = mouse_position[0] - (piece.rect.width / 2)
                    piece.rect.y = mouse_position[1] - (piece.rect.height / 2)
            

            pg.display.flip()
    pg.quit()

# Toggles between the two colours 
def alternate():
    while True:
        yield brown
        yield light_brown


# Create an 8x8 grid
def buildBoard(board):

    # Create a 'toggler'
    alternator = alternate()

    increment = board_width / 8
    cur_colour = light_brown

    coords = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H']

    # Starting at the top left-hand corner (0, 0), create the board    
    for column in range(8):
        for row in range(8):
            new_square = square.Square(Rect(row * increment, column * increment, increment + 1, increment + 1), f'{coords[row]}{8 - column}')
            if new_square not in squareCenters:
                squareCenters.append(new_square)
            squares.add(new_square)
            rect(board, cur_colour, new_square.coords)
            cur_colour = next(alternator) 
        cur_colour = next(alternator)


# Places the pieces in their correct starting positions
def setupBoard(board):
    
    # Get all squares of interest
    eligible_squares = [square for square in squares if square.rank == '1' or square.rank == '2' or square.rank == '7' or square.rank == '8']
    
    for square in eligible_squares:

        # Set the colour
        if square.rank == '1' or square.rank == '2':
            colour = 'white'
        else:
            colour = 'black'

        # Determine which piece to be created based on rank and column
        if square.rank == '2' or square.rank == '7':
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
        
        pieces.add(piece)
        board.blit(piece.image, (square.x + 25, square.y + 25))

if __name__ == "__main__":
    main() 