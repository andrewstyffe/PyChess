import pygame as pg

class Knight(pg.sprite.Sprite):
    def __init__(self, square, colour):
        super(Knight, self).__init__()
        self.clicked = False
        self.name = 'Knight'
        #self.id = _id
        self.colour = colour
        self.curSquare = square

        if self.colour == 'white':
            self.image = pg.image.load("./white_knight.png")
        else:
            self.image = pg.image.load("./black_knight.png")
        
        self.image = pg.transform.scale(self.image, (50, 50))
        self.rect = self.image.get_rect(center = self.curSquare.center)
        
    def drag(self, board, cursor):
        self.rect = self.rect.move(cursor[0], cursor[1])

    def draw(self, surface):
        surface.blit(self.image, self.rect.topleft)

    def update(self, board, newSquare):
        self.curSquare = newSquare
        self.rect.center = newSquare.center
        #board.blit(self.image, curSquare.coords.center)