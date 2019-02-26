from opensimplex import OpenSimplex
from random import random
gen = OpenSimplex()


class MapProfile: # represent all float values for generation as class
    
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.value, self.mount, self.weather, self.genmap = (
            [[0] * width for _ in range(height)], # biome data
            [[0] * width for _ in range(height)], # dev
            [[0] * width for _ in range(height)], # weather data
            [[0] * width for _ in range(height)]) # generator data

    def update(self, i, j, value, mount, weather, genmap):
        self.value[i][j], self.mount[i][j], self.weather[i][j], self.genmap[i][j] = (
            float(value), float(mount), float(weather), float(genmap))


def noise(nx, ny): # generate noisemap
    return gen.noise2d(nx, ny) / 2.0 + 0.5


def generate(width, height):
    
    mapProfile = MapProfile(width, height)
    c1, c2 = random(), random() # make generation more random
    
    for y in range(height):       
        for x in range(width):
            nx = x / width - 0.5 + c1
            ny = y / height - 0.5 + c2
            mapProfile.update(y, x,
                              noise(6 * nx, 6 * ny),
                              noise(5 * nx, 5 * ny),
                              noise(4 * nx, 4 * ny),
                              random())
            
    return mapProfile


def from_file(path, width, height):
    
    mapProfile = MapProfile(width, height)
    
    f = open(path).read().split()
    exitPosition = int(f[0]), int(f[1]) # first two coords = exit position
    
    for y in range(height):
        for x in range(width):
            shift = 4 * (y * width + x) + 2
            mapProfile.update(y, x, f[shift], f[shift + 1], f[shift + 2], f[shift + 3])
            
    return mapProfile, exitPosition
    