import pygame as pg

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

# Wrangling together this monstrous list of diagonals
pos_diagonals = [pos_diag_a1, pos_diag_b1, pos_diag_c1, pos_diag_d1, pos_diag_e1, pos_diag_f1, pos_diag_g1, pos_diag_a2, pos_diag_a3, pos_diag_a4, pos_diag_a5, pos_diag_a6, pos_diag_a7]
neg_diagonals = [neg_diag_b1, neg_diag_c1, neg_diag_d1, neg_diag_e1, neg_diag_f1, neg_diag_g1, neg_diag_h1, neg_diag_h2, neg_diag_h3, neg_diag_h4, neg_diag_h5, neg_diag_h6, neg_diag_h7]
diagonals = [pos_diagonals, neg_diagonals]

class Bishop(pg.sprite.Sprite):
    def __init__(self, square, colour):
        super(Bishop, self).__init__()
        self.clicked = False
        self.name = 'Bishop'
        self.colour = colour
        self.curSquare = square
        self.legal_moves = []
        
        # Assigns a picture to the bishop
        if self.colour == 'white':
            self.image = pg.image.load("./white_bishop.png")
        else:
            self.image = pg.image.load("./black_bishop.png")
        
        self.image = pg.transform.scale(self.image, (50, 50))
        self.rect = self.image.get_rect(center = self.curSquare.center)

    def drag(self, board, cursor):
        self.rect = self.rect.move(cursor[0], cursor[1])

    def draw(self, surface):
        surface.blit(self.image, self.rect.topleft)

    def update(self, board, fromSquare, newSquare):
        self.curSquare = newSquare
        self.rect.center = newSquare.center
        self.fromSquare = fromSquare

        newSquare.isOccupied = True
        fromSquare.isOccupied = False
        newSquare.occupied_colour = self.colour


    # Returns the square object with the given square id.
    def get_square(self, square_of_interest, squares):
        for square in squares:
            if square.id == square_of_interest:
                return square


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

    # Gets the closest occupied squares to the square of interest.
    def get_closest_occupied(self, square_of_interest):

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
        #     self.get_diagonal_squares(square_of_interest, squares)

        # Get the closest occupied squares to the square of interest.
        leftmost_pos_occupied, rightmost_pos_occupied, leftmost_neg_occupied, rightmost_neg_occupied = self.get_closest_occupied(square_of_interest)

        # If there are no leftmost and no rightmost pieces along a given diagonal on which the selected bishop resides, 
        # then we can move to any of those squares.
        if leftmost_pos_occupied == '' and rightmost_pos_occupied == '' and self.curSquare in square_of_interest.pos_diagonal:
            return False
        if leftmost_neg_occupied == '' and rightmost_neg_occupied == '' and self.curSquare in square_of_interest.neg_diagonal:
            return False


        # This case tests when our selected bishop wants to move on its positive diagonal in the positive direction, i.e. the square of interest
        # has a larger rank than our current square.
        # If our current rank is smaller than the closest leftmost piece to the square of interest, then we cannot move to the square of interest.
        if leftmost_pos_occupied and self.curSquare.rank < leftmost_pos_occupied[1] and self.curSquare in square_of_interest.pos_diagonal:
            return True
        
        # This case tests when our selected bishop wants to move on its positive diagonal in the negative direction, i.e. the square of interest
        # has a smaller rank than our current square.
        # If our current rank is larger than the closest rightmost piece to the square of interest, then we cannot move to the square of interest.
        if rightmost_pos_occupied and self.curSquare.rank > rightmost_pos_occupied[1] and self.curSquare in square_of_interest.pos_diagonal:
            return True

        # This case tests when our selected bishop wants to move on its negative diagonal in the positive direction, i.e. the square of interest
        # has a smaller rank than our current square.
        # If our current rank is larger than the closest leftmost piece to the square of interest, then we cannot move to the square of interest.
        if leftmost_neg_occupied and self.curSquare.rank > leftmost_neg_occupied[1] and self.curSquare in square_of_interest.neg_diagonal:
            return True

        # This case tests when our selected bishop wants to move on its negative diagonal in the negative direction, i.e. the square of interest
        # has a larger rank than our current square.
        # If our current rank is smaller than the closest rightmost piece to the square of interest, then we cannot move to the square of interest.
        if rightmost_neg_occupied and self.curSquare.rank < rightmost_neg_occupied[1] and self.curSquare in square_of_interest.neg_diagonal:
            return True
        
        # If all of these cases are untrue, then we are able to move to the square of interest.
        return False



    # Returns a list of squares the a given bishop is able to move to.
    # After a bishop is selected, this method does the following.
    # 1. It gets the squares residing on the diagonal(s) in which the selected bishop resides.
    # 1. It adds all of the squares found in step 1 to self.legal_squares.
    # 3. It sorts through all of those squares to determine which ones represent illegal moves.
    def get_legal_moves(self, squares):

        # Get the squares on the same diagonals as the selected bishop, and reset our list of legal_moves.
        self.get_diagonal_squares(self.curSquare, squares)  
        self.legal_moves = []

        # Now add all of these squares to legal_moves. Next then remove the illegal ones
        for square in self.curSquare.diagonals:
            if square not in self.legal_moves:
                self.legal_moves.append(square)

        # Now sort through those square ids by eliminating the illegal ones.
        for square in self.curSquare.diagonals:

            # Get the squares on the same diagonals as the square of interest.
            self.get_diagonal_squares(square, squares)

            # If the selected bishop doesn't reside on the diagonals of the square of interest. Then clearly we cannot move there.
            if self.curSquare not in square.diagonals:
                self.legal_moves.remove(square)

            # If the square of interest is occupied by one of our own pieces, then we cannot move there.
            if square.isOccupied and square.occupied_colour == self.colour and square in self.legal_moves:
                self.legal_moves.remove(square)

            # If the square of interest is on the same diagonal as the selected bishop, but there is no path from the bishop to that square.
            # I.e. There is a piece inbetween the bishop and that square, then we cannot move there.
            if self.is_blocked_diagonal(square, squares) and square in self.legal_moves:
                self.legal_moves.remove(square)

        # Remove our current square as a potential move.
        if self.curSquare in self.legal_moves:
            self.legal_moves.remove(self.curSquare)

        # Instead of returning a list of legal square objects, return a list of legal square ids.
        sorted_legal_moves = [square.id for square in self.legal_moves]
        return sorted_legal_moves