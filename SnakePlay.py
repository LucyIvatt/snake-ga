#!/usr/bin/env python
# coding: utf-8

# This version of the snake game allows you to play the same yourself using the arrow keys.

# In[ ]:


import random
import time
import turtle


# In[ ]:


class DisplayGame:
    def __init__(self, XSIZE, YSIZE):
        # SCREEN
        self.win = turtle.Screen()
        self.win.title("EVCO Snake game")
        self.win.bgcolor("grey")
        self.win.setup(width=(XSIZE*20)+18,height=(YSIZE*20)+18)
        self.win.screensize((XSIZE*20),(YSIZE*20))
        self.win.tracer(0)

        #Snake Head
        self.head = turtle.Turtle()
        self.head.shape("square")
        self.head.color("black")

        # Snake food
        self.food = turtle.Turtle()
        self.food.shape("circle")
        self.food.color("yellow")
        self.food.penup()
        self.food.shapesize(0.55, 0.55)
        
        self.segments = []
        self.reset()

    def reset(self):
        self.head.penup()
        self.food.goto(-500, -500)
        self.head.goto(-500, -500)
        self.segments = []
        
    def update_food(self,new_food):
        self.food.goto(((new_food[1]-9)*20), ((9-new_food[0])*20)-10)
        
    def update_segment_positions(self, snake):
        self.head.goto(((snake[0][1]-9)*20), ((9-snake[0][0])*20)-10)
        for i in range(len(self.segments)):
            self.segments[i].goto(((snake[i+1][1]-9)*20), ((9-snake[i+1][0])*20)-10)

    def add_snake_segment(self):
        self.new_segment = turtle.Turtle()
        self.new_segment.speed(0)
        self.new_segment.shape("square")
        self.new_segment.color("green")
        self.new_segment.penup()
        self.segments.append(self.new_segment)


# In[ ]:


XSIZE = YSIZE = 18 # Grids in each direction

display = DisplayGame(XSIZE,YSIZE)
display.win.update()
    
def go_up():
    display.head.direction = "up"
 
def go_down():
    display.head.direction = "down"
 
def go_right():
    display.head.direction = "right"
 
def go_left():
    display.head.direction = "left"


# In[ ]:


def placeFood(snake):
    food = [random.randint(1, (YSIZE-2)), random.randint(1, (XSIZE-2))]
    while (food in snake):
        food = [random.randint(1, (YSIZE-2)), random.randint(1, (XSIZE-2))]
    return( food )


# In[ ]:


display.win.listen()
display.win.onkey(go_up, "w")
display.win.onkey(go_down, "s")
display.win.onkey(go_right, "d")
display.win.onkey(go_left, "a")

score = 0
snake = [[8,10], [8,9], [8,8], [8,7], [8,6], [8,5], [8,4], [8,3], [8,2], [8,1],[8,0] ]# Initial snake co-ordinates [ypos,xpos]

for i in range(len(snake)-1): display.add_snake_segment()  
display.update_segment_positions(snake)


# In[ ]:


food = placeFood(snake)
display.update_food(food)
snake_direction = random.choice(["right","up","down"]) # random start direction (cannot be left)

display.head.direction = snake_direction
display.win.update()


# In[ ]:


game_over = False
while not game_over:
    
    #*Add your evolved controller here to decide on the direction the snake should take*
    #snake_direction = "down" / snake_direction = "up" / snake_direction = "left" / snake_direction = "right"
    
    snake_direction = display.head.direction
    
    snake.insert(0, [snake[0][0] + (snake_direction == "down" and 1) + (snake_direction == "up" and -1), snake[0][1] + (snake_direction == "left" and -1) + (snake_direction == "right" and 1)])

    if snake[0] == food:                                            # When snake eats the food
        score += 1
        print("Score:" + str(score))
        food = placeFood(snake)
        display.update_food(food)
    else:    
        last = snake.pop()  # [1] If it does not eat the food, it moves forward and so last tail item is removed

    display.update_segment_positions(snake)

    # Game over if the snake runs over itself
    if snake[0] in snake[1:]:
        game_over = True
        print("Snake turned into itself!")

    # Game over if the snake goes through a wall
    if snake[0][0] == 0 or snake[0][0] == (YSIZE-1) or snake[0][1] == 0 or snake[0][1] == (XSIZE-1):
        game_over = True
        print("Snake hit a wall!")

    display.win.update()
    time.sleep(0.5)
   
print("\nFINAL score - " + str(score))
print()
turtle.bye()

