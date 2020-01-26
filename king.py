import pygame as pg

class King(pg.sprite.Sprite):
    def __init__(self, coords, _id):
        super(King, self).__init__()
        pic = pg.image.load("./white_king.png")
        self.image = pg.transform.scale(pic, (50, 50))
        self.clicked = False
        self.rect = self.image.get_rect()
        self.rect.x = coords[0]
        self.rect.y = coords[1]
        self.id = _id