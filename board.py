import pygame as pg
from pygame.locals import QUIT, KEYUP, K_ESCAPE, Rect
from pygame.draw import rect
from chess_pieces import *
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
white_king = None
black_king = None

our_king = None
opponents_king = None

files_dict = {'A' : 8, 'B' : 7, 'C' : 6, 'D' : 5, 'E' : 4, 'F' : 3, 'G' : 2, 'H' : 1}

# Initialize pygame
pg.init()

# Create the board and caption
board = pg.display.set_mode((800, 800))
pg.display.set_caption("Chessboard")

# Create the sprite groups
pieces = pg.sprite.Group()
squares = pg.sprite.Group()

def main():
    
    # Build the board and set the pieces
    buildBoard(board)
    white_king, black_king = setupBoard(board)
    
    team_alternator = alternate_teams()

    mouse_down = False
    selected_piece = None

    # Main game loop
    done = False
    turn = 'white'
    
    while not done:

        # Get events
        for event in pg.event.get():

            # Keep the board live until the game window is exited
            if event.type == pg.QUIT: 
                done = True

            if turn == 'white':
                our_king = white_king
                opponents_king = black_king
            else:
                our_king = black_king
                opponents_king = white_king
            
            # Check if our king is in check.  If it is, we can't make just any move.
            for piece in pieces:
                if piece.colour != turn and piece.name != 'Pawn' and piece.name != 'King': # TODO: NEED TO FIX THIS!!!
                    if our_king.curSquare.id in piece.get_legal_moves(squares, our_king):
                        our_king.in_check = True
                        our_king.checking_piece = piece

                        if our_king.checking_piece.name == 'Bishop':
                            our_king.in_check_along_diagonal = True

                        elif our_king.checking_piece.name == 'Rook':

                            if our_king.curSquare.file == piece.curSquare.file:
                                print('A')
                                our_king.in_check_along_file = True

                            elif our_king.curSquare.rank == piece.curSquare.rank:
                                print('B')
                                our_king.in_check_along_rank = True

                        elif our_king.checking_piece.name == 'Queen':

                            if our_king.curSquare.file == piece.curSquare.file:
                                our_king.in_check_along_file = True

                            elif our_king.curSquare.rank == piece.curSquare.rank:
                                our_king.in_check_along_rank = True

                            elif our_king.curSquare in piece.curSquare.diagonals:
                                our_king.in_check_along_diagonal = True

                        elif our_king.checking_piece.name == 'Pawn':
                            our_king.in_check_along_diagonal = True

                        break

            # Get the current mouse event
            if event.type == pg.MOUSEBUTTONDOWN:
                
                # Get current mouse position and check pieces against that position
                mouse_down_position = pg.mouse.get_pos()

                castling = False
                # Find and move the selected piece
                for piece in pieces:
                    if piece.rect.collidepoint(mouse_down_position) and piece.colour == turn:

                        # Selected piece found - get its data
                        selected_piece = piece
                        fromSquare = selected_piece.curSquare
                        selected_piece.fromSquare = fromSquare
                        
                        # If we are in check, we have to either move the king, take the piece checking-us, or block the piece checking-us.
                        if our_king.in_check:
                            print('asuh')

                        print(f'{selected_piece.colour} {selected_piece.name} selected. Its curSquare is {selected_piece.curSquare.id}')
                        if selected_piece.name == 'King':
                            print(f'Its available moves are {selected_piece.get_legal_moves(squares, pieces, our_king)}')
                        else:
                            print(f'Its available moves are {selected_piece.get_legal_moves(squares, our_king)}')

                        # 'Erase' the old position of the selected piece, by drawing over it the original square
                        pg.draw.rect(board, fromSquare.colour, (fromSquare.x, fromSquare.y, 100, 100))
                        selected_piece.drag(board, mouse_down_position)
                        #board.blit(selected_piece.image, (mouse_down_position[0], mouse_down_position[1]))
                        break
                        

            # If we are done dragging, get the square we moved to
            elif event.type == pg.MOUSEBUTTONUP:
                up_mouse_position = pg.mouse.get_pos()
                for square_of_interest in squares:
                    if square_of_interest.coords.collidepoint(up_mouse_position) and selected_piece:

                        # Deals with castling
                        if selected_piece.name == 'King' and square_of_interest.id != selected_piece.curSquare.id:

                            # If the selected square represents a legal move for the selected king.
                            if square_of_interest in selected_piece.legal_moves:

                                # The case where the selected king is castling.
                                if files_dict[selected_piece.curSquare.file] == files_dict[square_of_interest.file] + 2 or files_dict[selected_piece.curSquare.file] == files_dict[square_of_interest.file] - 2:
                                    castling = True
                                    turn, selected_piece = castle(square_of_interest, selected_piece, fromSquare, team_alternator, castling, our_king, opponents_king)
                                    
                                # The case where the selected king is making a non-castling move.
                                else:
                                    turn, selected_piece = format_move(selected_piece, square_of_interest, fromSquare, team_alternator, castling, our_king, opponents_king)
                            # If the square we clicked on isn't a legal move for the selected king, then put the king back to its starting square.
                            else:
                                print('Invalid move. Try again.')
                                selected_piece.update(board, fromSquare, fromSquare)
                                selected_piece.first_move = True
                                selected_piece.draw(board)
                                selected_piece = None
                        
                        # For every piece that is not a king.
                        elif selected_piece:
                            
                            # If the square of interest represents a legal move for the selected piece.
                            if square_of_interest in selected_piece.legal_moves:
                                turn, selected_piece = format_move(selected_piece, square_of_interest, fromSquare, team_alternator, castling, our_king, opponents_king)

                            # If the square of interest represents an illegal move for the selected piece, then return that piece to its fromSquare.
                            else:
                                print('Invalid move. Try again.')
                                selected_piece.update(board, fromSquare, fromSquare)
                                selected_piece.draw(board)
                                selected_piece = None
                    
                    our_king.in_check = False
                    # If we are in check, then reset all of the king's variables to being False
                    if our_king and our_king.in_check:
                        print('Our king is in check.')
                        
                        if our_king.checking_piece.name == 'Bishop':
                            our_king.in_check_along_diagonal = False

                        elif our_king.checking_piece.name == 'Rook':

                            if our_king.curSquare.file == piece.curSquare.file:
                                our_king.in_check_along_file = False

                            elif our_king.curSquare.rank == piece.curSquare.rank:
                                our_king.in_check_along_rank = False

                        elif our_king.checking_piece.name == 'Queen':

                            if our_king.curSquare.file == piece.curSquare.file:
                                our_king.in_check_along_file = False

                            elif our_king.curSquare.rank == piece.curSquare.rank:
                                our_king.in_check_along_rank = False

                            elif our_king.curSquare.diagonals in piece.curSquare.diagonals:
                                our_king.in_check_along_diagonal = False

                        elif our_king.checking_piece.name == 'Pawn':
                            our_king.in_check_along_diagonal = False
        
            pg.display.update()
    pg.quit()

