import turtle
import random
import time
import numpy as np


class DisplayGame:
    """Class for displaying the game when HEADLESS is set to False"""

    def __init__(self, XSIZE, YSIZE):
        """Initializes all aspects of the game including the board, snake and food pellets."""
        # SCREEN
        self.win = turtle.Screen()
        self.win.title("EVAC Snake game")
        self.win.bgcolor("grey")
        self.win.setup(width=(XSIZE*20)+40, height=(YSIZE*20)+40)
        self.win.tracer(0)

        # Snake Head
        self.head = turtle.Turtle()
        self.head.shape("square")
        self.head.color("black")

        # Snake food
        self.food = turtle.Turtle()
        self.food.shape("circle")
        self.food.color("red")
        self.food.penup()
        self.food.shapesize(0.55, 0.55)
        self.segments = []

    def reset(self, snake):
        """Resets the display when the game is first ran"""
        self.segments = []
        self.head.penup()
        self.food.goto(-500, -500)
        self.head.goto(-500, -500)
        for i in range(len(snake)-1):
            self.add_snake_segment()
        self.update_segment_positions(snake)

    def update_food(self, new_food):
        """Updates/draws food to the display"""
        self.food.goto(((new_food[1]-9)*20)+20, (((9-new_food[0])*20)-10)-20)

    def update_segment_positions(self, snake):
        """Updates/draws each segment of the snake to the display"""
        self.head.goto(((snake[0][1]-9)*20)+20, (((9-snake[0][0])*20)-10)-20)
        for i in range(len(self.segments)):
            self.segments[i].goto(((snake[i+1][1]-9)*20)+20,
                                  (((9-snake[i+1][0])*20)-10)-20)

    def add_snake_segment(self):
        """Draws and adds a new snake segment to the display"""
        self.new_segment = turtle.Turtle()
        self.new_segment.speed(0)
        self.new_segment.shape("square")
        # TODO: Change back to random colour generation before submission
        self.new_segment.color("green")
        self.new_segment.penup()
        self.segments.append(self.new_segment)


class Snake:
    """Class which contains the game logic for the game Snake"""

    def __init__(self, _XSIZE, _YSIZE):
        """Draws and adds a new snake segment to the display"""
        self.XSIZE = _XSIZE
        self.YSIZE = _YSIZE
        self.reset()

    def reset(self):
        """Resets the game after a run has finished"""
        self.snake = [[8, 10], [8, 9], [8, 8], [8, 7], [8, 6], [8, 5], [8, 4], [
            8, 3], [8, 2], [8, 1], [8, 0]]  # Initial snake co-ordinates [ypos,xpos]
        self.food = self.place_food()
        self.snake_direction = "right"
        # TODO: 1. Check if this modification is allowed
        self.time_until_starve = self.XSIZE * self.YSIZE * 1.5

    def place_food(self):
        """Randomly generates a location for the food, and regenerates it if spawned inside the snake"""
        self.food = [random.randint(1, (self.YSIZE-2)),
                     random.randint(1, (self.XSIZE-2))]
        while (self.food in self.snake):
            self.food = [random.randint(
                1, (self.YSIZE-2)), random.randint(1, (self.XSIZE-2))]
        return(self.food)

    def update_snake_position(self):
        """Adds the new coordinate of the snakes head to the front of the snake coordinate list."""
        self.snake.insert(0, [self.snake[0][0] + (self.snake_direction == "down" and 1) + (self.snake_direction == "up" and -1),
                          self.snake[0][1] + (self.snake_direction == "left" and -1) + (self.snake_direction == "right" and 1)])

    def food_eaten(self):
        """Returns True if snakes head coordinate is the same as the food location, otherwise removes the oldest coordinate 
            in the snake coordinate list (as a new one will be added for the movement of the head) and returns False."""
        if self.snake[0] == self.food:
            self.time_until_starve = self.XSIZE * self.YSIZE * 1.5
            return True
        else:
            self.time_until_starve -= 1
            self.snake.pop()  # snake moves forward and so last tail item is removed
            return False

    def snake_turns_into_self(self):
        """Returns True if new snakes head coordinate is already in the body, otherwise False"""
        if self.snake[0] in self.snake[1:]:
            return True
        else:
            return False

    def snake_hit_wall(self):
        """Returns True if new snakes head coordinate goes out of bounds, otherwise False"""
        if self.snake[0][0] == 0 or self.snake[0][0] == (self.YSIZE-1) or self.snake[0][1] == 0 or self.snake[0][1] == (self.XSIZE-1):
            return True
        else:
            return False

    # Sensor Functions
    def get_adj_coords(self):
        """Returns dictionary of adjacent coordinates to the snakes head"""
        adj_coords = {}
        dir_offsets = {"up": [-1, 0], ("down"): [+1, 0],
                       ("left"): [0, -1], ("right"): [0, +1]}
        for key, value in dir_offsets.items():
            adj_coords[key] = list(map(sum, zip(self.snake[0], value)))

        return adj_coords

    def sense_wall(self, coord):
        """Returns True if provided coordinate out of bounds, otherwise False"""
        return(coord[0] == 0 or coord[0] == (self.YSIZE-1) or coord[1] == 0 or coord[1] == (self.XSIZE-1))

    def sense_food(self, coord):
        """True if food is at provided coordinate, otherwise False"""
        return self.food == coord

    def sense_tail(self, coord):
        """Returns True if coordinate is a part of the snake, otherwise False"""
        return coord in self.snake

    def obstacle_check(self, coord):
        """Returns 0 if a tail or wall is found in a given direction, otherwise 1"""
        if self.sense_wall(coord):
            return 0
        elif self.sense_tail(coord):
            return 0
        else:
            return 1

    def food_direction(self, direction):
        """Returns 1 if food coordinate greater than snake, 0 if equal, -1 if less"""
        snake_head = self.snake[0]
        index = 1 if direction == "x" else 0

        if(self.food[index] < snake_head[index]):
            return -1
        elif(self.food[index] == snake_head[index]):
            return 0
        elif(self.food[index] > snake_head[index]):
            return 1
        return 0

    def distance_to_obstacle(self, direction):
        dir_offsets = {"up": [-1, 0], ("down"): [+1, 0],
                       ("left"): [0, -1], ("right"): [0, +1]}

        checked_coord = self.snake[0]
        distance, obstacle_found = 0, False
        while not obstacle_found:
            checked_coord = [checked_coord[0]+dir_offsets[direction]
                             [0], checked_coord[1]+dir_offsets[direction][1]]
            distance += 1
            if self.sense_tail(checked_coord):
                return distance
            elif self.sense_wall(checked_coord):
                return distance

    def distance_to_food(self, direction):
        dir_offsets = {"up": [-1, 0], ("down"): [+1, 0],
                       ("left"): [0, -1], ("right"): [0, +1]}

        checked_coord = self.snake[0]
        distance, food_found = 0, False
        while not food_found:
            checked_coord = [checked_coord[0]+dir_offsets[direction]
                             [0], checked_coord[1]+dir_offsets[direction][1]]
            distance += 1
            if self.sense_food(checked_coord):
                return distance
            elif self.sense_wall(checked_coord):
                return -1


