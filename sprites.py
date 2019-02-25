import pygame
from terrain import *
from random import randint
from math_thingies import get_starting_pixel, cur_frame, cur_frame_gen


CELL_SIZE = 97
sprites = pygame.sprite.OrderedUpdates()
players = pygame.sprite.Group()
roads = pygame.sprite.Group()
weathers = pygame.sprite.Group()
base = pygame.sprite.Group()


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
                                               CELL_SIZE * self.y - 32)
    
    def moves(self, dx, dy):
        self.x += dx
        self.y += dy
        self.rect = self.image.get_rect().move(CELL_SIZE * self.x,
                                               CELL_SIZE * self.y - 32)
        

class BaseSprite(TileSprite):
    
    def __init__(self, tile_type, pos_x, pos_y):
        super().__init__(tile_type, pos_x, pos_y)
        self.rect = self.image.get_rect().move(CELL_SIZE * self.x,
                                               CELL_SIZE * self.y)        
        
    def beautiful(self):
        pass
    
    def moves(self, dx, dy):
        self.x += dx
        self.y += dy
        self.rect = self.image.get_rect().move(CELL_SIZE * self.x,
                                               CELL_SIZE * self.y)    

        
class WaterSprite(pygame.sprite.Sprite):
    
    def __init__ (self, tile_type, pos_x, pos_y):
        super().__init__()
        self.x = pos_x
        self.y = pos_y        
        self.i = 0
        self.images = [load_image(f"water/frame_{str(i).rjust(2, '0')}_delay-0.1s.png") for i in range(50)]
        self.image = self.images[self.i]
        self.rect = self.image.get_rect().move(CELL_SIZE * self.x,
                                               CELL_SIZE * self.y)
    def moves(self, dx, dy):
        self.x += dx
        self.y += dy
        self.i += 1
        self.image = self.images[cur_frame(self.i, 99)]
        self.rect = self.image.get_rect().move(CELL_SIZE * self.x,
                                               CELL_SIZE * self.y)
        
        
class ThunderSprite(pygame.sprite.Sprite):
    
    def __init__ (self, tile_type, pos_x, pos_y):
        super().__init__()
        self.x = pos_x
        self.y = pos_y        
        self.i = 0
        self.images = [load_image(f"thunder/frame_{str(i).rjust(2, '0')}_delay-0.06s.png") for i in range(20)]
        for i in range(len(self.images)):
            self.images[i] = self.images[i]
        self.image = self.images[self.i]
        self.rect = self.image.get_rect().move(CELL_SIZE * self.x - 24,
                                               CELL_SIZE * self.y - 64)
    def moves(self, dx, dy):
        self.x += dx
        self.y += dy
        self.i += 1
        self.k = self.i // 5
        self.image = self.images[cur_frame(self.k, 39)]
        self.rect = self.image.get_rect().move(CELL_SIZE * self.x - 24,
                                               CELL_SIZE * self.y - 64)
        
class GeneratorSprite(pygame.sprite.Sprite):
    
    def __init__ (self, pos_x, pos_y, level):
        super().__init__()
        self.ix = self.x = pos_x
        self.iy = self.y = pos_y
        self.level = level       
        self.i = 0
        self.images = [load_image(f"generator/{i}.png") for i in range(4)]
        self.image = self.images[self.i]
        self.rect = self.image.get_rect().move(CELL_SIZE * self.x,
                                               CELL_SIZE * self.y)
    def moves(self, dx, dy):
        self.x += dx
        self.y += dy
        self.i += 1
        activated = bool(self.level[self.ix][self.iy].activated)
        self.image = self.images[cur_frame_gen(self.i, activated)]
        self.rect = self.image.get_rect().move(CELL_SIZE * self.x,
                                               CELL_SIZE * self.y) 


class ExitSprite(pygame.sprite.Sprite):
    
    def __init__ (self, pos_x, pos_y, level):
        super().__init__()
        self.ix = self.x = pos_x
        self.iy = self.y = pos_y
        self.level = level
        self.i = 0
        self.images = [load_image(f"exit/Drive{i}_0.png") for i in range(7)]
        self.image = self.images[self.i]
        self.rect = self.image.get_rect().move(CELL_SIZE * self.x + 16,
                                               CELL_SIZE * self.y + 16)
    def moves(self, dx, dy):
        self.x += dx
        self.y += dy
        self.total = self.level.cntGens
        self.now = self.level.cntActive
        self.image = self.images[self.now * 6 // self.total]
        self.rect = self.image.get_rect().move(CELL_SIZE * self.x + 16,
                                               CELL_SIZE * self.y + 16)     

        
class Player(pygame.sprite.Sprite):
    
    def __init__ (self, pos_x, pos_y):
        super().__init__()
        self.ix = self.x = pos_x
        self.iy = self.y = pos_y
        self.i = 0
        self.images = [load_image(f"player/{str(i + 1)}.png") for i in range(14)]
        self.image = self.images[self.i]
        self.rect = self.image.get_rect().move(CELL_SIZE * self.x + 16,
                                               CELL_SIZE * self.y + 16) 
    
    def upd(self):
        self.i += 1
        self.image = self.images[cur_frame(self.i, 27)]
        self.rect = self.image.get_rect().move(CELL_SIZE * self.ix,
                                               CELL_SIZE * self.iy)         
    
    def moves(self, dx, dy, dix, diy):
        self.ix = dix
        self.iy = diy
        self.x += dx
        self.y += dy
        self.image = self.images[cur_frame(self.i, 27)]
        self.rect = self.image.get_rect().move(CELL_SIZE * self.ix,
                                               CELL_SIZE * self.iy)        
        

class Road(pygame.sprite.Sprite):
    
    def __init__(self, pos_x, pos_y, level):
        super().__init__()
        self.ix = self.x = pos_x
        self.iy = self.y = pos_y
        self.level = level
        self.roadmap = level.roadmap
        self.image = load_image(f"empty.png")
        self.mask = ['0'] * 4
        self.rect = self.image.get_rect().move(CELL_SIZE * self.x,
                                               CELL_SIZE * self.y)        
        
    def getRoadMask(self):
        a = ['0', '0', '0', '0']
        w, h = self.level.width, self.level.height
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
        if self.newmask == self.mask or not self.roadmap[self.ix][self.iy]:
            return
        self.image = load_image(f"roads/{''.join(self.newmask)}.png")  
        self.rect = self.image.get_rect().move(CELL_SIZE * self.x,
                                               CELL_SIZE * self.y)             
        
    def moves(self, dx, dy):
        self.x += dx
        self.y += dy
        self.rect = self.image.get_rect().move(CELL_SIZE * self.x,
                                               CELL_SIZE * self.y)     