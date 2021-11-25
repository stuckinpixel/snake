

import pygame, sys, time, random
from pygame.locals import *


class Snake:
    def __init__(self, width=300, height=100, rows=20, columns=20, min_time_gap=0.1):
        self.check_errors_at_init(width=width, height=height, rows=rows, columns=columns, min_time_gap=min_time_gap)
        self.WIDTH = width
        self.HEIGHT = height
        self.rows = rows
        self.columns = columns
        self.unit_row = self.HEIGHT/self.rows
        self.unit_column = self.WIDTH/self.columns
        self.snake = [[]]
        self.create_snake()
        self.direction = [0, 0]
        self.last_updated_move = time.time()
        self.last_updated_direction = time.time()
        self.min_time_gap = min_time_gap
        self.food = None
        self.create_food()
        self.eaten_for_now = False
        self.sample_actions = [
            [1, 0],
            [0, 1],
            [-1, 0],
            [0, -1]
        ]
        self.graphic_initialized = False
        self.failed = False
    def __init__for_render(self):
        pygame.init()
        surface=pygame.display.set_mode((self.WIDTH,self.HEIGHT),0,32)
        self.fps=100
        self.ft=pygame.time.Clock()
        pygame.display.set_caption('Snake')
        self.surface=surface
        self.mouse=pygame.mouse.get_pos()
        self.click=pygame.mouse.get_pressed()
        self.color = {
            "background": [5, 50, 55, 210],
            "alpha": [5, 70, 65, 255],
            "snake": [20, 210, 30, 255],
            "food": [210, 30, 20, 255]
        }
        self.graphic_initialized = True
    def check_errors_at_init(self, width, height, rows, columns, min_time_gap):
        range_values = {
            "width": {
                "min": 100,
                "max": 1200
            },
            "height": {
                "min": 100,
                "max": 1200
            },
            "rows": {
                "min": 2,
                "max": height
            },
            "columns": {
                "min": 2,
                "max": width
            }
        }
        error_message = ""
        if not range_values["width"]["min"]<=width<=range_values["width"]["max"]:
            error_message += "width should be in the range of {} and {}\n". format(range_values["width"]["min"], range_values["width"]["max"])
        if not range_values["height"]["min"]<=height<=range_values["height"]["max"]:
            error_message += "height should be in the range of {} and {}\n". format(range_values["height"]["min"], range_values["height"]["max"])
        if not range_values["rows"]["min"]<=rows<=range_values["rows"]["max"]:
            error_message += "rows should be in the range of 2 and height\n"
        if not range_values["columns"]["min"]<=columns<=range_values["columns"]["max"]:
            error_message += "columns should be in the range of 2 and width\n"
        if len(error_message)>0:
            print ("\nERROR:")
            print (error_message)
            sys.exit()
    def create_food(self):
        food = [random.randint(0, self.columns-1), random.randint(0, self.rows-1)]
        while self.does_point_collides_with_snake(food):
            food = [random.randint(0, self.columns-1), random.randint(0, self.rows-1)]
        self.food = food[:]
    def does_point_collides_with_snake(self, point):
        for body_part in self.snake:
            if point[0]==body_part[0] and point[1]==body_part[1]:
                return True
        return False
    def does_food_collides_with_snake(self, food):
        if food[0]==self.snake[0][0] and food[1]==self.snake[0][1]:
            return True
        return False
    def does_snake_collides_with_itself(self):
        head = self.snake[0][:]
        for body_part in self.snake[1:]:
            if body_part[0]==head[0] and body_part[1]==head[1]:
                return True
        return False
    def does_snake_collides_with_walls(self):
        head = self.snake[0][:]
        if (head[0]<0 or head[0]>=self.columns) or (head[1]<0 or head[1]>=self.rows):
            return True
        return False
    def create_snake(self):
        head = [self.columns//2, self.rows//2]
        self.snake = [head[:]]
    def opposite_direction(self, mat):
        return [mat[0]*(-1), mat[1]*(-1)]
    def are_same(self, mat1, mat2):
        if mat1[0]==mat2[0] and mat1[1]==mat2[1]:
            return True
        return False
    def draw_world(self):
        for i in range(self.rows):
            for j in range(self.columns):
                x = j*self.unit_column
                y = i*self.unit_row
                pygame.draw.rect(self.surface, self.color["alpha"], (x, y, self.unit_column, self.unit_row), 1)
    def draw_snake(self):
        for body_part in self.snake:
            x = body_part[0]*self.unit_column
            y = body_part[1]*self.unit_row
            pygame.draw.rect(self.surface, self.color["snake"], (x,y, self.unit_column, self.unit_row))
    def sample_action(self):
        return random.choice(self.sample_actions)
    def draw_food(self):
        x = self.food[0]*self.unit_column
        y = self.food[1]*self.unit_row
        pygame.draw.rect(self.surface, self.color["food"], (x,y, self.unit_column, self.unit_row))
    def move_snake(self):
        if (time.time()-self.last_updated_move)>self.min_time_gap:
            self.check_eat_food()
            new_head = self.snake[0][:]
            new_head[0] += self.direction[0]
            new_head[1] += self.direction[1]
            body = self.snake[:]
            self.snake = [new_head]+body[:-1]
            self.last_updated_move = time.time()
    def change_direction(self, direction):
        if (time.time()-self.last_updated_direction)>self.min_time_gap:
            if not self.are_same(self.opposite_direction(self.direction[:]), direction[:]):
                self.direction = direction[:]
            self.last_updated_direction = time.time()
    def check_eat_food(self):
        self.eaten_for_now = False
        if self.does_food_collides_with_snake(self.food):
            self.snake.append(self.snake[-1])
            self.eaten_for_now = True
            self.create_food()
    def collided(self):
        if self.does_snake_collides_with_itself() or self.does_snake_collides_with_walls():
            return True
        return False
    def exec(self):
        self.move_snake()
        return self.collided()
    def render(self):
        if not self.graphic_initialized:
            self.__init__for_render()
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
        #--------------------------------------------------------------
        self.draw_world()
        self.draw_snake()
        self.draw_food()
        # -------------------------------------------------------------
        pygame.display.update()
        self.ft.tick(self.fps)

