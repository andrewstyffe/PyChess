import pygame as pg
import king
import queen
import rook
import bishop
import knight
import pawn

# Define colours and constants
black = (0,0,0)
white = (255,255,255)
brown = (150,75,0)
SQUARE_SIZE = 100
BORDER_MARGIN = 25

# Initialize pygame
pg.init()

# Create the board and caption
board = pg.display.set_mode((850, 850))
pg.display.set_caption("Chessboard")

pieces = pg.sprite.Group()

def main():

    # Build the board and set the pieces
    buildboard(board)
    getPieces(board)
    #print(key_list)

    done = False
    while not done:
        for event in pg.event.get():
            # Keep the board live until the game window is exited
            if event.type == pg.QUIT: 
                done = True

            elif event.type == pg.MOUSEBUTTONDOWN:
                pos = pg.mouse.get_pos()
                for piece in pieces:
                    if piece.rect.collidepoint(pos):
                        piece.clicked = True
                        print('asuh')

            elif event.type == pg.MOUSEBUTTONUP:
                for piece in pieces:
                    piece.clicked = False
            

            for piece in pieces:
                if piece.clicked == True:
                    pos = pg.mouse.get_pos()
                    piece.rect.x = pos[0] - (piece.rect.width / 2)
                    piece.rect.y = pos[1] - (piece.rect.height / 2)
            
            pieces.draw(board)
            pg.display.flip()
    pg.quit()

def buildboard(board):
    # Create an 8x8 grid
        # Square 0 is the square in the top left-hand corner of the screen. A8 in chess terms.  Square 8 is A7 etc...
        # Every odd-numbered square is coloured white.
        # Here row and column simply act as offsets for the colouring of the squares.
        # I.e. Square 1 has an offset of 1 * SQUARE_SIZE + MARGIN in the x-direction (since it's in column 1)
        # and an offset of 0 * SQUARE_SIZE + MARGIN in the y-direction (since it's in row 0).
        square_num = 0
        for row in range(8):
            for column in range(8):
                colour = brown
                if square_num % 2 == 0:
                    colour = white
                pg.draw.rect(board, colour, (SQUARE_SIZE * column + BORDER_MARGIN, SQUARE_SIZE * row + BORDER_MARGIN, SQUARE_SIZE, SQUARE_SIZE))
                square_num += 1
            square_num -= 1 # This is needed to create a diagonal pattern across the board, otherwise we get strips (columns) of the same colour

def getPieces(board):
    files = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']
    for column in range(8):

        BACK_RANK_COORDS = (BORDER_MARGIN + (SQUARE_SIZE * column) + 25, BORDER_MARGIN + (SQUARE_SIZE * 7) + 25)

        # Pawns
        p = pawn.Pawn((BORDER_MARGIN + (SQUARE_SIZE * column) + 25, BORDER_MARGIN + (SQUARE_SIZE * 6) + 25), f'{files[column]}2')
        pieces.add(p)
        board.blit(p.image, (BORDER_MARGIN + (SQUARE_SIZE * column) + 25, BORDER_MARGIN + (SQUARE_SIZE * 6) + 25))

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