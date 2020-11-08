#############################
# SNAKE GAME                #
# Carlos Caminero           #
# Contributors:             #
#   Javier Martinez         #
#############################

import pygame
import random
import time
from pygame.locals import *

random.seed(time.time())

WIDTH = 400
HEIGHT = 300
SQUARE_SIDE = 20

RIGHT=0
LEFT=1
UP=2
DOWN=3

LIGHT_GREEN = (168, 222, 53)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

rows = int(HEIGHT/20)
cols = int(WIDTH/20)

red_square = []

class Snake():
    def __init__(self):
        self.dir = RIGHT
        self.body = [[0, 0], [-20, 0], [-40, 0], [-60, 0]]
        self.eat_sound = pygame.mixer.Sound("sounds/eat_apple.wav")

    def move(self, objetive):
        global screen, score

        head = self.body[0]
        if self.dir == RIGHT:
            if self.body[0][0] < (WIDTH - SQUARE_SIDE):
                self.body.insert(0, [head[0] + SQUARE_SIDE, head[1]])
            else:
                return False
        if self.dir == LEFT:
            if self.body[0][0] > 0:
                self.body.insert(0, [head[0] - SQUARE_SIDE, head[1]])
            else:
                return False
        if self.dir == UP:
            if self.body[0][1] > 0:
                self.body.insert(0, [head[0], head[1] - SQUARE_SIDE])
            else:
                return False
        if self.dir == DOWN:
            if self.body[0][1] < (HEIGHT - SQUARE_SIDE):
                self.body.insert(0, [head[0], head[1] + SQUARE_SIDE])
            else:
                return False

        if self.body[0][0] == objetive[0][0] and self.body[0][1] == objetive[0][1]:
            self.eat(objetive)
            score += 1
            pygame.mixer.Sound.play(self.eat_sound)
            print(score)
        else:
            self.body.pop()
        return True

    def eat(self, objetive):
        objetive.pop()

    def set_direction(self, dir):
        self.dir = dir

    def get_direction(self):
        return self.dir

    def draw(self):
        global screen

        for coord in self.body:
            pygame.draw.rect(screen, LIGHT_GREEN, [coord[0],coord[1], SQUARE_SIDE, SQUARE_SIDE])

    def getHead(self):
        return self.body[0]

    def isAutoShock(self):
        return self.getHead() in self.body[1:]

    def showCoords(self):
        print(self.body)

def drawGrid():
    global screen

    for i in range(rows):
        for j in range(cols):
            xi = j*SQUARE_SIDE
            yi = i*SQUARE_SIDE
            xf = SQUARE_SIDE*(j+1)
            yf = SQUARE_SIDE*(i+1)
            pygame.draw.rect(screen, BLUE ,[xi,yi,xf,yf],1)

def generateSquare(square):
    x = random.randint(0, cols - 1)
    y = random.randint(0, rows - 1)
    square.append((x*SQUARE_SIDE, y*SQUARE_SIDE))

def draw_square(location, color):
    global screen
    pygame.draw.rect(screen, color, [location[0][0], location[0][1], SQUARE_SIDE, SQUARE_SIDE])

def draw_snake(snake):
    snake.draw()

def draw_background(color):
    screen.fill(color)

def game_init():
    global screen, snake, red_square

    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    snake = Snake()
    generateSquare(square=red_square)


if __name__ == "__main__":

    game_init()

    pygame.mixer.music.load("sounds/music.wav")
    pygame.mixer.music.play(-1)
    game_over_sound = pygame.mixer.Sound("sounds/game_over.wav")

    score = 0
    end = False
    clock = pygame.time.Clock()
    while not end:

        for event in pygame.event.get():
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    end = True
                if event.key == K_a and snake.get_direction() != RIGHT:
                    snake.set_direction(LEFT)
                elif event.key == K_d and snake.get_direction() != LEFT:
                    snake.set_direction(RIGHT)
                elif event.key == K_s and snake.get_direction() != UP:
                    snake.set_direction(DOWN)
                elif event.key == K_w and snake.get_direction() != DOWN:
                    snake.set_direction(UP)
                break # it avoids bug control (3 keys in time)

            elif event.type == QUIT:
                end = True

        # Moving the snake
        game_state = snake.move(objetive=red_square)

        if snake.isAutoShock():
            game_state = False

        # Test if GAME OVER
        if game_state == False:
            pygame.mixer.music.stop()
            pygame.mixer.Sound.play(game_over_sound)
            time.sleep(1)
            end = True

        # if there isn't Objetive square, it generates another
        if len(red_square) == 0:
            generateSquare(square=red_square)

        # Draw functions
        draw_background(color=WHITE)
        drawGrid()
        draw_snake(snake)
        draw_square(location=red_square, color=RED)
        pygame.display.flip()

        clock.tick(10)
    print("PUNCTUATION:", score)
