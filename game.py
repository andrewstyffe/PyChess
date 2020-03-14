import pygame as pg
from pygame.locals import QUIT, KEYUP, K_ESCAPE, Rect
from pygame.draw import rect
import signal
from chess_pieces import *
import subprocess
import square
import king
import queen
import rook
import bishop
import knight
import pawn
import network
import board

our_king = None
opponents_king = None

files_dict = {'A' : 8, 'B' : 7, 'C' : 6, 'D' : 5, 'E' : 4, 'F' : 3, 'G' : 2, 'H' : 1}

class Player():

    def __init__(self, selected_piece, colour):

        self.selected_piece = selected_piece
        self.colour = colour
        self.board = board.Board(800, 800, f"Chessboard for {self.colour} player")
        self.has_moved = False
        self.turn = 'white'
        if self.colour == 'white':
            self.pieces = self.board.white_pieces
        else:
            self.pieces = self.board.black_pieces

    def draw(self, g):
        pg.draw.rect(g, self.fromSquare.colour, (self.fromSquare.x, self.fromSquare.y, 100, 100), 0)

    def move(self, board, selected_piece):
        if selected_piece:
            selected_piece.update(board, selected_piece.fromSquare, selected_piece.curSquare)

class TimeoutError(Exception):
    pass

class Game:


    def __init__(self):
        self.net = network.Network()

        # The main player of the current Game object is the player that is making moves on that board.
        # The other player will simply be viewing the moves that are made on its own board.
        self.main_player = Player(None, f'{self.net.id.decode()}')

    # Toggles between the two teams 
    def alternate_teams(self):
        while True:
            yield 'black'
            yield 'white'

    # Toggles between the two kings
    def alternate_kings(self, white_king, black_king):
        while True:
            yield white_king
            yield black_king

    def send_data(self, chess_move):
        self.net.send(chess_move)


    def timeout_handler(self, signum, frame):
        raise TimeoutError()

    def parse_data(self, data):
        turn = data.split()[2]
        piece_taken = data.split()[3]
        fromSquare = data.split()[1].split("-")[0]
        toSquare = data.split()[1].split("-")[1]
        return turn, self.get_square(fromSquare, self.main_player.board.squares), self.get_square(toSquare, self.main_player.board.squares), piece_taken

    def run(self):


        # Change the behavior of SIGALRM
        team_alternator = self.alternate_teams()
        selected_piece = None
        move_made = False
        turn = self.main_player.turn

        our_pieces = [piece for piece in self.main_player.board.pieces if piece.colour == self.main_player.colour]
        opponents_pieces = [piece for piece in self.main_player.board.pieces if piece not in our_pieces]
        our_king = [piece for piece in our_pieces if piece.name == 'King' and piece.colour == self.main_player.colour][0]
        opponents_king = [piece for piece in self.main_player.board.pieces if piece.name == 'King' and piece.colour != self.main_player.colour][0]

        done = False
        while not done:

            chess_move = None
            opponents_move = None
            
            # Get our piece sets, and our kings.
            our_pieces = [piece for piece in self.main_player.board.pieces if piece.colour == self.main_player.colour]
            opponents_pieces = [piece for piece in self.main_player.board.pieces if piece not in our_pieces]
            our_king = [piece for piece in our_pieces if piece.name == 'King' and piece.colour == self.main_player.colour][0]
            opponents_king = [piece for piece in self.main_player.board.pieces if piece.name == 'King' and piece.colour != self.main_player.colour][0]
    
            # Get events
            for event in pg.event.get():

                # Keep the board live until the game window is exited
                if event.type == pg.QUIT: 
                    done = True
                
                move_to_square = None
                if self.main_player.colour == turn:
                    # Get the current mouse event
                   
                    if event.type == pg.MOUSEBUTTONDOWN:
                        
                        # Get current mouse position and check pieces against that position
                        mouse_down_position = pg.mouse.get_pos()

                        castling = False
                        castling_kingside = False
                        castling_queenside = False
                        
                        # Find and move the selected piece
                        for piece in our_pieces:
                            if piece.rect.collidepoint(mouse_down_position) and piece.colour == turn:

                                # Selected piece found - get its data
                                selected_piece = piece
                                fromSquare = selected_piece.curSquare
                                selected_piece.fromSquare = fromSquare

                                # Get the legal moves of every piece on the board before the selected piece has moved.
                                print(f'{selected_piece.colour} {selected_piece.name} selected. Its curSquare is {selected_piece.curSquare.id}')
                                for piece in self.main_player.board.pieces:
                                    if piece.name != 'King':
                                        piece.get_legal_moves(self.main_player.board.squares, self.main_player.board.pieces, selected_piece, our_king)
                                    else:
                                        piece.get_legal_moves(self.main_player.board.squares, self.main_player.board.pieces, selected_piece, our_king)

                                # Get the legal moves of the selected piece.
                                print(f'The selected piece"s available moves are {[square.id for square in selected_piece.legal_moves]}')

                                # 'Erase' the old position of the selected piece, by drawing over it the original square
                                pg.draw.rect(self.main_player.board.screen, fromSquare.colour, (fromSquare.x, fromSquare.y, 100, 100))
                                selected_piece.drag(board, mouse_down_position)
                                break
                                

                    # If we are done dragging, get the square we moved to
                    elif event.type == pg.MOUSEBUTTONUP:
                        up_mouse_position = pg.mouse.get_pos()
                        for square_of_interest in self.main_player.board.squares:
                            if square_of_interest.coords.collidepoint(up_mouse_position) and selected_piece:

                                # Deals with castling
                                if selected_piece.name == 'King':

                                    # If the selected square represents a legal move for the selected king.
                                    if square_of_interest in selected_piece.legal_moves and square_of_interest.id != selected_piece.curSquare.id:

                                        # The case where the selected king is castling.
                                        if files_dict[selected_piece.curSquare.file] == files_dict[square_of_interest.file] + 2 or files_dict[selected_piece.curSquare.file] == files_dict[square_of_interest.file] - 2:
                                            castling = True
                                            selected_piece, chess_move, square_of_interest = self.castle(self.main_player.board.screen, square_of_interest, selected_piece, fromSquare, castling, our_king, opponents_king, our_pieces, opponents_pieces, turn)
                                            move_to_square = square_of_interest
                                        # The case where the selected king is making a non-castling move.
                                        else:
                                            selected_piece, chess_move, square_of_interest = self.format_move(self.main_player.board.screen, selected_piece, square_of_interest, fromSquare, castling, castling_kingside, castling_queenside, our_king, opponents_king, our_pieces, opponents_pieces, turn)
                                            move_to_square = square_of_interest
                                    # If the square we clicked on isn't a legal move for the selected king, then put the king back to its starting square.
                                    else:
                                        print('Invalid move. Try again.')
                                        selected_piece.update(self.main_player.board.screen, fromSquare, fromSquare)

                                        if selected_piece.first_move:
                                            selected_piece.first_move = True
                                        selected_piece.draw(self.main_player.board.screen)
                                        selected_piece = None
                                
                                # For every piece that is not a king.
                                else:
                                    
                                    # If the square of interest represents a legal move for the selected piece.
                                    if square_of_interest in selected_piece.legal_moves:
                                        selected_piece, chess_move, square_of_interest = self.format_move(self.main_player.board.screen, selected_piece, square_of_interest, fromSquare, castling, castling_kingside, castling_queenside, our_king, opponents_king, our_pieces, opponents_pieces, turn)
                                        move_to_square = square_of_interest
                                    # If the square of interest represents an illegal move for the selected piece, then return that piece to its fromSquare.
                                    else:
                                        print('Invalid move. Try again.')
                                        selected_piece.update(self.main_player.board.screen, fromSquare, fromSquare)
                                        selected_piece.draw(self.main_player.board.screen)
                                        selected_piece = None
                    if chess_move:
                        self.main_player.has_moved = True
                
                elif self.main_player.colour != turn:

                    # Player whose turn it isn't hangs here until their opponent has made a move.
                    while opponents_move is None:
                        
                        opponents_move = self.net.client.recv(2048).decode()
                
                        # Non-castling moves. Update the board of the player whose turn it isn't.
                        if opponents_move.split()[0] != 'O-O' and opponents_move.split()[0] != 'O-O-O':
                            turn, fromSquare, newSquare, piece_taken = self.parse_data(opponents_move)

                            # Check if one of our pieces was taken.
                            # print(newSquare.id)
                            # testing_square = None
                            # for square in self.main_player.board.squares:
                            #     if square.piece_taken:
                            #         print('yet' + square.id)
                            #         testing_square = square
                            #         break
                            if piece_taken == 'True':
                                pg.draw.rect(self.main_player.board.screen, newSquare.colour, (newSquare.x, newSquare.y, 100, 100))

                            for piece in opponents_pieces:
                                if piece.curSquare == fromSquare:
                                    pg.draw.rect(self.main_player.board.screen, piece.curSquare.colour, (piece.curSquare.x, piece.curSquare.y, 100, 100))
                                    piece.update(self.main_player.board.screen, fromSquare, newSquare)
                                    piece.draw(self.main_player.board.screen)
                                    break

                        elif opponents_move.split()[0] == 'O-O':
                            turn = opponents_move.split()[1]

                            # If we are white, then other player is black.  Castling kingside then implies which rook moved.
                            if self.main_player.colour == 'white':
                                # Update the board of the person whose turn it isn't.
                                # Update the king.
                                for piece in opponents_pieces:
                                    if piece.name == 'King':
                                        pg.draw.rect(self.main_player.board.screen, piece.curSquare.colour, (piece.curSquare.x, piece.curSquare.y, 100, 100))
                                        piece.update(self.main_player.board.screen, piece.curSquare, self.get_square('G8', self.main_player.board.squares))
                                        piece.draw(self.main_player.board.screen)
                                        break
                                
                                # Update the rook.
                                for piece in opponents_pieces:
                                    if piece.curSquare.id == 'H8':
                                        print(len(self.main_player.board.squares))
                                        pg.draw.rect(self.main_player.board.screen, piece.curSquare.colour, (piece.curSquare.x, piece.curSquare.y, 100, 100))
                                        piece.update(self.main_player.board.screen, piece.curSquare, self.get_square('F8', self.main_player.board.squares))
                                        piece.draw(self.main_player.board.screen)
                                        break

                            # If we are black, then other player is white.  Castling kingside then implies which rook moved.
                            else:
                                # Update the king.
                                for piece in opponents_pieces:
                                    if piece.name == 'King':
                                        pg.draw.rect(self.main_player.board.screen, piece.curSquare.colour, (piece.curSquare.x, piece.curSquare.y, 100, 100))
                                        piece.update(self.main_player.board.screen, piece.curSquare, self.get_square('G1', self.main_player.board.squares))
                                        piece.draw(self.main_player.board.screen)
                                        break
                                
                                # Update the rook.
                                for piece in opponents_pieces:
                                    if piece.curSquare.id == 'H1':
                                        pg.draw.rect(self.main_player.board.screen, piece.curSquare.colour, (piece.curSquare.x, piece.curSquare.y, 100, 100))
                                        piece.update(self.main_player.board.screen, piece.curSquare, self.get_square('F1', self.main_player.board.squares))
                                        piece.draw(self.main_player.board.screen)
                                        break

                        elif opponents_move.split()[0] == 'O-O-O':
                            turn = opponents_move.split()[1]

                            # If we are white, then other player is black.  Castling kingside then implies which rook moved.
                            if self.main_player.colour == 'white':
                                # Update the board of the person whose turn it isn't.
                                # Update the king.
                                for piece in opponents_pieces:
                                    if piece.name == 'King':
                                        pg.draw.rect(self.main_player.board.screen, piece.curSquare.colour, (piece.curSquare.x, piece.curSquare.y, 100, 100))
                                        piece.update(self.main_player.board.screen, piece.curSquare, self.get_square('C8', self.main_player.board.squares))
                                        piece.draw(self.main_player.board.screen)
                                        break
                                
                                # Update the rook.
                                for piece in opponents_pieces:
                                    if piece.curSquare.id == 'A8':
                                        pg.draw.rect(self.main_player.board.screen, piece.curSquare.colour, (piece.curSquare.x, piece.curSquare.y, 100, 100))
                                        piece.update(self.main_player.board.screen, piece.curSquare, self.get_square('D8', self.main_player.board.squares))
                                        piece.draw(self.main_player.board.screen)
                                        break

                            # If we are black, then other player is white.  Castling kingside then implies which rook moved.
                            else:
                                # Update the king.
                                for piece in opponents_pieces:
                                    if piece.name == 'King':
                                        pg.draw.rect(self.main_player.board.screen, piece.curSquare.colour, (piece.curSquare.x, piece.curSquare.y, 100, 100))
                                        piece.update(self.main_player.board.screen, piece.curSquare, self.get_square('C1', self.main_player.board.squares))
                                        piece.draw(self.main_player.board.screen)
                                        break
                                
                                # Update the rook.
                                for piece in opponents_pieces:
                                    if piece.curSquare.id == 'A1':
                                        pg.draw.rect(self.main_player.board.screen, piece.curSquare.colour, (piece.curSquare.x, piece.curSquare.y, 100, 100))
                                        piece.update(self.main_player.board.screen, piece.curSquare, self.get_square('D1', self.main_player.board.squares))
                                        piece.draw(self.main_player.board.screen)
                                        break

            if self.main_player.has_moved and turn == self.main_player.colour:
                if turn == 'white':
                    turn = 'black'
                else:
                    turn = 'white'
                print(f'Updated the turn.  Now it is {turn}s turn.')
                
                info = chess_move + " " + turn + " " + str(move_to_square.piece_taken)
                self.net.client.send(str.encode(info))
                self.main_player.has_moved = False

            pg.display.update()
    pg.quit()

    # Returns the square object with the given square id.
    def get_square(self, square_of_interest, squares):
        for square in squares:
            if square.id == square_of_interest:
                return square

    def castle(self, board, square_of_interest, selected_piece, fromSquare, castling, our_king, opponents_king, our_pieces, opponents_pieces, turn):
        # Get the rook whose current square is rook_fromSquare
        rook_of_interest = None
        castling_kingside = False
        castling_queenside = False

        for rook in [piece for piece in self.main_player.board.pieces if piece.name == 'Rook']:
            if square_of_interest.id == 'G1':
                if rook.curSquare.id == 'H1':
                    rook_of_interest = rook
                    castling_kingside = True
            elif square_of_interest.id == 'C1':
                if rook.curSquare.id == 'A1':
                    rook_of_interest = rook
                    castling_queenside = True
            elif square_of_interest.id == 'G8':
                if rook.curSquare.id == 'H8':
                    rook_of_interest = rook
                    castling_kingside = True
            elif square_of_interest.id == 'C8':
                if rook.curSquare.id == 'A8':
                    rook_of_interest = rook
                    castling_queenside = True

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
        rook_of_interest.update(board, rook_of_interest.curSquare, selected_piece.get_square(f'{new_file}{square_of_interest.rank}', self.main_player.board.squares))
        rook_of_interest.draw(board)
        our_king.first_move = False
        
        selected_piece, chess_move, square_of_interest = self.format_move(self.main_player.board.screen, selected_piece, square_of_interest, fromSquare, castling, castling_kingside, castling_queenside, our_king, opponents_king, our_pieces, opponents_pieces, turn)
        return selected_piece, chess_move, square_of_interest


    # Deals with printing the move to the screen and updating piece information after every move.
    def format_move(self, board, selected_piece, square_of_interest, fromSquare, castling, castling_kingside, castling_queenside, our_king, opponents_king, our_pieces, opponents_pieces, turn):

        # If the selected piece is about to capture an opponent's piece, then that piece must be removed from pieces.
        # Also need to update the checking variables here, since otherwise they won't get updated afterwards.
        if square_of_interest and square_of_interest.occupied_colour != selected_piece.colour:
            for piece in opponents_pieces:
                if piece.curSquare == square_of_interest:
                    if piece == our_king.checking_piece:
                        our_king.our_king_in_check(piece, our_king)
                    print('Hello' + square_of_interest.id)
                    square_of_interest.piece_taken = True
                    self.main_player.board.pieces.remove(piece)
                    opponents_pieces.remove(piece)
                    break
        
        # Update the main player's board.
        pg.draw.rect(self.main_player.board.screen, square_of_interest.colour, (square_of_interest.x, square_of_interest.y, 100, 100))
        selected_piece.update(board, fromSquare, square_of_interest)
        selected_piece.draw(self.main_player.board.screen)
        
        print(f'{selected_piece.colour} {selected_piece.name} released. Its curSquare is {selected_piece.curSquare.id}\n')
        print()

        # Update the legal moves for every piece on the board now.
        # After the move is made, we need to update the available moves for every piece on the board (I think).
        for piece in self.main_player.board.pieces:
            if piece.name == 'Pawn' and piece == selected_piece:
                piece.first_move = False
                piece.taking_squares = []

                # If the selected pawn is promoting, then we need to remove that pawn from the list of pieces, as well as the set of pieces in which it lies.
                # Then we need to add the desired promoted-to piece to pieces, as well as the set of pieces to which it belongs.
                if self.check_promotion(piece):
                    
                    # Run promotion box as a subprocess.
                    new_piece_name = subprocess.check_output(["python3", "promotion_box.py", f"{selected_piece.colour}"]).strip().decode('ascii')

                    # Remove the selected pawn from the sets it belongs to.
                    pg.draw.rect(board, selected_piece.curSquare.colour, (selected_piece.curSquare.x, selected_piece.curSquare.y, 100, 100))
                    self.main_player.board.pieces.remove(selected_piece)

                    if piece.colour == 'white':
                        self.main_player.board.white_pieces.remove(selected_piece)
                    else:
                        self.main_player.board.black_pieces.remove(selected_piece)

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
                    self.main_player.board.pieces.add(selected_piece)

                    # Draw in the new piece and continue.
                    selected_piece.update(board, fromSquare, square_of_interest)
                    selected_piece.draw(board)
                    selected_piece.get_legal_moves(self.main_player.board.squares, self.main_player.board.pieces, selected_piece, our_king)
                    break

            piece.get_legal_moves(self.main_player.board.squares, self.main_player.board.pieces, selected_piece, our_king)
        

        # Check if the move just made delivered a check to the opponent's king. If it did, then set up the appropriate checking variables.
        if self.opponent_in_check(opponents_king, turn):
            print(f'Opponents {opponents_king.checking_piece.name} on {opponents_king.checking_piece.curSquare.id} is checking you!')
            print('CHECK!')

            # Determine the details of how the opponent's king is in check.
            opponents_king.how_in_check(opponents_king)

            # Update the legal moves for every piece on the board now.
            # After the move is made, we need to update the available moves for every piece on the board (I think).
            for piece in self.main_player.board.pieces:
                piece.get_legal_moves(self.main_player.board.squares, self.main_player.board.pieces, selected_piece, opponents_king)

        else:
            # Update the legal moves for every piece on the board now.
            # After the move is made, we need to update the available moves for every piece on the board (I think).
            for piece in self.main_player.board.pieces:
                piece.get_legal_moves(self.main_player.board.squares, self.main_player.board.pieces, selected_piece, opponents_king)

        print(f'Now its available moves are {[square.id for square in selected_piece.legal_moves]}')
        print(f'{selected_piece.name} moved from {fromSquare.id} to {square_of_interest.id}.  Its new square is {selected_piece.curSquare.id}\n')

        if castling_kingside:
            chess_move = 'O-O'
        elif castling_queenside:
            chess_move = 'O-O-O'
        else:   
            chess_move = f'{selected_piece.name} {fromSquare.id}-{selected_piece.curSquare.id}'

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

        return selected_piece, chess_move, square_of_interest

    # Returns true if a pawn is about to promote, false otherwise.
    def check_promotion(self, selected_piece):
        if selected_piece.colour == 'white':
            if selected_piece.curSquare.rank == 8:
                return True
        else:
            if selected_piece.curSquare.rank == 1:
                return True


    # Check if opponent's king is in check.  If it is, they can't make just any move. Determines how the king is in check.
    def opponent_in_check(self, opponents_king, turn):
        for piece in self.main_player.board.pieces:
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