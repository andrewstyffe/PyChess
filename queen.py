import pygame as pg

class Queen(pg.sprite.Sprite):
    def __init__(self, square, colour):
        super(Queen, self).__init__()
        self.clicked = False
        self.name = 'Queen'
        #self.id = _id
        self.colour = colour

        if self.colour == 'white':
            pic = pg.image.load("./white_queen.png")
        else:
            pic = pg.image.load("./black_queen.png")
        
        self.image = pg.transform.scale(pic, (50, 50))
        self.rect = pg.Rect(square.x, square.y, 50, 50)