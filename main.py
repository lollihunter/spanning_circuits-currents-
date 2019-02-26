import pygame
from random import choice, random, randint
from terrain import *
from kruskal import *
from dijkstra import *
from handling import *
from math_thingies import *
from save import *
from cfgReader import *
import time


params = {"fps": 24,
          "LIM_X": 8,
          "LIM_Y": 4,
          "SIZEX": 10,
          "SIZEY": 6,
          "difficulty": 3,
          "CHANCE": 0.12}

params_cfg = cfgread()
for param in params:
    try:
        params[param] = params_cfg[param]
    except KeyError:
        pass
        
    
result = 0
SPRITES = [sprites, roads, base, weathers]
directions = {pygame.K_RIGHT: (1, 0), pygame.K_LEFT: (-1, 0),
              pygame.K_UP: (0, -1), pygame.K_DOWN: (0, 1),
              pygame.K_d: (1, 0), pygame.K_a: (-1, 0),
              pygame.K_w: (0, -1), pygame.K_s: (0, 1),}

pygame.font.init()


class Camera:
    
    def __init__(self):
        self.relativex = 3
        self.relativey = 3
 
    def update(self, dx, dy):
        
        if dx != 0:
            
            if (1 < self.relativex + dx < params["LIM_X"]) or not \
           (2 < level.player.x < params["SIZEX"] - 3):
                self.relativex += dx
        
            else:
                for group in SPRITES:
                    for member in group:
                        member.moves(-dx, -dy)                
        else:
            
            if (1 < self.relativey + dy < params["LIM_Y"]) or not \
           (2 < level.player.y < params["SIZEY"] - 3):
                self.relativey += dy            
            
            else:
                for group in SPRITES:
                    for member in group:
                        member.moves(-dx, -dy)
                    
        level.player.moves(dx, dy, self.relativex, self.relativey)
    
    def shift_view(self, dx, dy):
        
        self.relativex -= dx
        self.relativey -= dy
        for group in SPRITES:
            for member in group:
                member.moves(-dx, -dy)
                
        level.player.moves(0, 0, self.relativex, self.relativey)
        


def check_bounds(x, y):
    global levels
    return (0 <= x + level.player.x < params["SIZEX"] and
            0 <= y + level.player.y < params["SIZEY"] and
            level.level[x + level.player.x][y + level.player.y].passable)


def update_gui():
    myfont = pygame.font.SysFont('Arial Black', 20)
    text1 = myfont.render(f"{level.player.hp}", False, (255, 255, 255))
    text2 = myfont.render(f"{level.cntGens - level.cntActive}", False, (255, 255, 255))
    text3 = myfont.render(f"{int(level.player.health)}", False, (255, 255, 255))
    screen.blit(text1, (180, HEIGHT - 75))
    screen.blit(text2, (340, HEIGHT - 75))
    screen.blit(text3, (100, HEIGHT - 75))
        

def game_finished():
    global result
    if level.cntGens == level.cntActive and (level.player.x, level.player.y) == level.exit:
        result = 2    
    if (level.player.hp <= 0 or
        level.player.health <= 0):
        result = 1
    if level.cntGens == level.cntActive and (level.player.x, level.player.y) == level.exit and level.player.hp == 0:
        result = 2  
    return result

   
pygame.init()
size = WIDTH, HEIGHT = 97 * 10, 97 * 6
color = (0, 0, 0)
screen = pygame.display.set_mode(size)
running = True

level = Map(params["SIZEX"], params["SIZEY"])
level.generateTerrain()
level.createGenerators(params["CHANCE"])
level.createWeather()
level.readMap()
level.getMatrix()
level.getDijkstra()
heuristic_min_moves = level.getKruskal()
print(heuristic_min_moves)
initial = level.player.hp = evaluate(heuristic_min_moves, params["difficulty"])
level.player.health = 100

camera = Camera()
clock = pygame.time.Clock()


