import sys
import collections
import os
from enum import Enum, auto

import pygame
from pygame.locals import *

pygame.init()


def load_snake_tiles():

	# Snake Tile Set
	snake_tile_set = pygame.image.load(os.path.join('image','Snake.png'))
	snake_tile_set_size = snake_tile_set.get_size()
	snake_tile_set_size_x, snake_tile_set_size_y = tuple(map(lambda x: x // 4, snake_tile_set_size))


	tiles = [
		["head_up", "head_right", "head_down", "head_left"],
		["tail_up", "tail_right", "tail_down", "tail_left"],
		["turn_1", "turn_2", "turn_3", "turn_4"],
		["body_vertical", "body_horizontal", "rabbit", "grass"]
	]
	images = {}
	for i in range(4):
		for j in range(4):
			surface = pygame.Surface((snake_tile_set_size_x, snake_tile_set_size_y), SRCALPHA, 32)
			surface = surface.convert_alpha()
			surface.blit(snake_tile_set, (0, 0), (
				snake_tile_set_size_x * j,
				snake_tile_set_size_y * i,
				snake_tile_set_size_x * (j + 1),
				snake_tile_set_size_y * (i + 1))
			)
			surface = pygame.transform.scale(surface, (cell, cell))
			images[tiles[i][j]] = surface
	return images

# Constants
size = width, height = 600, 600
cell = 25

white = 255, 255, 255
black = 0, 0, 0

xn = width // cell
yn = height // cell

# Screen
screen = pygame.display.set_mode(size)

# Background
images = load_snake_tiles()
background = [[images["grass"]] * yn] * xn

SnakePart = collections.namedtuple("SnakePart", ["name", "x", "y", "direction"])


class Direction(Enum):
    UP = auto()
    RIGHT = auto()
    DOWN = auto()
    LEFT = auto()


class State(Enum):
	READY = auto()
	PLAYING = auto()
	PAUSED = auto()


# Snake Class
class Snake:
	def __init__(self):
		self.parts = [
			SnakePart("head_down", 5, 13, Direction.DOWN),
			SnakePart("body_vertical", 5, 12, Direction.DOWN),
			SnakePart("body_vertical", 5, 11, Direction.DOWN),
			SnakePart("tail_down", 5, 10, Direction.DOWN)
		]
		self.previous_direction = Direction.DOWN
		self.direction = Direction.DOWN
		self.state = State.READY
		self._grow = False

	def draw(self, screen):
		for part in self.parts:
			screen.blit(images[part.name], (part.x * cell, part.y * cell))

	def move(self):
		if self.state == State.PLAYING:
			head = self.parts[0]
			tail = self.parts[-1]
			previous_last_but_one = self.parts[-2]

			if self.direction == Direction.DOWN:
				new_head = SnakePart("head_down", head.x, head.y + 1, Direction.DOWN)

				if self.previous_direction == Direction.DOWN:
					new_part = "body_vertical"

				elif self.previous_direction == Direction.RIGHT:
					new_part = "turn_3"

				elif self.previous_direction == Direction.LEFT:
					new_part = "turn_2"

			elif self.direction == Direction.RIGHT:
				new_head = SnakePart("head_right", head.x + 1, head.y, Direction.RIGHT)

				if self.previous_direction == Direction.DOWN:
					new_part = "turn_1"

				elif self.previous_direction == Direction.RIGHT:
					new_part = "body_horizontal"

				elif self.previous_direction == Direction.UP:
					new_part = "turn_2"

			elif self.direction == Direction.LEFT:
				new_head = SnakePart("head_left", head.x - 1, head.y, Direction.LEFT)

				if self.previous_direction == Direction.DOWN:
					new_part = "turn_4"

				elif self.previous_direction == Direction.UP:
					new_part = "turn_3"

				elif self.previous_direction == Direction.LEFT:
					new_part = "body_horizontal"


			elif self.direction == Direction.UP:
				new_head = SnakePart("head_up", head.x, head.y - 1, Direction.UP)

				if self.previous_direction == Direction.RIGHT:
					new_part = "turn_4"

				elif self.previous_direction == Direction.UP:
					new_part = "body_vertical"

				elif self.previous_direction == Direction.LEFT:
					new_part = "turn_1"

			self.parts[0] = new_head

			# Insert New Part Behind Head
			self.parts.insert(1, SnakePart(new_part, head.x, head.y, self.previous_direction))
			self.previous_direction = self.direction

			if self._grow:
				self._grow = False
				return

			# Remove Part From Back
			self.parts.pop(-2)

			# Tail Calculation
			last_but_one = self.parts[-2]

			if last_but_one.direction == Direction.DOWN:
				tail_name = "tail_down"
			elif last_but_one.direction == Direction.UP:
				tail_name = "tail_up"
			elif last_but_one.direction == Direction.RIGHT:
				tail_name = "tail_right"
			elif last_but_one.direction == Direction.LEFT:
				tail_name = "tail_left"

			self.parts[-1] = SnakePart(tail_name, previous_last_but_one.x, previous_last_but_one.y, last_but_one.direction)

	def start(self):
		if self.state == State.READY or self.state == State.PAUSED:
			self.state = State.PLAYING
		elif self.state == State.PLAYING:
			self.state = State.PAUSED

	def turn(self, direction):
		if direction == Direction.DOWN and self.previous_direction == Direction.UP:
			pass
		elif direction == Direction.RIGHT and self.previous_direction == Direction.LEFT:
			pass
		elif direction == Direction.UP and self.previous_direction == Direction.DOWN:
			pass
		elif direction == Direction.LEFT and self.previous_direction == Direction.RIGHT:
			pass
		else:
			self.direction = direction

	def grow(self):
		self._grow = True

s = Snake()
clock = pygame.time.Clock()

while True:

	# Events
	# pygame.event.pump()
 #    keys = pygame.key.get_pressed()
    for event in pygame.event.get():
        if event.type == QUIT:
            sys.exit()
        elif event.type == KEYDOWN:
        	if event.key == K_SPACE:
        		s.start()
        	elif event.key == K_RIGHT:
        		s.turn(Direction.RIGHT)
        	elif event.key == K_DOWN:
        		s.turn(Direction.DOWN)
        	elif event.key == K_UP:
        		s.turn(Direction.UP)
        	elif event.key == K_LEFT:
        		s.turn(Direction.LEFT)
        	elif event.key == K_RETURN:
        		s.grow()

    # Calculations
    s.move()

    # Drawing
    screen.fill(white)
    for i in range(xn):
    	for j in range(yn):
    		screen.blit(background[i][j], (i * cell, j * cell))
    s.draw(screen)

    # pygame.display.flip()
    pygame.display.update()
    # pygame.time.delay(200)
    clock.tick(2)