def run_game(display, snake_game, headless, network, algorithm):
    '''Runs through a game simulation, using the neural network to make decisions on the snakes movement. 
        Returns the final score the snake achieved before a loss condition was met.'''

    # Resets the score, game & display
    score = 0
    steps = 0
    snake_game.reset()
    if not headless:
        display.reset(snake_game.snake)
        display.win.update()
    snake_game.place_food()
    game_over = False

    while not game_over:
        steps += 1
        adj_coords = snake_game.get_adj_coords()

        local_sensing = [snake_game.obstacle_check(adj_coords["up"]),
                         snake_game.obstacle_check(adj_coords["down"]),
                         snake_game.obstacle_check(adj_coords["left"]),
                         snake_game.obstacle_check(adj_coords["right"]),
                         snake_game.sense_food(adj_coords["up"]),
                         snake_game.sense_food(adj_coords["down"]),
                         snake_game.sense_food(adj_coords["left"]),
                         snake_game.sense_food(adj_coords["right"])]

        global_sensing = [snake_game.distance_to_obstacle("up"),
                          snake_game.distance_to_obstacle("down"),
                          snake_game.distance_to_obstacle("left"),
                          snake_game.distance_to_obstacle("right"),
                          snake_game.distance_to_food("up"),
                          snake_game.distance_to_food("down"),
                          snake_game.distance_to_food("left"),
                          snake_game.distance_to_food("right")]

        food_direction = [snake_game.food_direction(
            "x"), snake_game.food_direction("y")]

        food_coordinate = [snake_game.food[0], snake_game.food[1]]

        # Gets softmax output of the neural network decision
        if algorithm == "a":
            decision = network.feedForward(local_sensing)
        elif algorithm == "b":
            decision = network.feedForward(local_sensing + food_direction)
        elif algorithm == "c":
            decision = network.feedForward(local_sensing + food_coordinate)
        elif algorithm == "d":
            decision = network.feedForward(global_sensing + food_coordinate)
        elif algorithm == "e":
            decision = network.feedForward(global_sensing + food_direction)

        # Converts softmax output to output direction and sets it
        directions = ["up", "down", "left", "right"]
        direction = np.argmax(decision)
        snake_game.snake_direction = directions[direction]

        snake_game.update_snake_position()

        # Checks if food is eaten and replaces food + increments score
        if snake_game.food_eaten():
            snake_game.place_food()
            score += 1
            if not headless:
                display.add_snake_segment()

        # Ends game if the snake runs into itself
        if snake_game.snake_turns_into_self():
            game_over = True

        # Ends game if the snake hits a wall
        if snake_game.snake_hit_wall():
            game_over = True

        # Ends game if snake starves
        if snake_game.time_until_starve == 0:
            game_over = True

        # Updates display when not running in headless mode
        if not headless:
            display.update_food(snake_game.food)
            display.update_segment_positions(snake_game.snake)
            display.win.update()

            time.sleep(10)     # Change to change update rate of the game

    if not headless:
        turtle.done()
        turtle.bye()

    return score