def castle(square_of_interest, selected_piece, fromSquare, team_alternator, castling, our_king, opponents_king):
    # Get the rook whose current square is rook_fromSquare
    rook_of_interest = None

    for rook in [piece for piece in pieces if piece.name == 'Rook']:
        if square_of_interest.id == 'G1':
            if rook.curSquare.id == 'H1':
                rook_of_interest = rook
        elif square_of_interest.id == 'C1':
            if rook.curSquare.id == 'A1':
                rook_of_interest = rook
        elif square_of_interest.id == 'G8':
            if rook.curSquare.id == 'H8':
                rook_of_interest = rook
        elif square_of_interest.id == 'C8':
            if rook.curSquare.id == 'A8':
                rook_of_interest = rook

    new_file = ''
    for key, val in files_dict.items():
        if square_of_interest.id == 'G1' or square_of_interest.id == 'G8':
            if val == files_dict[square_of_interest.file] + 1:
                new_file = key
        elif square_of_interest.id == 'C1' or square_of_interest.id == 'C8':
            if val == files_dict[square_of_interest.file] - 1:
                new_file = key

    # Update the selected king and the accompanying rook.
    pg.draw.rect(board, rook_of_interest.curSquare.colour, (rook_of_interest.curSquare.x, rook_of_interest.curSquare.y, 100, 100))
    rook_of_interest.update(board, rook_of_interest.curSquare, selected_piece.get_square(f'{new_file}{square_of_interest.rank}', squares))
    rook_of_interest.draw(board)
    
    selected_piece = format_move(selected_piece, square_of_interest, fromSquare, team_alternator, castling, our_king, opponents_king)
    return next(team_alternator), selected_piece


# Deals with printing the move to the screen and updating piece information after every move.
def format_move(selected_piece, square_of_interest, fromSquare, team_alternator, castling, our_king, opponents_king):

    selected_piece.update(board, fromSquare, square_of_interest)
    selected_piece.draw(board)
    print(f'{selected_piece.colour} {selected_piece.name} released. Its curSquare is {selected_piece.curSquare.id}')

    if selected_piece.name == 'King':
        print(f'Now its available moves are {selected_piece.get_legal_moves(squares, pieces, our_king)}')
    else:
        if selected_piece.name == 'Pawn':
            selected_piece.first_move = False
        print(f'Now its available moves are {selected_piece.get_legal_moves(squares, our_king)}')
    
    if selected_piece.name != 'Pawn' and opponents_king and opponents_king.curSquare in selected_piece.legal_moves:
        print('CHECK!')

    print(f'{selected_piece.name} moved from {fromSquare.id} to {square_of_interest.id}.  Its new square is {selected_piece.curSquare.id}')
    print('\n----------------------\n')
    
    selected_piece = None

    if castling:
        return selected_piece
    else:
        return next(team_alternator), selected_piece

# Toggles between the two teams 
def alternate_teams():
    while True:
        yield 'black'
        yield 'white'


# Toggles between the two colours 
def alternate_colours():
    while True:
        yield brown
        yield light_brown


# Create an 8x8 grid
def buildBoard(board):

    # Create a 'toggler'
    alternator = alternate_colours()

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
    eligible_squares = [square for square in squares if square.rank == 1 or square.rank == 2 or square.rank == 7 or square.rank == 8]
    
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
        
        # While we are here, set square.isOccupied to be True, since when square objects are created, these are set to be False.
        square.isOccupied = True
        square.occupied_colour = colour

        pieces.add(piece)

        board.blit(piece.image, piece.rect)
        pg.display.update()  
    
    # We need to get the legal moves for each piece on startup, since if a king is selected to move
    # we need to check that no opponent's piece is controlling a given surrounding square of that king.
    # But since kings can move before every other piece has been moved, we account for that by getting every piece's available moves right away.
    for piece in pieces:
        if piece.name == 'King':
            piece.get_legal_moves(squares, pieces, None)
            #print(f'{piece.colour} {piece.name} has these moves available to it {piece.get_legal_moves(squares, pieces)}')
        else:
            print(piece.name)
            piece.get_legal_moves(squares, None)
            if piece.name == 'Pawn':
                piece.first_move = True
            #print(f'{piece.colour} {piece.name} has these moves available to it {piece.get_legal_moves(squares)}')

    return white_king, black_king

if __name__ == "__main__":
    main() 