import pygame as pg
from pygame.locals import Rect

# Coords is a Rect object describing the square
# Square_id is a string in the chess coordinate system, e.g. 'A5'...
class Square(pg.sprite.Sprite):
    def __init__(self, coords, square_id, colour):
        pg.sprite.Sprite.__init__(self)
        self.coords = coords
        self.id = square_id
        self.file = square_id[0]
        self.rank = int(square_id[1])
        self.colour = colour
        self.topleft = coords.topleft
        self.center = coords.center
        self.x = coords[0]
        self.y = coords[1]
        self.isOccupied = False
        self.occupied_colour = None

        self.pos_diagonal = []
        self.neg_diagonal = []
        self.diagonals = []
        self.diagonal_ids = None