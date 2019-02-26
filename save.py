import time

def save_map(level):
    
    f = open(f"maps/{time.time()}.txt", "w")
    
    f.write(f"{level.exitCoords[0]} {level.exitCoords[1]} ")
    
    for y in range(level.width):
        for x in range(level.height):
            
            value = level.mapProfile.value[y][x]
            mount = level.mapProfile.mount[y][x]
            weather = level.mapProfile.weather[y][x]
            genmap = level.mapProfile.genmap[y][x]
            
            f.write(f"{value} {mount} {weather} {genmap}\n")
            
    f.close()