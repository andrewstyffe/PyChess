import pygame as pg

# Composed this way so as to make sense in the is_blocked_rank method
files_dict = {'A' : 8, 'B' : 7, 'C' : 6, 'D' : 5, 'E' : 4, 'F' : 3, 'G' : 2, 'H' : 1}

# Describes the various attributes of a rook and enforces the rules of a rook on the object
class Rook(pg.sprite.Sprite):
    def __init__(self, square, colour):
        super(Rook, self).__init__()
        self.clicked = False
        self.name = 'Rook'

        self.colour = colour
        self.curSquare = square
        self.legal_moves = []

        # Assigns a picture to the rook
        if self.colour == 'white':
            self.image = pg.image.load("./white_rook.png")
        else:
            self.image = pg.image.load("./black_rook.png")
        
        self.image = pg.transform.scale(self.image, (50, 50))
        self.rect = self.image.get_rect(center = self.curSquare.center)

    # Move pawn image with the cursor
    def drag(self, board, cursor):
        self.rect = self.rect.move(cursor[0], cursor[1])

    # Draw the piece in the correct position on the correct square
    def draw(self, surface):
        surface.blit(self.image, self.rect.topleft)

    # Deals with maintaining piece attributes to ensure continuity amongst pieces
    def update(self, board, fromSquare, newSquare):
        self.curSquare = newSquare
        self.rect.center = newSquare.center
        self.fromSquare = fromSquare

        newSquare.isOccupied = True
        fromSquare.isOccupied = False
        newSquare.occupied_colour = self.colour

    # Returns true if a given square is in the same file as our current square, false otherwise
    def is_same_file(self, square_id):
        return square_id[0] == self.curSquare.file

    # Returns true if a given square is in the same rank as our current square, false otherwise
    def is_same_rank(self, square_id):
        return square_id[1] == self.curSquare.rank

    # Returns a sorted list of squares in the same file as the selected piece
    def get_file_squares(self, squares):
        file_squares = []

        for square in squares:
            if self.is_same_file(square.id):
                file_squares.append(square)

        # Sort the squares.  e.g. file_squares = ['A1', 'A2', 'A3', ... , 'A8']
        file_squares.sort(key = lambda x: x.id)
    
        return file_squares

    # Returns a sorted list of squares in the same rank as the selected piece
    def get_rank_squares(self, squares):
        rank_squares = []

        for square in squares:
            if self.is_same_rank(square.id):
                rank_squares.append(square)

        # Sort the squares.  e.g. file_squares = ['A2', 'B2', 'C2', ... , 'H2']
        rank_squares.sort(key = lambda x: x.id)
    
        return rank_squares

    # Returns the corresponding square to a given square_id
    def get_square(self, square_id, squares):
        for square in squares:
            if square.id == square_id:
                return square

    # Determines if the path along a file from the selected rook to the square_of_interest is being blocked by some piece.
    # Returns true if it is, false otherwise.
    def is_blocked_file(self, file_squares, square_of_interest, squares):

        next_piece_above_on_file = ''
        next_piece_below_on_file = ''

        reversed_file_squares = file_squares[::-1]

        # For white
        if self.colour == 'white':

            # Gets the first occupied square that occurs below the selected piece on the same file.  Works since file_squares is sorted.
            for square in file_squares:
                if square.isOccupied and square.rank < self.curSquare.rank:
                    next_piece_below_on_file = square.id
            
            # Gets the first occupied square that occurs below the selected piece on the same file.  Works since file_squares is sorted.
            for square in reversed_file_squares:
                if square.isOccupied and square.rank > self.curSquare.rank:
                    next_piece_above_on_file = square.id
        
        # For black
        else:

            # Gets the first occupied square that occurs below the selected piece on the same file.  Works since file_squares is sorted.
            for square in reversed_file_squares:
                if square.isOccupied and square.rank < self.curSquare.rank:
                    next_piece_below_on_file = square.id
            
            # Gets the first occupied square that occurs below the selected piece on the same file.  Works since file_squares is sorted.
            for square in file_squares:
                if square.isOccupied and square.rank > self.curSquare.rank:
                    next_piece_above_on_file = square.id
                    
        # If the selected piece is the only piece on its file and its rank, then there are no limitations to where it can move, so return false.
        if next_piece_below_on_file == '' and next_piece_above_on_file == '':
            return False

        # If there is no piece below us, then we can move to whatever squares lie below us.
        elif next_piece_below_on_file == '':    
            if self.colour == 'white':
                if int(square_of_interest.rank) < int(next_piece_above_on_file[1]):
                    return False

        # If there is no piece above us, then we can move to whatever squares lie above us.
        elif next_piece_above_on_file == '':
            if int(square_of_interest.rank) > int(next_piece_below_on_file[1]):
                return False

        # If there are pieces above and below us...
        else:
            
            if self.colour == 'white':
                
                # As long as the selected piece lies between the next_piece_below_on_file and the next_piece_above_on_file, 
                # and the square_of_interest is on a higher rank than the next_piece_below_on_file, we can move to those squares
                if int(next_piece_below_on_file[1]) <= int(self.curSquare.rank) <= int(next_piece_above_on_file[1]) and int(square_of_interest.rank) <= int(next_piece_above_on_file[1]):
                    if int(square_of_interest.rank) > int(next_piece_below_on_file[1]):
                        
                        # If the next piece below the selected piece isn't the same colour, then the selected piece can move to that square.
                        if self.get_square(next_piece_below_on_file, squares).occupied_colour != self.colour:
                            return False

                        # If the next piece above the selected piece isn't the same colour, then the selected piece can move to that square.
                        elif self.get_square(next_piece_above_on_file, squares).occupied_colour != self.colour:
                            return False
            else:
                if int(next_piece_below_on_file[1]) <= int(self.curSquare.rank) <= int(next_piece_above_on_file[1]) and int(square_of_interest.rank) < int(next_piece_above_on_file[1]):
                    if int(square_of_interest.rank) >= int(next_piece_below_on_file[1]):

                        # If the next piece above the selected piece isn't the same colour, then the selected piece can move to that square.
                        if self.get_square(next_piece_above_on_file, squares).occupied_colour != self.colour:
                            return False

                        elif self.get_square(next_piece_below_on_file, squares).occupied_colour != self.colour:
                            return False



        # If all these cases fail, then we cannot move to the square of interest, so return true.
        return True

    # Determines if the path along a rank from the selected rook to the square_of_interest is being blocked by some piece.
    # Returns true if it is, false otherwise.
    def is_blocked_rank(self, rank_squares, square_of_interest, squares):
        
        # First occupied, meaning the leftmost occupied square, and last_occupied, meaning the rightmost occupied square.
        next_piece_left_on_rank = ''
        next_piece_right_on_rank = ''

        reversed_rank_squares = rank_squares[::-1]

        # Gets the closest occupied square to the left of the selected piece.
        for square in rank_squares:
            if square.isOccupied and files_dict[square.file] > files_dict[self.curSquare.file]:
                next_piece_left_on_rank = square.id

        # Gets the closest occupied square to the right of the selected piece.
        for square in reversed_rank_squares:
            if square.isOccupied and files_dict[square.file] < files_dict[self.curSquare.file]:
                next_piece_right_on_rank = square.id


        # If there is no piece left or right of the selected piece, then there are no squares off limits, return false.
        if next_piece_left_on_rank == '' and next_piece_right_on_rank == '':
            return False

        
        # Remove those squares that lie to the right of the next_piece_right_on_rank.
        if next_piece_right_on_rank and files_dict[square_of_interest.file] < files_dict[next_piece_right_on_rank[0]]:
            print(f'Square of interest {square_of_interest.id}')
            return True

        # Remove those squares that lie to the left of the next_piece_left_on_rank.
        if next_piece_left_on_rank and files_dict[square_of_interest.file] > files_dict[next_piece_left_on_rank[0]]:
            print(f'Square of interest {square_of_interest.id}')
            return True
        
        # If none of these options applied to a square, then we can move to that square.
        return False


    # Gets legal moves available for a given rook.
    def get_legal_moves(self, squares):

        # Get the squares in the same file, and rank as our selected piece
        file_squares = self.get_file_squares(squares)
        rank_squares = self.get_rank_squares(squares)

        # For the black pieces, reverse the list, so that the first_occupied_square_on_file is found from black's perspective
        if self.colour == 'black':
            file_squares.reverse()

        # Start by adding every square to legal_moves, then remove those squares that are illegal
        for square in squares:
            if square not in self.legal_moves:
                self.legal_moves.append(square)
        
        # Now remove the illegal squares.
        # Important to iterate through sqaures and not self.legal_moves since legal_moves changes during each iteration of the loop.
        for square in squares:

            # If the square of interest is occupied by one of our own pieces, then we cannot move there.
            if square.isOccupied and square.occupied_colour == self.colour:
                self.legal_moves.remove(square)

            # If the square of interest is not in the same file and it is not in the same rank, then we cannot move there.
            if not self.is_same_file(square.id) and not self.is_same_rank(square.id) and square in self.legal_moves:
                self.legal_moves.remove(square)

            # If the square of interest is in the same file as the selected rook, but there is no path from the rook to that square.
            # I.e. There is a piece inbetween the rook and that square, then we cannot move there.
            if self.is_blocked_file(file_squares, square, squares) and square in self.legal_moves:
                self.legal_moves.remove(square)

            # If the square of interest is in the same rank as the selected rook, but there is no path from the rook to that square.
            # I.e. There is a piece inbetween the rook and that square, then we cannot move there.
            if self.is_blocked_rank(rank_squares, square, squares) and square in self.legal_moves:
                self.legal_moves.remove(square)

        # Lastly, if the current square of the selected rook is in legal_moves, then we cannot move there.
        if self.curSquare in self.legal_moves:
            self.legal_moves.remove(self.curSquare)  

        # Sort self.legal_moves for readability
        sorted_legal_moves = [square.id for square in self.legal_moves]
        sorted_legal_moves.sort()
        return sorted_legal_moves