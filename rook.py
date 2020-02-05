import pygame as pg

class Rook(pg.sprite.Sprite):
    def __init__(self, square, colour):
        super(Rook, self).__init__()
        self.clicked = False
        self.name = 'Rook'
        #self.id = _id
        self.colour = colour

        if self.colour == 'white':
            pic = pg.image.load("./white_rook.png")
        else:
            pic = pg.image.load("./black_rook.png")
        
        self.image = pg.transform.scale(pic, (50, 50))
        self.rect = pg.Rect(square.x, square.y, 50, 50)