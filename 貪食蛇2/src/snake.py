import pygame
from src.config import SNAKE_SIZE, SCREEN_WIDTH, SCREEN_HEIGHT, GREEN

class Snake:
    def __init__(self):
        self.body = [(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)]
        self.direction = pygame.K_RIGHT
        self.grow_pending = False

    def move(self):
        head_x, head_y = self.body[0]
        if self.direction == pygame.K_UP:
            new_head = (head_x, head_y - SNAKE_SIZE)
        elif self.direction == pygame.K_DOWN:
            new_head = (head_x, head_y + SNAKE_SIZE)
        elif self.direction == pygame.K_LEFT:
            new_head = (head_x - SNAKE_SIZE, head_y)
        elif self.direction == pygame.K_RIGHT:
            new_head = (head_x + SNAKE_SIZE, head_y)

        self.body.insert(0, new_head)
        if not self.grow_pending:
            self.body.pop()
        else:
            self.grow_pending = False

    def grow(self):
        self.grow_pending = True

    def get_head_position(self):
        return self.body[0]

    def get_body_positions(self):
        return self.body

    def change_direction(self, new_direction):
        # Prevent reversing direction
        if (new_direction == pygame.K_LEFT and self.direction != pygame.K_RIGHT) or \
           (new_direction == pygame.K_RIGHT and self.direction != pygame.K_LEFT) or \
           (new_direction == pygame.K_UP and self.direction != pygame.K_DOWN) or \
           (new_direction == pygame.K_DOWN and self.direction != pygame.K_UP):
            self.direction = new_direction

    def check_collision(self):
        head = self.get_head_position()
        # Wall collision
        if head[0] < 0 or head[0] >= SCREEN_WIDTH or head[1] < 0 or head[1] >= SCREEN_HEIGHT:
            return True
        # Self-collision
        for segment in self.body[1:]:
            if head == segment:
                return True
        return False

    def draw(self, screen):
        for segment in self.body:
            pygame.draw.rect(screen, GREEN, (segment[0], segment[1], SNAKE_SIZE, SNAKE_SIZE))
