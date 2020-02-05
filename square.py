import pygame as pg
from pygame.locals import Rect

class Square(pg.sprite.Sprite):
    def __init__(self, coords, square_id):
        pg.sprite.Sprite.__init__(self)
        self.coords = coords
        self.id = square_id
        self.file = square_id[0]
        self.rank = square_id[1]
        self.topleft = coords.topleft
        self.centre = coords.center
        self.x = coords.topleft[0]
        self.y = coords.topleft[1]