import pygame
from random import choice, random, randint
from terrain import *
from kruskal import *
from dijkstra import *
from handling import *
from math_thingies import evaluate

difficulty = 4
directions = {pygame.K_RIGHT: (1, 0), pygame.K_LEFT: (-1, 0),
              pygame.K_UP: (0, -1), pygame.K_DOWN: (0, 1)}

pygame.font.init()

class Camera:
    
    def __init__(self):
        self.dx = 0
        self.dy = 0
 
    def update(self, dx, dy):
        
        if self.dx + dx < 0 or self.dy + dy < 0 or self.dy + dy > 16 or self.dx + dx > 16:
            pass
        
        self.dx += dx
        self.dy += dy
        
        for sprite in sprites:
            sprite.moves(-dx, -dy)
            
        level.player.moves(dx, dy)
        

pygame.init()
size = width, height = 1280, 720
color = (0, 0, 0)
screen = pygame.display.set_mode(size)
running = True

board = Board(17, 17, screen)
level = Map(17, 17)
level.generateTerrain()
level.createGenerators(0.2)
level.readMap()
level.getMatrix()
level.getDijkstra()
heuristic_min_moves = level.getKruskal()
level.player.hp = evaluate(heuristic_min_moves, difficulty)

camera = Camera()

while running:
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        for key in pygame.K_RIGHT, pygame.K_LEFT, pygame.K_UP, pygame.K_DOWN:
            if pygame.key.get_pressed()[key]:
                camera.update(*directions[key])
                level.playerInteract()
        
    screen.fill((0, 0, 0))
    sprites.draw(screen)
    players.draw(screen)
    roads.draw(screen)
    pygame.draw.rect(screen, pygame.Color("Black"), (0, height - 100, width, 100), 0)
    myfont = pygame.font.SysFont('Courier', 60)
    textsurface = myfont.render(f'Energy to activate left: {level.player.hp}', 1, (0, 255, 0))    
    screen.blit(textsurface, (5, height - 90))
    pygame.display.flip()