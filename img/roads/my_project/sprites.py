import pygame
from terrain import *
from random import randint

CELL_SIZE = 98
sprites = pygame.sprite.Group()
players = pygame.sprite.Group()
roads = pygame.sprite.Group()


def load_image(name, color_key=None):
    try:
        image = pygame.image.load("img/" + name)
        image = image.convert_alpha()
    except pygame.error as message:
        print('Cannot load image:', name)
        raise SystemExit(message)
    return image



class TileSprite(pygame.sprite.Sprite):
    
    def __init__(self, tile_type, pos_x, pos_y):
        self.x = pos_x
        self.y = pos_y
        global tile_paths
        super().__init__()  
        self.image = load_image(tile_paths[tile_type])
        self.rect = self.image.get_rect().move(CELL_SIZE * self.x,
                                               CELL_SIZE * self.y)
    
    def moves(self, dx, dy):
        self.x += dx
        self.y += dy
        self.rect = self.image.get_rect().move(CELL_SIZE * self.x,
                                               CELL_SIZE * self.y)        

class Player(pygame.sprite.Sprite):
    
    def __init__(self, pos_x, pos_y):
        self.x = self.ix = pos_x
        self.y = self.iy = pos_y
        super().__init__()          
        self.image = load_image(tile_paths["player"])
        self.rect = self.image.get_rect().move(CELL_SIZE * self.ix,
                                               CELL_SIZE * self.iy)
    
    def moves(self, dx, dy):
        self.x += dx
        self.y += dy
        

class Road(pygame.sprite.Sprite):
    
    def __init__(self, pos_x, pos_y, level):
        super().__init__()
        self.ix = self.x = pos_x
        self.iy = self.y = pos_y
        self.level = level
        self.roadmap = level.roadmap
        self.mask = self.getRoadMask()
        self.image = load_image(f"roads/{''.join(self.mask)}.png")
        self.rect = self.image.get_rect().move(CELL_SIZE * self.x,
                                               CELL_SIZE * self.y)        
        
    def getRoadMask(self):
        a = ['0', '0', '0', '0']
        w, h = self.level.width, self.level.height
        print(self.iy, self.ix, w, h)
        if self.iy - 1 >= 0 and self.iy < h and self.roadmap[self.ix][self.iy - 1]:
            a[0] = '1'
        if self.iy + 1 < h and self.iy >= 0 and self.roadmap[self.ix][self.iy + 1]:
            a[1] = '1'
        if self.ix + 1 < w and self.ix >= 0 and self.roadmap[self.ix + 1][self.iy]:
            a[2] = '1'
        if self.ix - 1 >= 0 and self.ix < w and self.roadmap[self.ix - 1][self.iy]:
            a[3] = '1'
        return a
    
    def update(self):
        self.newmask = self.getRoadMask()
        if self.newmask == self.mask:
            return
        self.image = load_image(f"roads/{''.join(self.newmask)}.png")  
        self.rect = self.image.get_rect().move(CELL_SIZE * self.x,
                                               CELL_SIZE * self.y)             
        
    def moves(self, dx, dy):
        self.x += dx
        self.y += dy
        self.mask = self.getRoadMask()
        self.image = load_image(f"roads/{''.join(self.mask)}.png")  
        self.rect = self.image.get_rect().move(CELL_SIZE * self.x,
                                               CELL_SIZE * self.y)     