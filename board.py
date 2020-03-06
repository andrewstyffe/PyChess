import pygame as pg
from pygame.locals import QUIT, KEYUP, K_ESCAPE, Rect
from pygame.draw import rect
from chess_pieces import *
import subprocess
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
white_pieces = pg.sprite.Group()
black_pieces = pg.sprite.Group()
squares = pg.sprite.Group()


def main():
    
    # Build the board and set the pieces
    buildBoard(board)
    white_king, black_king = setupBoard(board)
    #white_king, black_king = 
    team_alternator = alternate_teams()
    king_alternator = alternate_kings(white_king, black_king)
    #turn = next(team_alternator)
    #print(turn)

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

            # Get the current mouse event
            if event.type == pg.MOUSEBUTTONDOWN:
                
                # Get current mouse position and check pieces against that position
                mouse_down_position = pg.mouse.get_pos()

                castling = False
                our_king = [piece for piece in pieces if piece.name == 'King' and piece.colour == turn][0]
                opponents_king = [piece for piece in pieces if piece.name == 'King' and piece.colour != turn][0]
                
                # Find and move the selected piece
                for piece in pieces:
                    if piece.rect.collidepoint(mouse_down_position) and piece.colour == turn:

                        # Selected piece found - get its data
                        selected_piece = piece
                        fromSquare = selected_piece.curSquare
                        selected_piece.fromSquare = fromSquare

                        # Get the legal moves of every piece on the board before the selected piece has moved.
                        print(f'{selected_piece.colour} {selected_piece.name} selected. Its curSquare is {selected_piece.curSquare.id}')
                        for piece in pieces:
                            if piece.name != 'King':
                                piece.get_legal_moves(squares, pieces, selected_piece, our_king)
                            else:
                                piece.get_legal_moves(squares, pieces, selected_piece, our_king)

                        # Get the legal moves of the selected piece.
                        print(f'The selected piece"s available moves are {[square.id for square in selected_piece.legal_moves]}')

                        # 'Erase' the old position of the selected piece, by drawing over it the original square
                        pg.draw.rect(board, fromSquare.colour, (fromSquare.x, fromSquare.y, 100, 100))
                        selected_piece.drag(board, mouse_down_position)
                        break
                        

            # If we are done dragging, get the square we moved to
            elif event.type == pg.MOUSEBUTTONUP:
                up_mouse_position = pg.mouse.get_pos()
                for square_of_interest in squares:
                    if square_of_interest.coords.collidepoint(up_mouse_position) and selected_piece:

                        # Deals with castling
                        if selected_piece.name == 'King':

                            # If the selected square represents a legal move for the selected king.
                            if square_of_interest in selected_piece.legal_moves and square_of_interest.id != selected_piece.curSquare.id:

                                # The case where the selected king is castling.
                                if files_dict[selected_piece.curSquare.file] == files_dict[square_of_interest.file] + 2 or files_dict[selected_piece.curSquare.file] == files_dict[square_of_interest.file] - 2:
                                    castling = True
                                    turn, selected_piece = castle(square_of_interest, selected_piece, fromSquare, team_alternator, castling, our_king, opponents_king, turn)
                                    
                                # The case where the selected king is making a non-castling move.
                                else:
                                    turn, selected_piece = format_move(selected_piece, square_of_interest, fromSquare, team_alternator, castling, our_king, opponents_king, turn)
                            # If the square we clicked on isn't a legal move for the selected king, then put the king back to its starting square.
                            else:
                                print('Invalid move. Try again.')
                                selected_piece.update(board, fromSquare, fromSquare)

                                if selected_piece.first_move:
                                    selected_piece.first_move = True
                                selected_piece.draw(board)
                                selected_piece = None
                        
                        # For every piece that is not a king.
                        else:
                            
                            # If the square of interest represents a legal move for the selected piece.
                            if square_of_interest in selected_piece.legal_moves:
                                turn, selected_piece = format_move(selected_piece, square_of_interest, fromSquare, team_alternator, castling, our_king, opponents_king, turn)

                            # If the square of interest represents an illegal move for the selected piece, then return that piece to its fromSquare.
                            else:
                                print('Invalid move. Try again.')
                                selected_piece.update(board, fromSquare, fromSquare)
                                selected_piece.draw(board)
                                selected_piece = None
                        
            pg.display.update()
    pg.quit()

def castle(square_of_interest, selected_piece, fromSquare, team_alternator, castling, our_king, opponents_king, turn):
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
    our_king.first_move = False
    
    selected_piece = format_move(selected_piece, square_of_interest, fromSquare, team_alternator, castling, our_king, opponents_king, turn)
    return next(team_alternator), selected_piece


