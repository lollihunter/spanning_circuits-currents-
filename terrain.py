properties = {
    "jungle": (5, True, -0.5),
    "water": (1, True, -0.5),
    "grass": (1, True, -0.5),
    "forest": (2, True, -0.5),
    "desert": (1, True, 0.25),
    "mountain": (10 ** 8, False, 0),
}

tile_paths = {
    "jungle": "jungle.png",
    "water": "empty.png",
    "grass": "empty.png",
    "grass_base": "grass.png",
    "forest": "forest.png",
    "desert": "desert.png",
    "generator": "generator/0.png",
    "player": "player.png",
    "mountain": "mountain.png"
}

worldgen = {
    "water": 0.4,
    "desert": 0.5,
    "grass": 0.6,
    "forest": 0.7,
    "jungle": 0.8,
    "mountain": 1,
}

class Tile:
    
    def __init__(self, id_tile):
        self.movementPoints, self.passable, self.drainEnergy = properties[id_tile]
        self.id_tile = id_tile
        self.exit = False
        self.generator = False
        self.activated = 0
        self.weather = "clear"
        
        
        