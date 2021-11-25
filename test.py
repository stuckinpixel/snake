
from Game import *
snake = Snake(width=600, height=400, rows=16, columns=30, min_time_gap=0.1)


while True:
    snake.render()
    state = snake.exec()
    action = snake.sample_action()
    snake.change_direction(action)
    if state==True:
        break
