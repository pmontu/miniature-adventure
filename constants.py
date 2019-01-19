import pygame
import os

size = width, height = 600, 600
cell = 25

white = 255, 255, 255
black = 0, 0, 0

xn = width // cell
yn = height // cell

# Terrain Tile Set
terrain_all = pygame.image.load(os.path.join('image','terrain_atlas.png'))

# Terrain1
terrain1 = pygame.Surface((25, 25))
terrain1.blit(terrain_all, (0, 0), (125, 750, 25, 25))