import pygame
from random import choice, random, randint
from terrain import *
from kruskal import *
from dijkstra import *
from handling import *
from camera import Camera
from math_thingies import *
from save import *
from cfgReader import *
import time

# Основные параметры

launchParams = {"fps": 24,
          "LIM_X": 8,
          "LIM_Y": 4,
          "SIZEX": 10, # размер в ширину
          "SIZEY": 6, # размер в длину
          "difficulty": 3, # чем меньше - тем сложнее
          "CHANCE": 0.12} # шанс генерации генератора

configParams = cfgRead()
# прочитать settings.cfg и попытаться заменить дефолтные значения

overrideConfig(launchParams, configParams)
            
result = 0
SPRITES = [sprites, roads, base, weathers]
directions = {pygame.K_RIGHT: (1, 0), pygame.K_LEFT: (-1, 0),
              pygame.K_UP: (0, -1), pygame.K_DOWN: (0, 1),
              pygame.K_d: (1, 0), pygame.K_a: (-1, 0),
              pygame.K_w: (0, -1), pygame.K_s: (0, 1),} # передвижение по полю при нажатии кнопки

pygame.font.init()


def screenShow(text, result=0):
    
    introText = ["Spanning Currents", "",
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
    
    lossText = ["Вы проиграли!",
           f"Активировано {level.cntActive} генераторов из {level.cntGens}"]
    
    winText = ["Вы выиграли!",
           f"Активированы все генераторы: {level.cntGens}",
           f"Затрачено {initial - level.player.hp} энергии; лучший возможный результат составляет примерно {heuristic_min_moves}",
           "Поздравляем!"]
     
    if text == "start":
        displayText = introText
    elif text == "end" and result == 1:
        displayText = lossText
    else:
        displayText = winText
     
    fon = pygame.transform.scale(load_image('fon.jpg'), (WIDTH, HEIGHT))
    screen.blit(fon, (0, 0))
    font = pygame.font.SysFont("Arial", 20)
    text_coord = 80
    for line in displayText:
        string_rendered = font.render(line, 1, pygame.Color('black'))
        displayRect = string_rendered.get_rect()
        text_coord += 10
        displayRect.top = text_coord
        displayRect.x = 100
        text_coord += displayRect.height
        screen.blit(string_rendered, displayRect)
 
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN or \
                    event.type == pygame.MOUSEBUTTONDOWN:
                return
        pygame.display.flip()
        clock.tick(launchParams["fps"])


def check_bounds(x, y): # проверить возможность прохождения клетки
    global levels
    return (0 <= x + level.player.x < launchParams["SIZEX"] and
            0 <= y + level.player.y < launchParams["SIZEY"] and
            level.level[x + level.player.x][y + level.player.y].passable)


def update_gui(): # здоровье, энергия, количество генераторов
    myfont = pygame.font.SysFont('Arial Black', 20)
    text1 = myfont.render(f"{level.player.hp}", False, (255, 255, 255))
    text2 = myfont.render(f"{level.cntGens - level.cntActive}", False, (255, 255, 255))
    text3 = myfont.render(f"{int(level.player.health)}", False, (255, 255, 255))
    screen.blit(text1, (180, HEIGHT - 75))
    screen.blit(text2, (340, HEIGHT - 75))
    screen.blit(text3, (100, HEIGHT - 75))
        

def game_finished(): # определить исход игры при ее завершении
    global result
    if level.cntGens == level.cntActive and (level.player.x, level.player.y) == level.exit:
        result = 2    
    if (level.player.hp <= 0 or level.player.health <= 0
        and not (level.cntGens == level.cntActive and (level.player.x, level.player.y) == level.exit 
        and level.player.hp == 0)):
        result = 1  
    return result

   
pygame.init()
size = WIDTH, HEIGHT = 97 * 10, 97 * 6
color = (0, 0, 0)
screen = pygame.display.set_mode(size)
running = True

level = Map(launchParams["SIZEX"], launchParams["SIZEY"])
level.generateTerrain()
level.createGenerators(launchParams["CHANCE"])
level.createWeather()
level.readMap()
level.getMatrix()
level.getDijkstra()
heuristic_min_moves = level.getKruskal()
print(heuristic_min_moves)
initial = level.player.hp = evaluate(heuristic_min_moves, launchParams["difficulty"])
level.player.health = 100

camera = Camera(level, launchParams, SPRITES)
clock = pygame.time.Clock()

screenShow("start")

while running:    
    
    clock.tick(launchParams["fps"])
    
    for event in pygame.event.get():
        
        if event.type == pygame.QUIT:
            running = False
            
        if pygame.key.get_pressed()[pygame.K_q]:
            save_map(level)
            
        for key in pygame.K_RIGHT, pygame.K_LEFT, pygame.K_UP, pygame.K_DOWN: # сдвинуть игрока
            if pygame.key.get_pressed()[key]:
                if not check_bounds(*directions[key]):
                    break
                camera.update(*directions[key])
                level.playerInteract() # поменять клетки на поле
                level.updateGens() # обновить работоспособность генератора               
                
                
        for key in pygame.K_w, pygame.K_a, pygame.K_s, pygame.K_d: # сдвинуть камеру
            if pygame.key.get_pressed()[key]:
                camera.shift_view(*directions[key])    
                
    # обновить спрайты    
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
    
    # перенести спрайты        
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
        screenShow("end", result)
        pygame.display.flip()
        