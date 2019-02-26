class Camera:
    
    def __init__(self, level, launchParams, sprites):
        self.sprites = sprites
        self.launchParams = launchParams
        self.level = level
        self.relativex = 3
        self.relativey = 3 # позиция относительно левого верхнего края окна
 
    def update(self, dx, dy): # сдвинуть игрока и камеру соответственно
        
        if dx != 0:
            
            if (1 < self.relativex + dx < self.launchParams["LIM_X"]) or not \
           (2 < self.level.player.x < self.launchParams["SIZEX"] - 3):
                self.relativex += dx
        
            else:
                for group in SPRITES:
                    for member in group:
                        member.moves(-dx, -dy)                
        else:
            
            if (1 < self.relativey + dy < self.launchParams["LIM_Y"]) or not \
           (2 < self.level.player.y < self.launchParams["SIZEY"] - 3):
                self.relativey += dy            
            
            else:
                for group in SPRITES:
                    for member in group:
                        member.moves(-dx, -dy)
                    
        self.level.player.moves(dx, dy, self.relativex, self.relativey)
    
    def shift_view(self, dx, dy): # сдвинуть камеру без движения игрока
        
        self.relativex -= dx
        self.relativey -= dy
        for group in self.sprites:
            for member in group:
                member.moves(-dx, -dy)
                
        self.level.player.moves(0, 0, self.relativex, self.relativey)