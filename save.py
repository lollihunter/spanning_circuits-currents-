import time

def save_map(level):
    
    f = open(f"maps/{time.time()}.txt", "w")
    
    f.write(f"{level.exit_coords[0]} {level.exit_coords[1]} ")
    
    for y in range(level.width):
        for x in range(level.height):
            f.write(str(level.values[y][x]))
            f.write(' ')
            f.write(str(level.mount[y][x]))
            f.write(' ')
            f.write(str(level.weather[y][x]))
            f.write(' ')
            f.write(str(level.genmap[y][x]))
            f.write(' ')
    
    f.close()