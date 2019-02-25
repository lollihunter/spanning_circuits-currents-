properties = {
    "jungle": (3, True, 0),
    "water": (1, True, 0),
    "grass": (1, True, 0),
    "forest": (2, True, 0),
    "desert": (1, True, 0.25),
}

tile_paths = {
    "jungle": "jungle.png",
    "water": "water.png",
    "grass": "grass.png",
    "forest": "forest.png",
    "desert": "desert.png",
    "generator": "generator.png",
    "player": "player.png",
}

class Tile:
    
    def __init__(self, id_tile):
        self.movementPoints, self.passable, self.drainEnergy = properties[id_tile]
        self.id_tile = id_tile
        self.exit = False
        self.generator = False
        
        
        