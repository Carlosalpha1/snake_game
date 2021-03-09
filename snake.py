#!/usr/bin/python3

#############################
# SNAKE GAME                #
# Carlos Caminero           #
# Contributors:             #
#   Javier Martinez         #
#############################

import pygame
import pygame_menu
import random
import time
import sys
from pygame.locals import *

random.seed(time.time())

#############
# AUTO VARIABLES
#############

WIDTH = 400
TOTAL_HEIGHT = 400
GRID_HEIGHT = 300
LABEL_SCORE_HEIGTH = TOTAL_HEIGHT-GRID_HEIGHT
SQUARE_SIDE = 20

RIGHT=0
LEFT=1
UP=2
DOWN=3

BLACK = (0,0,0)
LIGHT_GREEN = (168, 222, 53)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

rows = int(GRID_HEIGHT/20)
cols = int(WIDTH/20)

red_square = []

score = 0

checkpoint_sound = 0
game_over_sound = 0

class Snake():
    def __init__(self):
        self.dir = RIGHT
        self.body = [[0, 0], [-20, 0], [-40, 0], [-60, 0]]
        self.eat_sound = pygame.mixer.Sound(eat_apple_sound_path)

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
            if self.body[0][1] < (GRID_HEIGHT - SQUARE_SIDE):
                self.body.insert(0, [head[0], head[1] + SQUARE_SIDE])
            else:
                return False

        if self.body[0][0] == objetive[0][0] and self.body[0][1] == objetive[0][1]:
            self.eat(objetive)
            score += 1
            if(score%10 == 0 and score != 0):
                pygame.mixer.Sound.play(checkpoint_sound)
            pygame.mixer.Sound.play(self.eat_sound)
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

def show_score(text):
    font = pygame.font.Font('freesansbold.ttf', 32)
    render_text = font.render(text, True, BLACK)
    text_rect = render_text.get_rect(center=(WIDTH/2, TOTAL_HEIGHT-(LABEL_SCORE_HEIGTH/2)))
    screen.blit(render_text, text_rect)

def show_checkpoint(text):
    font = pygame.font.Font('freesansbold.ttf', 75)
    render_text = font.render(text, True, RED)
    text_rect = render_text.get_rect(center=(WIDTH/2, TOTAL_HEIGHT-(LABEL_SCORE_HEIGTH/2)))
    screen.blit(render_text, text_rect)

def draw_label_score():
    pygame.draw.rect(screen, WHITE, [0, GRID_HEIGHT, WIDTH, TOTAL_HEIGHT])
    if(score%10 == 0 and score != 0):
        show_checkpoint(str(score))
    else:
        show_score("Score: "+str(score))

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
    """ initializing parameters """
    global snake, red_square, score, checkpoint_sound, game_over_sound

    checkpoint_sound = pygame.mixer.Sound(checkpoint_sound_path)
    game_over_sound = pygame.mixer.Sound(game_over_sound_path)
    score = 0
    snake = Snake()
    generateSquare(square=red_square)

def game_loop():
    """ the principal loop of game """
    global score

    pygame.mixer.music.load(music_sound_path)
    pygame.mixer.music.play(-1)

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
        draw_label_score()
        pygame.display.flip()

        clock.tick(10)
    red_square.pop()


# MAIN FUNCTION
if __name__ == "__main__":

    pygame.init()
    screen = pygame.display.set_mode((WIDTH, TOTAL_HEIGHT))
    def start_game():
        game_init()
        game_loop()

    menu = pygame_menu.Menu(TOTAL_HEIGHT, WIDTH, "SNAKE", theme=pygame_menu.themes.THEME_BLUE)
    menu.add_button('Play', start_game)
    menu.add_button('Quit', pygame_menu.events.EXIT)

    menu.mainloop(screen)
