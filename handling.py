import pygame
from random import choice, random, randint
from terrain import *
from kruskal import *
from dijkstra import *
from sprites import *
from math_thingies import get_starting_pixel
from noise_generation import *


custom = True

with open("cfg/settings.cfg") as a:
    try:
        a = a.readlines()
        path = a[7].split("=")[-1].strip()
        print(path)
        assert path.startswith("maps")
    except Exception:
        custom = False
        

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
        self.cntGens = 0
        self.cntActive = 0
        if custom:
            self.values, self.mount, self.weather, self.genmap = from_file(path, self.height, self.width)
        else:    
            self.values, self.mount, self.weather, self.genmap = generate(self.height, self.width)
        self.level = [[0] * height for _ in range(width)]
        self.roadmap = [[0] * height for _ in range(width)]
        
    
    def convert(self, i, j):
        return self.height * i + self.width
    
        
    def generateTerrain(self):
        for i in range(self.width):
            for j in range(self.height):
                for k in worldgen:
                    if self.values[i][j] < k: 
                        self.level[i][j] = Tile(worldgen[k])
                        break
    
    
    def createWeather(self):
        for i in range(self.width):
            for j in range(self.height):
                if self.values[i][j] > 0.7 and self.level[i][j].generator:
                    self.level[i][j].weather = "thunder"
                
    
    def createGenerators(self, chance):
        
        for i in range(self.width):
            for j in range(self.height):
                if self.genmap[i][j] < chance and not self.level[i][j].id_tile in ["water", "mountain"]:
                    self.level[i][j].generator = True
                    self.cntGens += 1
    
    
    def updateGens(self):
        
        self.cntActive = 0
        for i in range(self.width):
            for j in range(self.height):
                if self.level[i][j].generator and self.level[i][j].weather == "thunder":
                    self.level[i][j].activated = max(self.level[i][j].activated - 1, 0)
                if self.level[i][j].generator and self.level[i][j].activated > 0:
                    self.cntActive += 1            
                
                    
    def readMap(self):
        
        for i in range(self.width):
            for j in range(self.height):
                tile = self.level[i][j]
                tile_type = tile.id_tile
                
                if tile_type == "water":
                    base.add(WaterSprite("water_base", i, j))
                else:
                    base.add(BaseSprite("grass_base", i, j))
                
                sprites.add(TileSprite(tile_type, i, j))
                roads.add(Road(i, j, self))
                
                if tile.generator:
                    sprites.add(GeneratorSprite(i, j, self.level))
                    
                if tile.weather == "thunder":
                    weathers.add(ThunderSprite("thunder", i, j))
                
        self.entry = (3, 3)
        self.roadmap[3][3] = 1
        self.exit = (self.width - 1, randint(0, self.height - 1))
        sprites.add(ExitSprite(*self.exit, self))
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
        self.player.health = min(100, self.player.health - self.level[x][y].drainEnergy * 100)
        self.player.hp -= self.level[x][y].movementPoints
        if self.level[x][y].id_tile == "water":
            self.level[x][y].movementPoints = 1
        else:
            self.roadmap[x][y] = 1
            self.level[x][y].movementPoints = 0            
        self.level[x][y].activated = int(0.8 * (self.width + self.height) ** 1.3)
        for road in roads:
            road.update()
         