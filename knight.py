import pygame as pg

class Knight(pg.sprite.Sprite):
    def __init__(self, square, colour):
        super(Knight, self).__init__()
        self.clicked = False
        self.name = 'Knight'
        #self.id = _id
        self.colour = colour

        if self.colour == 'white':
            pic = pg.image.load("./white_knight.png")
        else:
            pic = pg.image.load("./black_knight.png")
        
        self.image = pg.transform.scale(pic, (50, 50))
        self.rect = pg.Rect(square.x, square.y, 50, 50)