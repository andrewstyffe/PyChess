import pygame as pg

# Define colours and constants
black = (0,0,0)
white = (255,255,255)
brown = (150,75,0)
SQUARE_SIZE = 100
BORDER_MARGIN = 25

def main():
    # Initialize pygame
    pg.init()

    # Create the board and caption
    board = pg.display.set_mode((850, 850))
    pg.display.set_caption("Chessboard")

    done = False
    while not done:

        # Keep the board live until the game window is exited
        ev = pg.event.poll()
        if ev.type == pg.QUIT: 
            done = True

        # Create an 8x8 grid
        # Square 0 is the square in the top left-hand corner of the screen. A8 in chess terms.  Square 8 is A7 etc...
        # Every odd-numbered square is coloured white.
        # Here row and column simply act as offsets for the colouring of the squares.
        # I.e. Square 1 has an offset of 1 * SQUARE_SIZE + MARGIN in the x-direction (since it's in column 1)
        # and an offset of 0 * SQUARE_SIZE + MARGIN in the y-direction (since it's in row 0).
        square_num = 0
        for row in range(8):
            for column in range(8):
                colour = white
                if square_num % 2 == 0:
                    colour = brown
                pg.draw.rect(board, colour, (SQUARE_SIZE * column + BORDER_MARGIN, SQUARE_SIZE * row + BORDER_MARGIN, SQUARE_SIZE, SQUARE_SIZE))
                square_num += 1
            square_num -= 1 # This is needed to create a diagonal pattern across the board, otherwise we get strips (columns) of the same colour
        
        getWhitePieces(board)
        getBlackPieces(board)
        pg.display.flip()

    pg.quit()


# Places the white pieces in their correct starting positions
def getWhitePieces(board):

    # Load the white pieces and adjust their sizes
    white_pawn = pg.image.load("./white_pawn.png")
    w_pawns = pg.transform.scale(white_pawn, (50, 50))

    white_rook = pg.image.load("./white_rook.png")
    w_rooks = pg.transform.scale(white_rook, (50, 50))

    white_knight = pg.image.load("./white_knight.png")
    w_knights = pg.transform.scale(white_knight, (50, 50))

    white_bishop = pg.image.load("./white_bishop.png")
    w_bishops = pg.transform.scale(white_bishop, (50, 50))

    white_king = pg.image.load("./white_king.png")
    w_king = pg.transform.scale(white_king, (50, 50))

    white_queen = pg.image.load("./white_queen.png")
    w_queen = pg.transform.scale(white_queen, (50, 50))

    # Place the white pawns
    for column in range(8):
        board.blit(w_pawns, (BORDER_MARGIN + (SQUARE_SIZE * column) + 25, BORDER_MARGIN + (SQUARE_SIZE * 6) + 25))

    # Place the white rooks
    board.blit(w_rooks, (BORDER_MARGIN + 25, BORDER_MARGIN + (SQUARE_SIZE * 7) + 25))
    board.blit(w_rooks, (BORDER_MARGIN + (SQUARE_SIZE * 7) + 25, BORDER_MARGIN + (SQUARE_SIZE * 7) + 25))

    # Place the white knights
    board.blit(w_knights, (BORDER_MARGIN + (SQUARE_SIZE * 1) + 25, BORDER_MARGIN + (SQUARE_SIZE * 7) + 25))
    board.blit(w_knights, (BORDER_MARGIN + (SQUARE_SIZE * 6) + 25, BORDER_MARGIN + (SQUARE_SIZE * 7) + 25))

    # Place the white bishops
    board.blit(w_bishops, (BORDER_MARGIN + (SQUARE_SIZE * 2) + 25, BORDER_MARGIN + (SQUARE_SIZE * 7) + 25))
    board.blit(w_bishops, (BORDER_MARGIN + (SQUARE_SIZE * 5) + 25, BORDER_MARGIN + (SQUARE_SIZE * 7) + 25))

    # Place the white king
    board.blit(w_king, (BORDER_MARGIN + (SQUARE_SIZE * 3) + 25, BORDER_MARGIN + (SQUARE_SIZE * 7) + 25))

    # Place the white queen
    board.blit(w_queen, (BORDER_MARGIN + (SQUARE_SIZE * 4) + 25, BORDER_MARGIN + (SQUARE_SIZE * 7) + 25))


# Places the black pieces in their correct starting positions
def getBlackPieces(board):

    # Load the black pieces and adjust their sizes
    black_pawn = pg.image.load("./black_pawn.png")
    b_pawns = pg.transform.scale(black_pawn, (50, 50))

    black_rook = pg.image.load("./black_rook.png")
    b_rooks = pg.transform.scale(black_rook, (50, 50))

    black_knight = pg.image.load("./black_knight.png")
    b_knights = pg.transform.scale(black_knight, (50, 50))

    black_bishop = pg.image.load("./black_bishop.png")
    b_bishops = pg.transform.scale(black_bishop, (50, 50))

    black_king = pg.image.load("./black_king.png")
    b_king = pg.transform.scale(black_king, (50, 50))

    black_queen = pg.image.load("./black_queen.png")
    b_queen = pg.transform.scale(black_queen, (50, 50))

    # Place the black pawns
    for column in range(8):
        board.blit(b_pawns, (BORDER_MARGIN + (SQUARE_SIZE * column) + 25, BORDER_MARGIN + (SQUARE_SIZE * 1) + 25))

    # Place the black rooks
    board.blit(b_rooks, (BORDER_MARGIN + 25, BORDER_MARGIN + 25))
    board.blit(b_rooks, (BORDER_MARGIN + (SQUARE_SIZE * 7) + 25, BORDER_MARGIN + 25))

    # Place the black knights
    board.blit(b_knights, (BORDER_MARGIN + (SQUARE_SIZE * 1) + 25, BORDER_MARGIN + 25))
    board.blit(b_knights, (BORDER_MARGIN + (SQUARE_SIZE * 6) + 25, BORDER_MARGIN + 25))

    # Place the black bishops
    board.blit(b_bishops, (BORDER_MARGIN + (SQUARE_SIZE * 2) + 25, BORDER_MARGIN + 25))
    board.blit(b_bishops, (BORDER_MARGIN + (SQUARE_SIZE * 5) + 25, BORDER_MARGIN + 25))

    # Place the black king
    board.blit(b_king, (BORDER_MARGIN + (SQUARE_SIZE * 3) + 25, BORDER_MARGIN + 25))

    # Place the black queen
    board.blit(b_queen, (BORDER_MARGIN + (SQUARE_SIZE * 4) + 25, BORDER_MARGIN + 25))


if __name__ == "__main__":
    main()