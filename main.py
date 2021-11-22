

import pygame, sys, time, math, threading, os, random, copy
from pygame.locals import *

pygame.init()
WIDTH,HEIGHT=930,630
surface=pygame.display.set_mode((WIDTH,HEIGHT),0,32)
fps=100
ft=pygame.time.Clock()
pygame.display.set_caption('Snake')

UNIT = 15


class Home:
    def __init__(self,surface):
        self.surface=surface
        self.mouse=pygame.mouse.get_pos()
        self.click=pygame.mouse.get_pressed()
        self.color = {
            "background": [5, 50, 55, 210],
            "alpha": [5, 70, 65, 255],
            "snake": [20, 210, 30, 255],
            "food": [210, 30, 20, 255]
        }
        self.rows = HEIGHT//UNIT
        self.columns = WIDTH//UNIT
        self.snake = []
        self.create_snake()
        self.direction = [0, 0]
        self.last_updated_move = time.time()
        self.last_updated_direction = time.time()
        self.min_time_gap = 0.1
        self.food = None
        self.create_food()
    def create_food(self):
        food = [random.randint(0, self.columns-1), random.randint(0, self.rows-1)]
        while self.does_food_collides_with_snake(food):
            food = [random.randint(0, self.columns-1), random.randint(0, self.rows-1)]
        self.food = food[:]
    def does_food_collides_with_snake(self, food):
        if food[0]==self.snake[0] and food[1]==self.snake[1]:
            return True
    def create_snake(self):
        self.snake = [self.columns//2, self.rows//2]
    def draw_world(self):
        for i in range(self.rows):
            for j in range(self.columns):
                x = j*UNIT
                y = i*UNIT
                pygame.draw.rect(self.surface, self.color["alpha"], (x, y, UNIT, UNIT), 1)
    def draw_snake(self):
        x = self.snake[0]*UNIT
        y = self.snake[1]*UNIT
        pygame.draw.rect(self.surface, self.color["snake"], (x,y, UNIT, UNIT))
    def draw_food(self):
        x = self.food[0]*UNIT
        y = self.food[1]*UNIT
        pygame.draw.rect(self.surface, self.color["food"], (x,y, UNIT, UNIT))
    def move_snake(self):
        if (time.time()-self.last_updated_move)>self.min_time_gap:
            self.snake[0] += self.direction[0]
            self.snake[1] += self.direction[1]
            self.last_updated_move = time.time()
    def change_direction(self, direction):
        if (time.time()-self.last_updated_direction)>self.min_time_gap:
            self.direction = direction[:]
            self.last_updated_direction = time.time()
    def basic_operations(self):
        self.draw_world()
        self.draw_snake()
        self.draw_food()
        self.move_snake()
    def run(self):
        play=True
        while play:
            self.surface.fill(self.color["background"])
            self.mouse=pygame.mouse.get_pos()
            self.click=pygame.mouse.get_pressed()
            for event in pygame.event.get():
                if event.type==QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type==KEYDOWN:
                    if event.key==K_TAB:
                        play=False
                    elif event.key==K_SPACE:
                        self.create_snake()
                        # self.create_food()
                    elif event.key==K_RIGHT:
                        self.change_direction([1, 0])
                    elif event.key==K_LEFT:
                        self.change_direction([-1, 0])
                    elif event.key==K_UP:
                        self.change_direction([0, -1])
                    elif event.key==K_DOWN:
                        self.change_direction([0, 1])
            #--------------------------------------------------------------
            self.basic_operations()
            # -------------------------------------------------------------
            pygame.display.update()
            ft.tick(fps)


if __name__=="__main__":
    app = Home(surface)
    app.run()


# #----------------

