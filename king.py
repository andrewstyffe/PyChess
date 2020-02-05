import pygame as pg

class King(pg.sprite.Sprite):
    def __init__(self, square, colour):
        super(King, self).__init__()
        self.clicked = False
        self.name = 'King'
        #self.id = _id
        self.colour = colour

        if self.colour == 'white':
            pic = pg.image.load("./white_king.png")
        else:
            pic = pg.image.load("./black_king.png")
        
        self.image = pg.transform.scale(pic, (50, 50))
        self.rect = pg.Rect(square.x, square.y, 50, 50)