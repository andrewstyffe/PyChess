import pygame as pg
from pygame.locals import Rect

class Square(pg.sprite.Sprite):
    def __init__(self, square_coords, square_id):
        pg.sprite.Sprite.__init__(self)
        self.square_coords = square_coords
        self.square_id = square_id
        #self.rect = pg.Rect(self.image.get_rect())