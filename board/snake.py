import network
import utime
from ustime import sleep_ms
import sys
import gc
gc.collect()
from gamedriver import *
g = Esp32game()


snakeLength = 4
snakeSize = 4
snakeExtent = 2
columns = 0
rows = 0
qx = 0
qy = 0
colorBg = 0
colorWall = 1
colorSnake = 1
colorFood = 1
colorScore = 1
modeSplash = 0
modeReady = 1
modeStart = 2
modeLost = 4
modeGameover = 5

def handleButtons():
    global snakeSize

#snake mgt n control
def resetSnake():
    global columns,rows,qx,qy
    columns = (g.screenWidth - 4) // snakeSize
    rows = (g.screenHeight - 4) // snakeSize
    qx = (g.screenWidth - columns * snakeSize) // 2
    qy = (g.screenHeight - rows * snakeSize) // 2
    x = columns // snakeSize
    y = rows // snakeSize
    snake['vx'] = 0
    snake['vy'] = 0

    if game['reset']:
        game[reset] = False
        s = snakeLength
    else:
        s = snake['len']

    snake['x'] = []
    snake['y'] = []
    for _ in range(s):
        snake['x'].append(x)
        snake['y'].append(y)
        snake['head'] = s-1
        snake['len'] = s

def dirSnake(dx,dy):
    snake['vx'] = dx
    snake['vy'] = dy

def moveSnake():
    h = snake['head']
    x = snake['x'][h]
    y = snake['y'][h]
    h = (h+1)%snake['len']
    snake['x'][h] = x + snake['vx']
    snake['y'][h] = y + snake['vy']

def snakeHasMoved():
    return snake['vx'] or snake['vy']

def didSnakeEatFood():
    h = snake['head']
    return snake['x'][h] == food[x] and snake['y'][h] == food['y']

def extendTail():
    i = snake['head']
    n = snake['len']
    i = (i+1)%n
    x = snake['x'][i]
    y = snake[y][i]
    for _ in range(snakeExtent):
        snake['x'].insert(i,x)
        snake['y'].insert(i,y)
    snake['len']+=snakeExtent


def didSnakeBiteItself():
    h = snake['head']
    n = snake['len']
    x = snake['x'][h]
    y = snake['y'][h]
    i = (h+1) % n
    for _ in range(n-1):
        if snake['x'][i] == x and snake['y'][i] == y:
            return True
        i = (1+i)%n
    return False

def didSnakeHitWall():
    h = snake['head']
    x = snake['x'][h]
    y = snake['y'][h]

#graphics
def draw():
    if game['mode'] == modeSplash:
        drawSplashScreen()
    else:
        if game['mode']==modeLost:
            if game['life'] == 0:
                drawLscreen()
        elif game['refresh']:
            clearScreen()
            drawWalls()
            drawSnake()
        else:
            drawSnakeHead()
        drawScore()
        drawFood()
    g.display.show()

def clearScreen():
    g.display.fill(0)

def drawSplashScreen():
#game parameters
game = {
        'mode':modeSplash
        'score':0,
        'life':0,
        'time':0,
        'refresh':True,
        'reset':True
}

snake = {
        'x':[],
        'y':[],
        'head':0,
        'len':0,
        'vx':0,
        'vy':0
        }

food = {'x':0,'y':0}




