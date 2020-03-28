import pygame as pg
import square

# List of all diagonals and the squares they contain, written from white's perspective
pos_diag_a1 = ['A1', 'B2', 'C3', 'D4', 'E5', 'F6', 'G7', 'H8'] 
pos_diag_b1 = ['B1', 'C2', 'D3', 'E4', 'F5', 'G6', 'H7']
pos_diag_c1 = ['C1', 'D2', 'E3', 'F4', 'G5', 'H6']
pos_diag_d1 = ['D1', 'E2', 'F3', 'G4', 'H5']
pos_diag_e1 = ['E1', 'F2', 'G3', 'H4']
pos_diag_f1 = ['F1', 'G2', 'H3']
pos_diag_g1 = ['G1', 'H2']

pos_diag_a2 = ['A2', 'B3', 'C4', 'D5', 'E6', 'F7', 'G8']
pos_diag_a3 = ['A3', 'B4', 'C5', 'D6', 'E7', 'F8']
pos_diag_a4 = ['A4', 'B5', 'C6', 'D7', 'E8']
pos_diag_a5 = ['A5', 'B6', 'C7', 'D8']
pos_diag_a6 = ['A6', 'B7', 'C8']
pos_diag_a7 = ['A7', 'B8']

neg_diag_b1 = ['B1', 'A2']
neg_diag_c1 = ['C1', 'B2', 'A3']
neg_diag_d1 = ['D1', 'C2', 'B3', 'A4']
neg_diag_e1 = ['E1', 'D2', 'C3', 'B4', 'A5']
neg_diag_f1 = ['F1', 'E2', 'D3', 'C4', 'B5', 'A6']
neg_diag_g1 = ['G1', 'F2', 'E3', 'D4', 'C5', 'B6', 'A7']
neg_diag_h1 = ['H1', 'G2', 'F3', 'E4', 'D5', 'C6', 'B7', 'A8']

neg_diag_h2 = ['H2', 'G3', 'F4', 'E5', 'D6', 'C7', 'B8']
neg_diag_h3 = ['H3', 'G4', 'F5', 'E6', 'D7', 'C8']
neg_diag_h4 = ['H4', 'G5', 'F6', 'E7', 'D8']
neg_diag_h5 = ['H5', 'G6', 'F7', 'E8']
neg_diag_h6 = ['H6', 'G7', 'F8']
neg_diag_h7 = ['H7', 'G8']

# Yadayada
files_dict = {'A' : 8, 'B' : 7, 'C' : 6, 'D' : 5, 'E' : 4, 'F' : 3, 'G' : 2, 'H' : 1}
files = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H']

# Wrangling together this monstrous list of diagonals
pos_diagonals = [pos_diag_a1, pos_diag_b1, pos_diag_c1, pos_diag_d1, pos_diag_e1, pos_diag_f1, pos_diag_g1, pos_diag_a2, pos_diag_a3, pos_diag_a4, pos_diag_a5, pos_diag_a6, pos_diag_a7]
neg_diagonals = [neg_diag_b1, neg_diag_c1, neg_diag_d1, neg_diag_e1, neg_diag_f1, neg_diag_g1, neg_diag_h1, neg_diag_h2, neg_diag_h3, neg_diag_h4, neg_diag_h5, neg_diag_h6, neg_diag_h7]
diagonals = [pos_diagonals, neg_diagonals]

