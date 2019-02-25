import pygame
from random import choice, random, randint
from terrain import *
from kruskal import *
from dijkstra import *
from sprites import *


class Board:
    
    
    def __init__(self, height, width, screen):
        
        self.width = width
        self.height = height
        self.left = 0
        self.top = 0
        self.cell_size = 80
        self.screen = screen
 
 
    def set_view(self, left, top, cell_size):
        
        self.left = left
        self.top = top
        self.cell_size = cell_size
        
        
    def repopulate(self, level):
        
        for i in range(self.width):
            for j in range(self.height):
                tile_type = level.level[i][j].id_tile
                loc = (self.left + j * self.cell_size,
                        self.top + i * self.cell_size)

class Map:
    
    
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.level = [[0] * height for _ in range(width)]
        self.roadmap = [[0] * height for _ in range(width)]
        
    
    def convert(self, i, j):
        return self.height * i + self.width
    
        
    def generateTerrain(self):
        
        for i in range(self.width):
            for j in range(self.height):
                self.level[i][j] = Tile(choice(list(properties.keys())))
    
    
    def createWeather(self):
        
        for i in range(self.width):
            for j in range(self.height):
                self.level[i][j].weather = Weather(choice(conditions))
                
                
    def createEntities(self):
        
        for i in range(self.width):
            for j in range(self.height):
                self.level[i][j].entity = Entity(choice(conditions))
    
    
    def createGenerators(self, chance):
        
        for i in range(self.width):
            for j in range(self.height):
                if random() < chance:
                    self.level[i][j].generator = True
                    
    def readMap(self):
        
        for i in range(self.width):
            for j in range(self.height):
                tile = self.level[i][j]
                tile_type = tile.id_tile
                sprites.add(TileSprite(tile_type, i, j))
                roads.add(Road(i, j, self))
                if tile.generator:
                    sprites.add(TileSprite("generator", i, j))
        self.entry = (0, randint(0, self.height - 1))
        self.exit = (self.width - 1, randint(0, self.height - 1))
        self.player = Player(*self.entry)        
        players.add(self.player)
    
    
    def getMatrix(self):
        
        self.matrix = [[0] * self.height for _ in range(self.width)]
        for i in range(self.width):
            for j in range(self.height):
                self.matrix[i][j] = self.level[i][j].movementPoints
    
        
    def getDijkstra(self):
        
        cntGen = 0
        self.edges, self.gens = [], [self.entry, self.exit]
        
        
        for i in range(self.width):
            for j in range(self.height):
                cntGen += self.level[i][j].generator
                if self.level[i][j].generator is True:
                    self.gens.append((i, j))            
        
        for gen in range(len(self.gens)):
            initDijkstra(self.width, self.height)
            g = self.gens[gen]
            res = Dijkstra((g[0], g[1]), self.matrix)
            for i in range(len(res)):
                for j in range(len(res[i])):
                    if (i, j) in self.gens and (i, j) != self.gens[gen]:
                        self.edges.append(Edge(gen, self.gens.index((i, j)), res[i][j]))
                        
                        
    def getKruskal(self):
        initDSU(len(self.gens))
        return Kruskal(self.edges)
    
    
    def playerInteract(self):
        x, y = self.player.x, self.player.y
        self.player.hp -= self.level[x][y].movementPoints
        self.level[x][y].movementPoints = 0
        self.roadmap[x][y] = 1
        for road in roads:
            road.update()
         