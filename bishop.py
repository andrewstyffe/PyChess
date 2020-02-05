import pygame as pg

class Bishop(pg.sprite.Sprite):
    def __init__(self, square, colour):
        super(Bishop, self).__init__()
        self.clicked = False
        self.name = 'Bishop'
        #self.id = _id
        self.colour = colour

        if self.colour == 'white':
            pic = pg.image.load("./white_bishop.png")
        else:
            pic = pg.image.load("./black_bishop.png")
        
        self.image = pg.transform.scale(pic, (50, 50))
        self.rect = pg.Rect(square.x, square.y, 50, 50)