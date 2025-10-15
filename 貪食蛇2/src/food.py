import pygame
import random
from src.config import SCREEN_WIDTH, SCREEN_HEIGHT, FOOD_SIZE, RED

class Food:
    def __init__(self):
        self.position = (0, 0)
        self.spawn_food()

    def spawn_food(self):
        x = random.randrange(0, SCREEN_WIDTH - FOOD_SIZE, FOOD_SIZE)
        y = random.randrange(0, SCREEN_HEIGHT - FOOD_SIZE, FOOD_SIZE)
        self.position = (x, y)

    def get_position(self):
        return self.position

    def draw(self, screen):
        pygame.draw.rect(screen, RED, (self.position[0], self.position[1], FOOD_SIZE, FOOD_SIZE))