# Deals with printing the move to the screen and updating piece information after every move.
def format_move(selected_piece, square_of_interest, fromSquare, team_alternator, castling, our_king, opponents_king, turn):
    

    # Check for checkmate
    our_pieces = None
    opponents_pieces = None
    if turn == 'white':
        our_pieces = white_pieces
        opponents_pieces = black_pieces
    else:
        our_pieces = black_pieces
        opponents_pieces = white_pieces

    # If the selected piece is about to capture an opponent's piece, then that piece must be removed from pieces.
    # Also need to update the checking variables here, since otherwise they won't get updated afterwards.
    if square_of_interest and square_of_interest.occupied_colour != selected_piece.colour:
        print('definitely should be getting here')
        for piece in opponents_pieces:
            if piece.curSquare == square_of_interest:
                print('also should probs be getting here...')
                if piece == our_king.checking_piece:
                    print('HERHEREREEEEEEEEEEEEEEEEEEEE')
                    our_king.our_king_in_check(piece, our_king)
                print(f'Removing {piece.name}')
                pieces.remove(piece)
                opponents_pieces.remove(piece)
                break
    
    pg.draw.rect(board, square_of_interest.colour, (square_of_interest.x, square_of_interest.y, 100, 100))
    selected_piece.update(board, fromSquare, square_of_interest)
    selected_piece.draw(board)
    print(f'{selected_piece.colour} {selected_piece.name} released. Its curSquare is {selected_piece.curSquare.id}\n')
    print()

    # Update the legal moves for every piece on the board now.
    # After the move is made, we need to update the available moves for every piece on the board (I think).
    for piece in pieces:
        if piece.name == 'Pawn' and piece == selected_piece:
            piece.first_move = False
            piece.taking_squares = []

            # If the selected pawn is promoting, then we need to remove that pawn from the list of pieces, as well as the set of pieces in which it lies.
            # Then we need to add the desired promoted-to piece to pieces, as well as the set of pieces to which it belongs.
            if check_promotion(piece):
                print('YO WE BOUTTA LEVEL THE HECK UP!!!')
                
                # Run promotion box as a subprocess.
                new_piece_name = subprocess.check_output(["python3", "promotion_box.py", f"{selected_piece.colour}"]).strip().decode('ascii')

                # Remove the selected pawn from the sets it belongs to.
                pg.draw.rect(board, selected_piece.curSquare.colour, (selected_piece.curSquare.x, selected_piece.curSquare.y, 100, 100))
                pieces.remove(selected_piece)

                if piece.colour == 'white':
                    white_pieces.remove(selected_piece)
                else:
                    black_pieces.remove(selected_piece)

                # Add the promoted piece to our set of pieces.
                if new_piece_name == 'Queen':
                    selected_piece = queen.Queen(selected_piece.curSquare, selected_piece.colour)

                elif new_piece_name == 'Rook':
                    selected_piece = rook.Rook(selected_piece.curSquare, selected_piece.colour)

                elif new_piece_name == 'Bishop':
                    selected_piece = bishop.Bishop(selected_piece.curSquare, selected_piece.colour)

                elif new_piece_name == 'Knight':
                    selected_piece = knight.Knight(selected_piece.curSquare, selected_piece.colour)
                
                our_pieces.add(selected_piece)
                pieces.add(selected_piece)

                # Draw in the new piece and continue.
                selected_piece.update(board, fromSquare, square_of_interest)
                selected_piece.draw(board)
                selected_piece.get_legal_moves(squares, pieces, selected_piece, our_king)
                break

        piece.get_legal_moves(squares, pieces, selected_piece, our_king)
    

    # Check if the move just made delivered a check to the opponent's king. If it did, then set up the appropriate checking variables.
    if opponent_in_check(opponents_king, turn):
        print(f'Opponents {opponents_king.checking_piece.name} on {opponents_king.checking_piece.curSquare.id} is checking you!')
        print('CHECK!')

        # Determine the details of how the opponent's king is in check.
        opponents_king.how_in_check(opponents_king)

        # Update the legal moves for every piece on the board now.
        # After the move is made, we need to update the available moves for every piece on the board (I think).
        for piece in pieces:
            piece.get_legal_moves(squares, pieces, selected_piece, opponents_king)

    else:
        # Update the legal moves for every piece on the board now.
        # After the move is made, we need to update the available moves for every piece on the board (I think).
        for piece in pieces:
            piece.get_legal_moves(squares, pieces, selected_piece, opponents_king)

    print(f'Now its available moves are {[square.id for square in selected_piece.legal_moves]}')
    print(f'{selected_piece.name} moved from {fromSquare.id} to {square_of_interest.id}.  Its new square is {selected_piece.curSquare.id}\n')

    # Note. TODO: Will need to keep track of how many pieces are left on each team throughout the game, since this depends on that.
    num_piece_with_zero_moves = 0
    if opponents_king.in_check:
        for piece in opponents_pieces:
            if piece.name == 'Pawn':
                if len(piece.taking_squares) == 0 or len(piece.legal_moves) == 0:
                    num_piece_with_zero_moves += 1
                #print(num_piece_with_zero_moves)
                else:
                    if len(piece.legal_moves) != 0:
                        print(f'Our {piece.name} on {piece.curSquare.id} can move to {[square.id for square in piece.legal_moves]} to get you out of check!')

            else:
                if len(piece.legal_moves) != 0:
                    print(f'Our {piece.name} on {piece.curSquare.id} can move to {[square.id for square in piece.legal_moves]} to get you out of check!')

                else:
                    num_piece_with_zero_moves += 1
                #break
        if num_piece_with_zero_moves == len(opponents_pieces):
            print('CHECKMATE!!!')

    print('\n----------------------\n')

    selected_piece = None   

    if castling:
        return selected_piece
    else:
        return next(team_alternator), selected_piece


