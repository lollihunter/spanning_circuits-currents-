from opensimplex import OpenSimplex
from random import random
gen = OpenSimplex()

def noise(nx, ny):
    return gen.noise2d(nx, ny) / 2.0 + 0.5

def generate(width, height):
    c1, c2 = random(), random()
    value, mount, weather, genmap = [], [], [], []
    for y in range(height):
        value.append([0] * width)
        mount.append([0] * width)
        weather.append([0] * width)
        genmap.append([0] * width)        
        for x in range(width):
            nx = x/width - 0.5 + c1
            ny = y/height - 0.5 + c2
            value[y][x] = noise(6 * nx, 6 * ny)
            mount[y][x] = noise(5 * nx, 5 * ny)
            weather[y][x] = noise(4 * nx, 4 * ny)
            genmap[y][x] = random()
            
    return value, mount, weather, genmap

def from_file(path, width, height):
    f = open(path).read().split()
    value, mount, weather, genmap = [], [], [], []
    cnt = 0
    for y in range(height):
        value.append([0] * width)
        mount.append([0] * width)
        weather.append([0] * width)
        genmap.append([0] * width)
        for x in range(width):
            value[y][x] = float(f[cnt])
            mount[y][x] = float(f[cnt + 1])
            weather[y][x] = float(f[cnt + 2])
            genmap[y][x] = float(f[cnt + 3])
            cnt += 4
            
    return value, mount, weather, genmap
    