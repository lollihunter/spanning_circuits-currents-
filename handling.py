import pygame
from random import choice, random, randint
from terrain import *
from kruskal import *
from dijkstra import *
from sprites import *
from math_thingies import get_starting_pixel
from noise_generation import *
from cfgReader import *



custom = True
terrainData = cfgRead()

try: # Try to read map file data from config; if MAP = -1, then random generate
    path = terrainData["MAP"]
    assert path != "-1"
except Exception:
    custom = False
    
moisture = {"thunder": 0.7}
overrideConfig(moisture, terrainData)
moisture = moisture["thunder"]



class Map:
    
    
    def __init__(self, width, height):
        
        self.width = width
        self.height = height
        self.cntGens = 0
        self.cntActive = 0
        
        if custom:
            self.mapProfile, self.exitCoords = from_file(path, self.height, self.width)
        else:    
            self.exitCoords = (self.width - 1, randint(0, self.height - 1))            
            self.mapProfile = generate(self.height, self.width)
        
        self.level = [[0] * height for _ in range(width)]
        self.roadmap = [[0] * height for _ in range(width)]
        
    
    def convert(self, i, j):
        
        return self.height * i + self.width
    
        
    def generateTerrain(self):
        
        for i in range(self.width):
            for j in range(self.height):
                for k in worldgen:
                    if self.mapProfile.value[i][j] < worldgen[k]: 
                        self.level[i][j] = Tile(k)
                        break
    
    
    def createWeather(self):
        
        for i in range(self.width):
            for j in range(self.height):
                if self.mapProfile.weather[i][j] > moisture and self.level[i][j].generator:
                    self.level[i][j].weather = "thunder"
                
    
    def createGenerators(self, chance):
        
        for i in range(self.width):
            for j in range(self.height):
                if self.mapProfile.genmap[i][j] < chance and not self.level[i][j].id_tile in ["water", "mountain"]:
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
                
        self.exit = self.exitCoords
        self.level[self.exitCoords[0]][self.exitCoords[1]] = Tile("grass")
        
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
        self.genMovementPoints = 0
        
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
                        self.edges.append(Edge(gen, self.gens.index((i, j)), res[i][j] - self.matrix[i][j]))
        
        for gen in set(self.gens):
            self.genMovementPoints += self.matrix[gen[0]][gen[1]]
                        
    def getKruskal(self):
        
        initDSU(len(self.gens))
        return Kruskal(self.edges) + self.genMovementPoints
    
    
    def playerInteract(self):
        
        x, y = self.player.x, self.player.y
        self.player.health = min(100, self.player.health - self.level[x][y].drainEnergy * 100)
        self.player.hp -= self.level[x][y].movementPoints
        if self.level[x][y].id_tile == "water":
            self.level[x][y].movementPoints = 1
        else:
            self.roadmap[x][y] = 1
            self.level[x][y].movementPoints = 0            
        self.level[x][y].activated = int(0.9 * (self.width + self.height) ** 1.07)
        for road in roads:
            road.update()
         