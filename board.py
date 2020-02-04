import pygame as pg
from pygame.locals import QUIT, KEYUP, K_ESCAPE, Rect
from pygame.draw import rect
import king
import queen
import rook
import bishop
import knight
import pawn
import square

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
    buildboard(board)
    #getPieces(board)

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
                    if piece.rect.collidepoint(mouse_position):
                        piece.clicked = True
                        print('asuh')
                for square in squares:
                    if square.square_coords.collidepoint(mouse_position):
                        print(square.square_id)

            elif event.type == pg.MOUSEBUTTONUP:
                for piece in pieces:
                    piece.clicked = False
            

            for piece in pieces:
                if piece.clicked == True:
                    mouse_position = pg.mouse.get_pos()
                    before_move_square = piece.square
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
def buildboard(board):

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
            if new_square.square_coords not in squares:
                squares.add(new_square)
            rect(board, cur_colour, new_square.square_coords)
            cur_colour = next(alternator) 
        cur_colour = next(alternator)

# Places the pieces in their correct starting positions
def getPieces(board):
    files = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']
    for column in range(8):

        BACK_RANK_COORDS = ((SQUARE_SIZE * column) + 25, (SQUARE_SIZE * 7) + 25)

        # Pawns
        p = pawn.Pawn(((SQUARE_SIZE * column) + 25, (SQUARE_SIZE * 6) + 25), f'{files[column]}2')
        pieces.add(p)
        board.blit(p.image, ((SQUARE_SIZE * column) + 25, (SQUARE_SIZE * 6) + 25))

        # Rooks
        if column == 0 or column == 7:
            r = rook.Rook(BACK_RANK_COORDS, f'{files[column]}1')
            pieces.add(r)
            board.blit(r.image, BACK_RANK_COORDS)
        
        # Knights
        elif column == 1 or column == 6:
            n = knight.Knight(BACK_RANK_COORDS, f'{files[column]}1')
            pieces.add(n)
            board.blit(n.image, BACK_RANK_COORDS)
        
        #Knights
        elif column == 2 or column == 5:
            b = bishop.Bishop(BACK_RANK_COORDS, f'{files[column]}1')
            pieces.add(b)
            board.blit(b.image, BACK_RANK_COORDS)

        # Queen
        elif column == 3:
            q = queen.Queen(BACK_RANK_COORDS, f'{files[column]}1')
            pieces.add(q)
            board.blit(q.image, BACK_RANK_COORDS)

        # King
        else:
            k = king.King(BACK_RANK_COORDS, f'{files[column]}1')
            pieces.add(k)
            board.blit(k.image, BACK_RANK_COORDS)

if __name__ == "__main__":
    main() 