class ChessPiece(pg.sprite.Sprite):
    def __init__(self, board, square, colour):
        pg.sprite.Sprite.__init__(self)

        self.colour = colour
        self.curSquare = square
        self.fromSquare = None
        self.legal_moves = []
        self.legal_move_copy = []
        self.protected_squares = []
        self.our_king = None
        self.opponents_king = None

        self.pinned_along_diagonal = False
        self.pinned_along_file = False
        self.pinned_along_rank = False
        self.pinning_piece = None
    
    # Move pawn image with the cursor
    def drag(self, board, cursor):
        self.rect = self.rect.move(cursor[0], cursor[1])

    # Draw the piece in the correct position on the correct square
    def draw(self, surface):
        surface.blit(self.image, self.rect.topleft)

    # Deals with maintaining piece attributes to ensure continuity amongst pieces
    def update(self, board, fromSquare, newSquare):

        if fromSquare == newSquare:
            self.curSquare = fromSquare
            self.rect.center = fromSquare.center
            self.fromSquare = None
            fromSquare.isOccupied = True
            fromSquare.occupied_colour = self.colour
        
        else:
            self.curSquare = newSquare
            self.rect.center = newSquare.center
            self.fromSquare = fromSquare

            fromSquare.isOccupied = False
            newSquare.isOccupied = True
            newSquare.occupied_colour = self.colour
            fromSquare.occupied_colour = None

    
    # Returns a list of squares that are reachable from traveling along some diagonal starting from the square of interest. 
    def get_diagonal_squares(self, square_of_interest, squares):

        # Make sure to reset all of the square of interest's attributes so that duplicate entries aren't added.
        square_of_interest.pos_diagonal = []
        square_of_interest.neg_diagonal = []
        square_of_interest.diagonals = []
        square_of_interest.diagonal_ids = []

        # Get the squares that are on the positive diagonal that are reachable from our current square.
        for diagonal in pos_diagonals:

            # If the square of interest is in the current diagonal, then we have found the pos_diagonal for that square.
            # Add that diagonal to diagonal_squares and add each square object corresponding to the square ids in diagonal to pos_diagonal.
            if square_of_interest.id in diagonal:
                
                for square_id in diagonal:
                    square_of_interest.pos_diagonal.append(self.get_square(square_id, squares))

                break
        
        # Get the squares that are on the negative diagonal that are reachable from our current square.
        for diagonal in neg_diagonals:

            # If the square of interest is in the current diagonal, then we have found the pos_diagonal for that square.
            # Add that diagonal to diagonal_squares and add each square object corresponding to the square ids in diagonal to pos_diagonal.
            if square_of_interest.id in diagonal:

                for square_id in diagonal:
                    square_of_interest.neg_diagonal.append(self.get_square(square_id, squares))
                
                break

        square_of_interest.diagonals = square_of_interest.pos_diagonal + square_of_interest.neg_diagonal
        square_of_interest.diagonal_ids = [square.id for square in square_of_interest.diagonals]

    # Determines and returns the ids of the closest squares along the square of interest's diagonals that are occupied.
    def get_closest_occupied_diag(self, square_of_interest):

        # Identify the leftmost/rightmost squares on the selected bishop's positive/negative diagonals that are occupied.
        leftmost_pos_occupied = ''
        rightmost_pos_occupied = ''
        leftmost_neg_occupied = ''
        rightmost_neg_occupied = ''

        # Obtain reversed diagonal lists. 
        reversed_pos_diagonal = square_of_interest.pos_diagonal[::-1]
        reversed_neg_diagonal = square_of_interest.neg_diagonal[::-1]   

        # Determine the closest leftmost piece to the square of interest.
        for square in square_of_interest.pos_diagonal:
            if square.isOccupied and square.rank < square_of_interest.rank and square.id != square_of_interest.id:
                leftmost_pos_occupied = square.id

        # Determine the closest rightmost piece along the selected bishop's positive diagonal.
        for square in reversed_pos_diagonal:
            if square.isOccupied and square.rank > square_of_interest.rank and square.id != square_of_interest.id:
                rightmost_pos_occupied = square.id
        

        # Determine the closest leftmost piece along the selected bishop's negative diagonal.
        for square in reversed_neg_diagonal:
            if square.isOccupied and square.rank > square_of_interest.rank and square.id != square_of_interest.id:
                leftmost_neg_occupied = square.id

        # Determine the closest rightmost piece along the selected bishop's negative diagonal.
        for square in square_of_interest.neg_diagonal:
            if square.isOccupied and square.rank < square_of_interest.rank and square.id != square_of_interest.id:
                rightmost_neg_occupied = square.id

        return leftmost_pos_occupied, rightmost_pos_occupied, leftmost_neg_occupied, rightmost_neg_occupied
        
    # This method determines if the selected bishop can move to a particular square of interest that resides on one of its diagonals.
    # It returns true if the square of interest represents and ILLEGAL move, and false otherwise.
    # It does this by doing the following.
    # 1. It determines the closest occupied squares to the square of interest on both of its diagonals. 
    # 2. It tests against cases which would prohibit the selected bishop from moving to the square of interest.
    def is_blocked_diagonal(self, square_of_interest, squares):

        # # Get the squares on the same diagonal(s) as the square of interest
        # if square_of_interest.id != self.curSquare.id:
        #     self.get_diagonal_squares(square_of_interest)

        # Get the closest occupied squares to the square of interest.
        leftmost_pos_occupied, rightmost_pos_occupied, leftmost_neg_occupied, rightmost_neg_occupied = self.get_closest_occupied_diag(square_of_interest)
        
        # If there are no leftmost and no rightmost pieces along a given diagonal on which the selected bishop resides, 
        # then we can move to any of those squares.
        if leftmost_pos_occupied == '' and rightmost_pos_occupied == '' and self.curSquare in square_of_interest.pos_diagonal:
            return False
        if leftmost_neg_occupied == '' and rightmost_neg_occupied == '' and self.curSquare in square_of_interest.neg_diagonal:
            return False


        # This case tests when our selected bishop wants to move on its positive diagonal in the positive direction, i.e. the square of interest
        # has a larger rank than our current square.
        # If our current rank is smaller than the closest leftmost piece to the square of interest, then we cannot move to the square of interest.
        if leftmost_pos_occupied and self.curSquare.rank < int(leftmost_pos_occupied[1]) and self.curSquare in square_of_interest.pos_diagonal:
            return True
        
        # This case tests when our selected bishop wants to move on its positive diagonal in the negative direction, i.e. the square of interest
        # has a smaller rank than our current square.
        # If our current rank is larger than the closest rightmost piece to the square of interest, then we cannot move to the square of interest.
        if rightmost_pos_occupied and self.curSquare.rank > int(rightmost_pos_occupied[1]) and self.curSquare in square_of_interest.pos_diagonal:
            return True

        # This case tests when our selected bishop wants to move on its negative diagonal in the positive direction, i.e. the square of interest
        # has a smaller rank than our current square.
        # If our current rank is larger than the closest leftmost piece to the square of interest, then we cannot move to the square of interest.
        if leftmost_neg_occupied and self.curSquare.rank > int(leftmost_neg_occupied[1]) and self.curSquare in square_of_interest.neg_diagonal:
            return True

        # This case tests when our selected bishop wants to move on its negative diagonal in the negative direction, i.e. the square of interest
        # has a larger rank than our current square.
        # If our current rank is smaller than the closest rightmost piece to the square of interest, then we cannot move to the square of interest.
        if rightmost_neg_occupied and self.curSquare.rank < int(rightmost_neg_occupied[1]) and self.curSquare in square_of_interest.neg_diagonal:
            return True
        
        # If all of these cases are untrue, then we are able to move to the square of interest.
        return False


    # Get the files where the knight moves 2 squares horizontally first, and then one square vertically
    def horizontally_first(self, possible_squares, squares):
        new_file = ''
        new_rank = ''

        # Check squares 2 squares to the right 
        if files_dict[self.curSquare.file] + 2 in files_dict.values():
            for key, value in files_dict.items():
                if value == files_dict[self.curSquare.file] + 2:
                    new_file = key
        
                    # Now that we have the new file, get the new rank
                    # Check if a square exists one square up from where we are
                    if int(self.curSquare.rank) + 1 in range(1, 9):
                        new_rank = int(self.curSquare.rank) + 1
                        possible_squares.append(self.get_square(f'{new_file}{new_rank}', squares))

                    # Check if a square exists one square down from where we are
                    if int(self.curSquare.rank) - 1 in range(1, 9):
                        new_rank = int(self.curSquare.rank) - 1
                        possible_squares.append(self.get_square(f'{new_file}{new_rank}', squares))


        # Now check squares 2 squares to the left
        if files_dict[self.curSquare.file] - 2 in files_dict.values():
            for key, value in files_dict.items():
                if value == files_dict[self.curSquare.file] - 2:
                    new_file = key
                   
                    # Now that we have the new file, get the new rank
                    # Check if a square exists one up down from where we are
                    if int(self.curSquare.rank) + 1 in range(1, 9):
                        new_rank = int(self.curSquare.rank) + 1
                        possible_squares.append(self.get_square(f'{new_file}{new_rank}', squares))

                    # Check if a square exists one square down from where we are
                    if int(self.curSquare.rank) - 1 in range(1, 9):
                        new_rank = int(self.curSquare.rank) - 1
                        possible_squares.append(self.get_square(f'{new_file}{new_rank}', squares))

    # Get the files where the knight moves 2 squares vertically first, and then one square horizontally
    def vertically_first(self, possible_squares, squares):
        new_file = ''
        new_rank = ''

        # Check one square to the right
        if files_dict[self.curSquare.file] + 1 in files_dict.values():
            for key, value in files_dict.items():
                if value == files_dict[self.curSquare.file] + 1:
                    new_file = key
                    
                    # Now that we have the new file, get the new rank
                    # Check if a square exists 2 squares up
                    if int(self.curSquare.rank) + 2 in range(1, 9):
                        new_rank = int(self.curSquare.rank) + 2
                        possible_squares.append(self.get_square(f'{new_file}{new_rank}', squares))

                    # Check if a square exists 2 squares down from one square
                    if int(self.curSquare.rank) - 2 in range(1, 9):
                        new_rank = int(self.curSquare.rank) - 2
                        possible_squares.append(self.get_square(f'{new_file}{new_rank}', squares))
                    

        # Check one square to the left
        if files_dict[self.curSquare.file] - 1 in files_dict.values():
            for key, value in files_dict.items():
                if value == files_dict[self.curSquare.file] - 1:
                    new_file = key
                    
                    # Now that we have the new file, get the new rank
                    # Check if a square exists 2 squares up
                    if int(self.curSquare.rank) + 2 in range(1, 9):
                        new_rank = int(self.curSquare.rank) + 2
                        possible_squares.append(self.get_square(f'{new_file}{new_rank}', squares))

                    # Check if a square exists 2 squares down
                    if int(self.curSquare.rank) - 2 in range(1, 9):
                        new_rank = int(self.curSquare.rank) - 2
                        possible_squares.append(self.get_square(f'{new_file}{new_rank}', squares))

    
    # Returns the square object with the given square id.
    def get_square(self, square_of_interest, squares):
        for square in squares:
            if square.id == square_of_interest:
                return square


    # Gets the closest occupied squares on the same file as the selected rook.
    def get_closest_occupied_file(self, piece_of_interest, file_squares):

        # Identify the closest squares on the selected rook's file that are occupied both above and below the rook.
        next_piece_above_on_file = None
        next_piece_below_on_file = None

        # Obtain a reversed list of file_squares.
        reversed_file_squares = file_squares[::-1]

        # The 'above' piece for white is black's 'below' piece, so we need to divide into cases.
        if self.colour == 'white':

            # Determine the closest piece that lies above the selected rook.        
            for square in file_squares:
                if square.isOccupied and square.rank > piece_of_interest.curSquare.rank:
                    next_piece_above_on_file = square

            # Determine the closest piece that lies below the selected rook.
            for square in reversed_file_squares:
                if square.isOccupied and square.rank < piece_of_interest.curSquare.rank:
                    next_piece_below_on_file = square

        else:
            
            # Determine the closest piece that lies above the selected rook.
            for square in file_squares:
                if square.isOccupied and square.rank > piece_of_interest.curSquare.rank:
                    next_piece_above_on_file = square

            # Determine the closest piece that lies below the selected rook.        
            for square in reversed_file_squares:
                if square.isOccupied and square.rank < piece_of_interest.curSquare.rank:
                    next_piece_below_on_file = square

        return next_piece_above_on_file, next_piece_below_on_file
    
    # Gets the closest occupied squares on the same rank as the selected rook.
    def get_closest_occupied_rank(self, piece_of_interest, rank_squares):

        # Identify the closest squares on the selected rook's rank that are occupied both left and right the rook.
        next_piece_left_on_rank = None
        next_piece_right_on_rank = None

        # Obtain a reversed list of rank_squares.
        reversed_rank_squares = rank_squares[::-1]

        # Gets the closest occupied square to the left of the selected rook.
        for square in rank_squares:
            if square.isOccupied and files_dict[square.file] > files_dict[piece_of_interest.curSquare.file]:
                next_piece_left_on_rank = square

        # Gets the closest occupied square to the right of the selected rook.
        for square in reversed_rank_squares:
            if square.isOccupied and files_dict[square.file] < files_dict[piece_of_interest.curSquare.file]:
                next_piece_right_on_rank = square

        return next_piece_left_on_rank, next_piece_right_on_rank

    # Determines if the path along a file from the selected rook to the square of interest is being blocked by some piece.
    # Returns true if it is, false otherwise.
    def is_blocked_file(self, square_of_interest, file_squares):

        # Get the closest occupied squares on the same file as the selected rook.
        next_piece_above_on_file, next_piece_below_on_file = self.get_closest_occupied_file(self, file_squares)

        # If there are no other pieces on a given file, then there are no squares off limits, return false.
        if next_piece_below_on_file is None and next_piece_above_on_file is None:
            return False

        # This case tests when there is a piece below the selected rook (on the same file).
        # If the square of interest has a smaller rank than the closest occupied piece below the selected rook, then we cannot move to the square of interest.
        if next_piece_below_on_file and square_of_interest.rank < next_piece_below_on_file.rank:
            return True

        # This case tests when there is a piece above the selected rook on its file (on the same file).
        # If the square of interest has a larger rank than the closest occupied piece above the selected rook, then we cannot move to the square of interest.
        if next_piece_above_on_file and square_of_interest.rank > next_piece_above_on_file.rank:
            return True

        # If all of these cases fail, then we are able to move to the square of interest.
        return False


    # Determines if the path along a rank from the selected rook to the square of interest is being blocked by some piece.
    # Returns true if it is, false otherwise.
    def is_blocked_rank(self, square_of_interest, rank_squares):
        
        # Get the closest occupied squares on the same rank as the selected rook.
        next_piece_left_on_rank, next_piece_right_on_rank = self.get_closest_occupied_rank(self, rank_squares)
        
        # If there are no other pieces on a given rank, then there are no squares off limits, return false.
        if next_piece_left_on_rank is None and next_piece_right_on_rank is None:
            return False

        # This case tests when there is a piece to the right of the selected rook (on the same rank).
        # If the square of interest is farther right than the closest piece to the right of the selected rook, then we cannot move to the square of interest.
        if next_piece_right_on_rank and files_dict[square_of_interest.file] < files_dict[next_piece_right_on_rank.file]:
            return True

        # This case tests when there is a piece to the left of the selected rook (on the same rank).
        # If the square of interest is farther left than the closest piece to the left of the selected rook, then we cannot move to the square of interest.
        if next_piece_left_on_rank and files_dict[square_of_interest.file] > files_dict[next_piece_left_on_rank.file]:
            return True
        
        # If all of these cases fail, then we are able to move to the square of interest.
        return False

    # For the queens
    def check_diagonals(self, square_of_interest, squares):

        # Get the squares on the same diagonal as the square of interest.
        self.get_diagonal_squares(square_of_interest, squares)

        # If the square of interest is on the same diagonal as the selected queen, but there is no path from the queen to that square.
        # I.e. There is a piece in-between the queen and that square, then we cannot move there.
        if self.is_blocked_diagonal(square_of_interest, squares) and square_of_interest in self.legal_moves:
            self.legal_moves.remove(square_of_interest)
            self.protected_squares.remove(square_of_interest)

    def check_files_and_ranks(self, square_of_interest, file_squares, rank_squares):

        # If the square of interest is not in the same file and it is not in the same rank as the square of interest, then we cannot move there.
        if square_of_interest.file != self.curSquare.file and square_of_interest.rank != self.curSquare.rank and square_of_interest in self.legal_moves:
            self.legal_moves.remove(square_of_interest)
            self.protected_squares.remove(square_of_interest)

        # If the square of interest is on the same file as the selected rook, but there is no path from the rook to that square.
        # I.e. There is a piece inbetween the rook and that square, then we cannot move there.
        if self.is_blocked_file(square_of_interest, file_squares):

            if square_of_interest in self.legal_moves:
                self.legal_moves.remove(square_of_interest)
            if square_of_interest in self.protected_squares:
                self.protected_squares.remove(square_of_interest)

        # If the square of interest is on the same rank as the selected rook, but there is no path from the rook to that square.
        # I.e. There is a piece inbetween the rook and that square, then we cannot move there.
        if self.is_blocked_rank(square_of_interest, rank_squares):
            
            if square_of_interest in self.legal_moves:
                self.legal_moves.remove(square_of_interest)
            if square_of_interest in self.protected_squares:
                self.protected_squares.remove(square_of_interest)


    # Determines if the king is attempting to castle 'through' check. Returns true if yes, false otherwise.
    def castle_through_check(self, square_of_interest, squares, pieces, selected_piece, our_king):
        for piece in pieces: 
            if piece.colour != self.colour and piece != self and piece.name != 'King':
                
                # if piece.name == 'King':
                #     piece.get_legal_moves(squares, pieces)
                # else:

                # for piece in pieces:
                #     if piece != self:
                #         piece.get_legal_moves(squares, pieces, selected_piece, our_king)

                if square_of_interest.id == 'G1':
                    if piece.name != 'Pawn': # TODO: Need to fix this!!!
                        for opponent_square in piece.legal_moves:
                            if opponent_square.id == 'F1' or opponent_square.id == 'G1':
                                return True
                
                elif square_of_interest.id == 'C1':
                    if piece.name != 'Pawn': # TODO: Need to fix this!!!:
                        for opponent_square in piece.legal_moves:
                            if opponent_square.id == 'D1' or opponent_square.id == 'C1':
                                return True

                elif square_of_interest.id == 'G8':
                    if piece.name != 'Pawn': # TODO: Need to fix this!!!:
                        for opponent_square in piece.legal_moves:
                            if opponent_square.id == 'F8' or opponent_square.id == 'G8':
                                return True

                elif square_of_interest.id == 'C8':
                    if piece.name != 'Pawn': # TODO: Need to fix this!!!:
                        for opponent_square in piece.legal_moves:
                            if opponent_square.id == 'D8' or opponent_square.id == 'C8':
                                return True

        return False

    # Returns true if our piece is pinned to our king, and thus cannot move, false otherwise.
    # Need to determine if the closest piece to the king, along the checking piece's diagonal, is also the closest piece to the checking piece.
    # If it is, then we are pinned.
    def is_pinned_along_diagonal(self, possible_pinning_piece, our_king):

        leftmost_pos_king, rightmost_pos_king, leftmost_neg_king, rightmost_neg_king = self.get_closest_occupied_diag(our_king.curSquare)
        
        # Get the closest pieces for the piece that is checking us.
        leftmost_pos_self, rightmost_pos_self, leftmost_neg_self, rightmost_neg_self = self.get_closest_occupied_diag(possible_pinning_piece.curSquare)

        if our_king:

            # If the closest piece to the left of the king on its positive diagonal is not the piece that is checking us, then it is blocking the check.
            if leftmost_pos_king and leftmost_pos_king != possible_pinning_piece.curSquare.id:

                # If the closest piece to the right of the checking-piece is the same piece that is closest to the left of the king, then that piece is pinned.
                if rightmost_pos_self and rightmost_pos_self == leftmost_pos_king and leftmost_pos_king == self.curSquare.id:
                    return True

            # If the closest piece to the left of the king on its negative diagonal is not the piece that is checking us, then it is blocking the check.
            if leftmost_neg_king and leftmost_neg_king != possible_pinning_piece.curSquare.id:
                
                # If the closest piece to the right of the piece checking us is the same piece that is closest to the left of the king, then that piece is pinned.
                if rightmost_neg_self and rightmost_neg_self == leftmost_neg_king and leftmost_neg_king == self.curSquare.id:
                    return True

            # If the closest piece to the right of the king on its positive diagonal is not the piece that is checking us, then it is blocking the check.
            if rightmost_pos_king and rightmost_pos_king != possible_pinning_piece.curSquare.id:
                
                # If the closest piece to the right of the piece checking us is the same piece that is closest to the left of the king, then that piece is pinned.
                if leftmost_pos_self and leftmost_pos_self == rightmost_pos_king and rightmost_pos_king == self.curSquare.id:
                    return True

            # If the closest piece to the right of the king on its negative diagonal is not the piece that is checking us, then it is blocking the check.
            if rightmost_neg_king and rightmost_neg_king != possible_pinning_piece.curSquare.id:
                
                # If the closest piece to the left of the piece checking us is the same piece that is closest to the right of the king, then that piece is pinned.
                if leftmost_neg_self and leftmost_neg_self == rightmost_neg_king and rightmost_neg_king == self.curSquare.id:
                    return True
        
        return False

    # Returns true if our piece is pinned to our king, and thus cannot move, false otherwise.
    # Need to determine if the closest piece to the king, along the checking piece's file, is also the closest piece to the checking piece.
    # If it is, then we are pinned.
    # Note. This function may need more work and/or testing. Not sure.
    def is_pinned_along_file(self, squares, pieces, possible_pinning_piece, our_king):
        
        if self.curSquare.file != our_king.curSquare.file:
            return False

        file_squares = [square for square in squares if square.file == our_king.curSquare.file]

        next_piece_above_on_file_king, next_piece_below_on_file_king = self.get_closest_occupied_file(our_king, file_squares)
        next_piece_above_on_file_piece, next_piece_below_on_file_piece = self.get_closest_occupied_file(self, file_squares) ############

        if our_king:

            # If the closest piece above the king on the same file is not the piece that is checking us, then it is blocking the check.
            # Then, if the next piece above the piece above the king is the possible pinning piece, and that piece is a queen or a rook, then we are pinned.
            # TODO: May need to change ######### above to get the closest occupied square above the piece that is above the king...
            #       It might not be the case that the piece above our king will always be self... Not sure...
            # This is from white's perspective.
            if next_piece_above_on_file_king and next_piece_above_on_file_king != possible_pinning_piece.curSquare:

                if next_piece_above_on_file_piece == possible_pinning_piece.curSquare and next_piece_below_on_file_piece == our_king.curSquare:
                    if possible_pinning_piece.name == 'Queen' or possible_pinning_piece.name == 'Rook':                        
                        return True

            # If the closest piece below the king on the same file is not the piece that is checking us, then it is blocking the check.
            if next_piece_below_on_file_king and next_piece_below_on_file_king != possible_pinning_piece.curSquare:

                if next_piece_below_on_file_piece == possible_pinning_piece.curSquare and next_piece_above_on_file_piece == our_king.curSquare:
                    if possible_pinning_piece.name == 'Queen' or possible_pinning_piece.name == 'Rook':
                        return True
        
        return False

    
    # Returns true if our piece is pinned to our king, and thus cannot move, false otherwise.
    # Need to determine if the closest piece to the king, along the checking piece's file, is also the closest piece to the checking piece.
    # If it is, then we are pinned.
    # Note. This function may need more work and/or testing. Not sure.
    def is_pinned_along_rank(self, squares, pieces, possible_pinning_piece, our_king):
        
        if self.curSquare.rank != our_king.curSquare.rank:
            return False

        rank_squares = [square for square in squares if square.rank == our_king.curSquare.rank]

        next_piece_left_of_king, next_piece_right_of_king = self.get_closest_occupied_rank(our_king, rank_squares)
        next_piece_left_of_piece, next_piece_right_of_piece = self.get_closest_occupied_rank(self, rank_squares) ############

        if our_king:
            # If the closest piece above the king on the same file is not the piece that is checking us, then it is blocking the check.
            # Then, if the next piece above the piece above the king is the possible pinning piece, and that piece is a queen or a rook, then we are pinned.
            # TODO: May need to change ######### above to get the closest occupied square above the piece that is above the king...
            #       It might not be the case that the piece above our king will always be self... Not sure...
            # This is from white's perspective.
            if next_piece_left_of_king and next_piece_left_of_king != possible_pinning_piece.curSquare:
                
                if next_piece_left_of_piece == possible_pinning_piece.curSquare and next_piece_right_of_piece == our_king.curSquare:
                    if possible_pinning_piece.name == 'Queen' or possible_pinning_piece.name == 'Rook':                        
                        return True

            # If the closest piece below the king on the same file is not the piece that is checking us, then it is blocking the check.
            if next_piece_right_of_king and next_piece_right_of_king != possible_pinning_piece.curSquare:
                
                if next_piece_right_of_piece == possible_pinning_piece.curSquare and next_piece_left_of_piece == our_king.curSquare:
                    if possible_pinning_piece.name == 'Queen' or possible_pinning_piece.name == 'Rook':
                        return True
        
        return False

    def get_piece(self, square_of_interest, pieces):
        for piece in pieces:
            if piece.curSquare == square_of_interest:
                return piece

    # If we are in check, then reset all of the king's variables to being False
    def our_king_in_check(self, captured_piece, our_king):
        
        if our_king and our_king.in_check:
            if our_king.curSquare not in our_king.checking_piece.legal_moves and captured_piece is None:
                our_king.in_check = False

                if our_king.checking_piece.name == 'Bishop':
                    our_king.in_check_along_diagonal = False

                elif our_king.checking_piece.name == 'Rook':

                    if our_king.curSquare.file != our_king.checking_piece.curSquare.file:
                        our_king.in_check_along_file = False

                    elif our_king.curSquare.rank != our_king.checking_piece.curSquare.rank:
                        our_king.in_check_along_rank = False

                elif our_king.checking_piece.name == 'Queen':

                    if our_king.curSquare.file != our_king.checking_piece.curSquare.file:
                        our_king.in_check_along_file = False

                    elif our_king.curSquare.rank != our_king.checking_piece.curSquare.rank:
                        our_king.in_check_along_rank = False

                    elif our_king.curSquare.diagonals in our_king.checking_piece.curSquare.diagonals:
                        our_king.in_check_along_diagonal = False

                elif our_king.checking_piece.name == 'Pawn':
                    our_king.in_check_along_diagonal = False

                elif our_king.checking_piece.name == 'Knight':
                    our_king.in_check_from_knight = False

                our_king.checking_piece = None

            elif captured_piece and captured_piece == our_king.checking_piece:
                print('Not in check anymore')
                our_king.in_check = False

                if captured_piece == 'Bishop':
                    our_king.in_check_along_diagonal = False

                elif captured_piece == 'Rook':

                    if our_king.in_check_along_file:
                        our_king.in_check_along_file = False

                    elif our_king.in_check_along_rank:
                        our_king.in_check_along_rank = False

                elif our_king.checking_piece.name == 'Queen':

                    if our_king.in_check_along_file:
                        our_king.in_check_along_file = False

                    elif our_king.in_check_along_rank:
                        our_king.in_check_along_rank = False

                    elif our_king.in_check_along_diagonal:
                        our_king.in_check_along_diagonal = False

                elif our_king.checking_piece.name == 'Pawn':
                    our_king.in_check_along_diagonal = False

                elif our_king.checking_piece.name == 'Knight':
                    our_king.in_check_from_knight = False

                our_king.checking_piece = None



    def how_in_check(self, king):

        method_of_checking = ''

        if king.checking_piece.name == 'Bishop':
            print('In check along a diagonal from a bishop.')
            king.in_check_along_diagonal = True
            method_of_checking = 'diagonal'

        elif king.checking_piece.name == 'Rook':

            if king.curSquare.file == king.checking_piece.curSquare.file:
                print('In check along a file from a rook.')
                king.in_check_along_file = True
                method_of_checking = 'file'

            elif king.curSquare.rank == king.checking_piece.curSquare.rank:
                print('In check along a rank from a rook.')
                king.in_check_along_rank = True
                method_of_checking = 'rank'

        elif king.checking_piece.name == 'Queen':

            if king.curSquare.file == king.checking_piece.curSquare.file:
                print('In check along a file from a queen.')
                king.in_check_along_file = True
                method_of_checking = 'file'

            elif king.curSquare.rank == king.checking_piece.curSquare.rank:
                print('In check along a rank from a queen.')
                king.in_check_along_rank = True
                method_of_checking = 'rank'

            elif king.curSquare in king.checking_piece.curSquare.diagonals:
                print('In check along a diagonal from a queen.')
                king.in_check_along_diagonal = True
                method_of_checking = 'diagonal'

        elif king.checking_piece.name == 'Pawn':
            print('In check along a diagonal from a pawn.')
            king.in_check_along_diagonal = True
            method_of_checking = 'diagonal'
        
        elif king.checking_piece.name == 'Knight':
            print('In check from a knight.')
            king.in_check_from_knight = True
            method_of_checking = 'knight'
        
        return king


    # Next, check if we are pinned to our king
    def check_for_pins(self, pieces, squares, our_king):
        if our_king:
            last_checking_piece = None
        
            for piece in [piece for piece in pieces if piece.colour != self.colour]:
                
                if len(our_king.list_of_checking_pieces) != 0:
                    last_checking_piece = list(our_king.list_of_checking_pieces)[-1][0]
                else:
                    last_checking_piece = piece


                # Is the selected queen pinned to our king by the piece of interest, which has checked our king.
                if self.is_pinned_along_diagonal(piece, our_king):
                    self.pinned_along_diagonal = True

                    if self.pinning_piece is None:
                        self.pinning_piece = last_checking_piece

                    for square in self.legal_move_copy:
                        if square not in our_king.curSquare.diagonals and square in self.legal_moves:
                            self.legal_moves.remove(square)
                    
                    break
                
                elif not self.is_pinned_along_diagonal(piece, our_king) and self.pinned_along_diagonal and self.pinning_piece == piece:
                    self.pinned_along_diagonal = False
                    self.pinning_piece = None
                    self.our_king_in_check(None, our_king)

            
                # Are we currently being pinned to our king along a file by the piece of interest?
                if self.is_pinned_along_file(squares, pieces, piece, our_king):
                    #print(f'{self.name} on {self.curSquare.id} we pinned')
                    self.pinned_along_file = True
                    self.pinning_piece = piece
                    #print(f'{self.curSquare.id} Being pinned by the {self.pinning_piece.colour} {self.pinning_piece.name} on {self.pinning_piece.curSquare.id}')

                    for square in self.legal_move_copy:
                        if square.file != our_king.curSquare.file and square in self.legal_moves:
                            self.legal_moves.remove(square)

                elif not self.is_pinned_along_file(squares, pieces, piece, our_king) and self.pinned_along_file:
                    #print(f'{self.name} {self.curSquare.id} aint pinned anymore')
                    self.pinned_along_file = False
                    self.pinning_piece = None
                    self.our_king_in_check(None, our_king)


                # Are we currently being pinned to our king along a rank by the piece of interest?
                if self.is_pinned_along_rank(squares, pieces, piece, our_king):
                    print(f'{self.name} on {self.curSquare.id} we pinned')
                    self.pinned_along_rank = True
                    self.pinning_piece = piece
                    #print(f'{self.curSquare.id} Being pinned by the {self.pinning_piece.colour} {self.pinning_piece.name} on {self.pinning_piece.curSquare.id}')

                    for square in self.legal_move_copy:
                        if square.rank != our_king.curSquare.rank and square in self.legal_moves:
                            self.legal_moves.remove(square)

                elif not self.is_pinned_along_rank(squares, pieces, piece, our_king) and self.pinned_along_rank:
                    #print(f'{self.name} {self.curSquare.id} aint pinned anymore')
                    self.pinned_along_rank = False
                    self.pinning_piece = None
                    self.our_king_in_check(None, our_king)

    def check_remaining_squares(self, our_king, legal_move_copy):
        for square in legal_move_copy:

            if square in self.legal_moves:

                # If the king was in check, but now isn't, and the bishop isn't the blocking piece.  Only remove squares on the bishop's diagonal if we are in check.
                if our_king and our_king.checking_piece and len(our_king.list_of_checking_pieces) != 0:
                    
                    last_checking_piece = list(our_king.list_of_checking_pieces)[-1][0]
                    # TODO: Add other cases, pinned along rile, rank...
                    # If some piece of interest is pinned along a diagonal and our king is in check by some piece not in the piece of interest's legal moves, then the piece of interest cannot make any moves.
                    # if self.pinned_along_diagonal and last_checking_piece.curSquare not in self.legal_moves:
                    #     self.legal_moves.clear()
                    #     break
                    
                        
                    # In check along diagonal
                    if square in self.legal_moves and our_king.in_check_along_diagonal:

                        # If the square of interest is not on either of our king's diagonals, and it isn't on either of our king's checking-piece's diagonals.
                        if square not in our_king.checking_piece.curSquare.diagonals:
                            self.legal_moves.remove(square)
                            continue
                            
                        # If the square of interest is on one of our king's diagonals, but it isn't on either of our king's checking-piece's diagonals.
                        elif square in our_king.curSquare.diagonals and square not in our_king.checking_piece.curSquare.diagonals:
                            if square in self.legal_moves:
                                self.legal_moves.remove(square)
                                continue

                        # If the square of interest is on one of our king's checking-piece's diagonals , but it isn't on either of our king's diagonals.
                        elif square in our_king.checking_piece.curSquare.diagonals and square not in our_king.curSquare.diagonals:
                            if square in self.legal_moves:
                                self.legal_moves.remove(square)      
                                continue                  
                        
                        # If the square of interest is on one of our king's diagonals and it is on one of our king's checking-piece's diagonals.
                        else:

                            # If the square of interest is on a file right of our king and our king's checking-piece is on a file left of our king.
                            # I.e. Our king is in-between our king's checking-piece and the square of interest, but the square of interest is on the wrong side.
                            if files_dict[last_checking_piece.curSquare.file] < files_dict[our_king.curSquare.file] < files_dict[square.file]:
                                if square in self.legal_moves:
                                    self.legal_moves.remove(square)
                                    continue
                            
                            # If the square of interest is on a file left of our king and our king's checking-piece is on a file right of our king.
                            # I.e. Our king is in-between our king's checking-piece and the square of interest, but the square of interest is on the wrong side.
                            elif files_dict[square.file] < files_dict[our_king.curSquare.file] < files_dict[last_checking_piece.curSquare.file]:
                                if square in self.legal_moves:
                                    self.legal_moves.remove(square)
                                    continue
                            
                            # If the square of interest is on a file left of our king's checking-piece and our king is on a file left of it's checking-piece.
                            # I.e. The checking-piece is in-between our king and the square of interest, but the square of interest is on the wrong side.
                            elif files_dict[square.file] < files_dict[last_checking_piece.curSquare.file] < files_dict[our_king.curSquare.file]:
                                if square in self.legal_moves:
                                    self.legal_moves.remove(square)
                                    continue
                            
                            # If the square of interest is on a file right of our king's checking-piece and our king is on a file right of it's checking-piece.
                            # I.e. The checking-piece is in-between our king and the square of interest, but the square of interest is on the wrong side.
                            elif files_dict[our_king.curSquare.file] < files_dict[last_checking_piece.curSquare.file] < files_dict[square.file]:
                                if square in self.legal_moves:
                                    self.legal_moves.remove(square)
                                    continue

                    # In check along file
                    elif square in self.legal_moves and our_king.in_check_along_file:
                        
                        # Remove any squares that aren't on the same file as our king.
                        if square.file != our_king.curSquare.file:
                            self.legal_moves.remove(square)
                            continue

                        # If the square of interest is on the same file as our king.
                        else:

                            # If the square of interest is on a higher rank than our king and our king's checking-piece is on a lower rank than our king.
                            # I.e. Our king is in-between our king's checking-piece and the square of interest, but the square of interest is on the wrong side.
                            if last_checking_piece.curSquare.rank < our_king.curSquare.rank < square.rank:
                                self.legal_moves.remove(square)
                                continue
                            
                            # If the square of interest is on a lower rank than our king and our king's checking-piece is on a higher rank than our king.
                            # I.e. Our king is in-between our king's checking-piece and the square of interest, but the square of interest is on the wrong side.
                            elif square.rank < our_king.curSquare.rank < last_checking_piece.curSquare.rank:
                                self.legal_moves.remove(square)
                                continue
                            
                            # If the square of interest is on a lower rank than our king's checking-piece and our king is on a higher rank than it's checking-piece.
                            # I.e. The checking-piece is in-between our king and the square of interest, but the square of interest is on the wrong side.
                            elif square.rank < last_checking_piece.curSquare.rank < our_king.curSquare.rank:
                                self.legal_moves.remove(square)
                                continue
                            
                            # If the square of interest is on a higher rank than our king's checking-piece and our king is on a lower rank than it's checking-piece.
                            # I.e. The checking-piece is in-between our king and the square of interest, but the square of interest is on the wrong side.
                            elif our_king.curSquare.rank < last_checking_piece.curSquare.rank < square.rank:
                                self.legal_moves.remove(square)
                                continue

                        

                    # In check along rank
                    elif square in self.legal_moves and our_king.in_check_along_rank:

                        # If the square of interest is not on the same rank as our king, and thus not on the same rank as our king's checking-piece.
                        if square.rank != our_king.curSquare.rank:
                            self.legal_moves.remove(square)
                            continue
                                        
                        # If the square of interest is on the same rank as our king, and thus on the same rank as our king's checking-piece.
                        else:

                            # If the square of interest is on a file left of our king and our king's checking-piece is on a file right of our king.
                            # I.e. Our king is in-between our king's checking-piece and the square of interest, but the square of interest is on the wrong side.
                            if files_dict[last_checking_piece.curSquare.file] < files_dict[our_king.curSquare.file] < files_dict[square.file]:
                                self.legal_moves.remove(square)
                                continue
                            
                            # If the square of interest is on a file right of our king and our king's checking-piece is on a file left of our king.
                            # I.e. Our king is in-between our king's checking-piece and the square of interest, but the square of interest is on the wrong side.
                            elif files_dict[square.file] < files_dict[our_king.curSquare.file] < files_dict[last_checking_piece.curSquare.file]:
                                self.legal_moves.remove(square)
                                continue
                            
                            # If the square of interest is on a file right of our king's checking-piece and our king is on a file left of it's checking-piece.
                            # I.e. The checking-piece is in-between our king and the square of interest, but the square of interest is on the wrong side.
                            elif files_dict[square.file] < files_dict[last_checking_piece.curSquare.file] < files_dict[our_king.curSquare.file]:
                                self.legal_moves.remove(square)
                                continue
                            
                            # If the square of interest is on a file left of our king's checking-piece and our king is on a file right of it's checking-piece.
                            # I.e. The checking-piece is in-between our king and the square of interest, but the square of interest is on the wrong side.
                            elif files_dict[our_king.curSquare.file] < files_dict[last_checking_piece.curSquare.file] < files_dict[square.file]:
                                self.legal_moves.remove(square)
                                continue

                    elif square in self.legal_moves and our_king.in_check_from_knight:
                        if square != our_king.checking_piece.curSquare:
                            self.legal_moves.remove(square)