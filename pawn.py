import pygame as pg

class Pawn(pg.sprite.Sprite):
    def __init__(self, square, _id):
        super(Pawn, self).__init__()
        pic = pg.image.load("./white_pawn.png")
        self.image = pg.transform.scale(pic, (50, 50))
        self.clicked = False
        self.rect = pg.Rect(self.image.get_rect())
        #self.rect.topleft = position.topleft
        #self.rect.center = position.center
        self.id = _id
        self.square = square