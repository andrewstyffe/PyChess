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
turn = None

# Initialize pygame
pg.init()

# Create the board and caption
board = pg.display.set_mode((800, 800))
pg.display.set_caption("Chessboard")

# Create the sprite groups
pieces = pg.sprite.Group()
squares = pg.sprite.Group()

def main():

    mouse_down = False
    selected_piece = None

    # Build the board and set the pieces
    buildBoard(board)
    setupBoard(board)

    # Main game loop
    done = False
    turn = 'white'
    
    team_alternator = alternate_teams()

    while not done:

        # Get events
        for event in pg.event.get():

            # Keep the board live until the game window is exited
            if event.type == pg.QUIT: 
                done = True

            # Get the current mouse event
            if event.type == pg.MOUSEBUTTONDOWN:
                
                # Get current mouse position and check pieces against that position
                mouse_down_position = pg.mouse.get_pos()

                # Find and move the selected piece
                for piece in pieces:
                    if piece.rect.collidepoint(mouse_down_position) and piece.colour == turn:

                        # Selected piece found - get its data
                        selected_piece = piece
                        fromSquare = selected_piece.curSquare
                        selected_piece.fromSquare = fromSquare

                        print(f'Piece selected. Pieces curSquare is {piece.curSquare.id}')
                        print(f'Pieces available moves are {selected_piece.get_legal_moves(squares)}')

                        # 'Erase' the old position of the selected piece, by drawing over it the original square
                        pg.draw.rect(board, fromSquare.colour, (fromSquare.x, fromSquare.y, 100, 100))
                        selected_piece.drag(board, mouse_down_position)
                        #board.blit(selected_piece.image, (mouse_down_position[0], mouse_down_position[1]))
                        break

            # If we are done dragging, get the square we moved to
            elif event.type == pg.MOUSEBUTTONUP:
                up_mouse_position = pg.mouse.get_pos()
                for square in squares:
                    if square.coords.collidepoint(up_mouse_position) and selected_piece and square.id in selected_piece.legal_moves and not square.isOccupied:  
                        selected_piece.update(board, fromSquare, square)
                        print(f'Piece released. Pieces curSquare is {piece.curSquare.id}')
                        print(f'Piece available moves are {selected_piece.get_legal_moves(squares)}')
                        #print(selected_piece.legal_moves)

                        print(f'{selected_piece.name} moved from {fromSquare.id} to {square.id}.  Its new square is {selected_piece.curSquare.id}\n')
                        selected_piece.draw(board)
                        selected_piece = None
                        turn = next(team_alternator)
                        break
            
            # for piece in pieces:
            #     if piece.name == 'Pawn':
            #         piece.get_legal_moves(squares)
            pg.display.update()
    pg.quit()


# Toggles between the two teams 
def alternate_teams():
    while True:
        yield 'black'
        yield 'white'


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
            new_square = square.Square(Rect(row * increment, column * increment, increment + 1, increment + 1), f'{coords[row]}{8 - column}', cur_colour)
            if new_square not in squareCenters:
                squareCenters.append(new_square)
            squares.add(new_square)
            pg.draw.rect(board, cur_colour, (new_square.x, new_square.y, 100, 100))
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
            #piece.get_legal_moves(squares)

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
        board.blit(piece.image, piece.rect)
        pg.display.update()  

if __name__ == "__main__":
    main() 