# Returns true if a pawn is about to promote, false otherwise.
def check_promotion(selected_piece):
    if selected_piece.colour == 'white':
        if selected_piece.curSquare.rank == 8:
            return True
    else:
        if selected_piece.curSquare.rank == 1:
            return True


# Check if opponent's king is in check.  If it is, they can't make just any move. Determines how the king is in check.
def opponent_in_check(opponents_king, turn):
    for piece in pieces:
        if piece.colour == turn and piece.name != 'King': # TODO: NEED TO FIX THIS!!!
            # Checks if the opponent's king is being put in check by any of our pieces.
            if piece.name == 'Pawn':
                if opponents_king.curSquare in piece.taking_squares:
                    opponents_king.in_check = True
                    opponents_king.checking_piece = piece
                    opponents_king.list_of_checking_pieces.append((piece, piece.curSquare.id))
                    return True    
            else:
                if opponents_king.curSquare in piece.legal_moves:
                    opponents_king.in_check = True
                    opponents_king.checking_piece = piece

                    method_of_checking = piece.how_in_check(opponents_king)
                    opponents_king.list_of_checking_pieces.append((piece, piece.curSquare.id))
                    print(f'added {piece.name} on {piece.curSquare.id} to the opponents list of checking pieces.')
                    return True
    return False

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

# Toggles between the two kings
def alternate_kings(white_king, black_king):
    while True:
        yield white_king
        yield black_king

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
    white_king = None
    black_king = None
    
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

        pieces.add(piece)

        
        # While we are here, set square.isOccupied to be True, since when square objects are created, these are set to be False.
        square.isOccupied = True
        square.occupied_colour = colour

        board.blit(piece.image, piece.rect)
        pg.display.update()  
    
    # Add pieces to appropriate groups
    for piece in pieces:
        if piece.colour == 'white':
            white_pieces.add(piece)
        else:
            black_pieces.add(piece)

    # We need to get the legal moves for each piece on startup, since if a king is selected to move
    # we need to check that no opponent's piece is controlling a given surrounding square of that king.
    # But since knights can move before every other piece has been moved, we account for that by getting every piece's available moves right away.
    for piece in pieces:
        
        # Get the legal moves for the current piece.
        if piece.name == 'King':
            piece.get_legal_moves(squares, pieces, None, None)
            if piece.colour == 'white':
                white_king = piece
            else:
                black_king = piece
            #print(f'{piece.colour} {piece.name} has these moves available to it {piece.get_legal_moves(squares, pieces)}')
        else:
            piece.get_legal_moves(squares, pieces, None, None)
        
        # Update pawn attribute.
        if piece.name == 'Pawn':
            piece.first_move = True
        #print(f'{piece.colour} {piece.name} has these moves available to it {piece.get_legal_moves(squares)}')


        # Now get each piece's king and its opponent's king.
        for k in [piece for piece in pieces if piece.name == 'King']:
            if piece.colour == k.colour:
                piece.our_king = k
            else:
                piece.opponents_king = k
    
    return white_king, black_king
    #return white_king, black_king

if __name__ == "__main__":
    main() 