def start_screen():
    intro_text = ["Spanning Currents", "",
                  "Правила игры",
                  "Вы попали на необитаемую планету, и ваш телепорт перестал работать.",
                  "К счастью, его можно вернуть к жизни, если включить генераторы.",
                  "Идя за собой, вы прокладываете дорогу. Прокладывание дороги по определенной",
                  "местности забирает некоторое количество энергии из вашего джетпака.",
                  "Затем по дороге можно передвигаться свободно. Вы не можете двигаться по горам.",
                  "Вам необходимо успеть включить все генераторы, пока ваш джетпак не разрядился.",
                  "Проливные дожди и грозы будут тушить генераторы через определенное количество ходов.",
                  "",
                  "Сложность игры и размер игрового поля могут быть редактированы в файле конфигурации.",]
 
    fon = pygame.transform.scale(load_image('fon.jpg'), (WIDTH, HEIGHT))
    screen.blit(fon, (0, 0))
    font = pygame.font.SysFont("Arial", 20)
    text_coord = 80
    for line in intro_text:
        string_rendered = font.render(line, 1, pygame.Color('black'))
        intro_rect = string_rendered.get_rect()
        text_coord += 10
        intro_rect.top = text_coord
        intro_rect.x = 100
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)
 
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN or \
                    event.type == pygame.MOUSEBUTTONDOWN:
                return
        pygame.display.flip()
        clock.tick(params["fps"])
        
def end_screen():
    
    LOSS = ["Вы проиграли!",
           f"Активировано {level.cntActive} генераторов из {level.cntGens}"]
    
    WIN = ["Вы выиграли!",
           f"Активированы все генераторы: {level.cntGens}",
           f"Затрачено {initial - level.player.hp} энергии; лучший возможный результат составляет примерно {heuristic_min_moves}",
           "Поздравляем!"]
 
    fon = pygame.transform.scale(load_image('fon.jpg'), (WIDTH, HEIGHT))
    screen.blit(fon, (0, 0))
    font = pygame.font.SysFont("Arial", 20)
    text_coord = 80
    intro_text = LOSS if result == 1 else WIN
    for line in intro_text:
        string_rendered = font.render(line, 1, pygame.Color('black'))
        intro_rect = string_rendered.get_rect()
        text_coord += 10
        intro_rect.top = text_coord
        intro_rect.x = 100
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)
    pygame.display.flip()
    time.sleep(5)

start_screen()

while running:    
    
    clock.tick(params["fps"])
    
    for event in pygame.event.get():
        
        if event.type == pygame.QUIT:
            running = False
            
        if pygame.key.get_pressed()[pygame.K_q]:
            save_map(level)
            
        for key in pygame.K_RIGHT, pygame.K_LEFT, pygame.K_UP, pygame.K_DOWN:
            if pygame.key.get_pressed()[key]:
                if not check_bounds(*directions[key]):
                    break
                camera.update(*directions[key])
                level.playerInteract()
                level.updateGens()                
                
                
        for key in pygame.K_w, pygame.K_a, pygame.K_s, pygame.K_d:
            if pygame.key.get_pressed()[key]:
                camera.shift_view(*directions[key])    
                
        
    screen.fill((0, 0, 0))
    for bases in base:
        if type(bases) == WaterSprite:
            bases.moves(0, 0)
    for sprite in sprites:
        if type(sprite) in [GeneratorSprite, ExitSprite]:
            sprite.moves(0, 0)
    for w in weathers:
        w.moves(0, 0)
    level.player.upd()
            
    base.draw(screen)
    sprites.draw(screen)
    players.draw(screen)
    weathers.draw(screen)
    roads.draw(screen)
    im = load_image("gui.png")   
    screen.blit(im, (40, HEIGHT - 90))
    update_gui()
    pygame.display.flip()
    
    if game_finished():
        running = False
        end_screen()
        pygame.display.flip()
        