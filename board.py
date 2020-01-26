import pygame as pg

# Initialize pygame
pg.init()

# Define colours and constants
black = (0,0,0)
white = (255,255,255)
brown = (150,75,0)
SQUARE_SIZE = 100
BORDER_MARGIN = 25

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
    
    pg.display.flip()

pg.quit()