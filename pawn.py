import pygame as pg

class Pawn(pg.sprite.Sprite):
    def __init__(self, square, colour):
        super(Pawn, self).__init__()
        self.clicked = False
        self.name = 'Pawn'
        #self.id = _id
        self.colour = colour

        if self.colour == 'white':
            pic = pg.image.load("./white_pawn.png")
        else:
            pic = pg.image.load("./black_pawn.png")
        
        self.image = pg.transform.scale(pic, (50, 50))
        self.rect = pg.Rect(square.x, square.y, 100, 100)