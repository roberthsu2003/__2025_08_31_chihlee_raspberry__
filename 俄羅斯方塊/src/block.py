
import pygame
import random
from settings import *

class Block(pygame.sprite.Sprite):
    def __init__(self, shape, color):
        super().__init__()
        self.shape = shape
        self.color = color

    def rotate(self):
        self.shape = [list(row) for row in zip(*self.shape[::-1])]

    def un_rotate(self):
        self.shape = [list(row) for row in zip(*self.shape)][::-1]

    def draw(self, screen, grid_x, grid_y):
        for y, row in enumerate(self.shape):
            for x, cell in enumerate(row):
                if cell:
                    pygame.draw.rect(screen, self.color, (grid_x * GRID_SIZE + x * GRID_SIZE, grid_y * GRID_SIZE + y * GRID_SIZE, GRID_SIZE, GRID_SIZE), 0)
                    pygame.draw.rect(screen, WHITE, (grid_x * GRID_SIZE + x * GRID_SIZE, grid_y * GRID_SIZE + y * GRID_SIZE, GRID_SIZE, GRID_SIZE), 1)
