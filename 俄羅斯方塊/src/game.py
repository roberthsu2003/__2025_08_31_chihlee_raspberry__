
import pygame
import random
from settings import *
from block import Block

class Game:
    def __init__(self):
        self.grid = [[0 for _ in range(SCREEN_WIDTH // GRID_SIZE)] for _ in range(SCREEN_HEIGHT // GRID_SIZE)]
        self.current_block = self.new_block()
        self.next_block = self.new_block()
        self.score = 0
        self.game_over = False
        self.block_x = (SCREEN_WIDTH // GRID_SIZE) // 2 - 1
        self.block_y = 0
        self.fall_time = 0
        self.fall_speed = 0.5

    def new_block(self):
        shape = random.choice(list(TETROMINOES.keys()))
        return Block(TETROMINOES[shape], TETROMINO_COLORS[shape])

    def draw_grid(self, screen):
        for x in range(0, SCREEN_WIDTH, GRID_SIZE):
            pygame.draw.line(screen, GRAY, (x, 0), (x, SCREEN_HEIGHT))
        for y in range(0, SCREEN_HEIGHT, GRID_SIZE):
            pygame.draw.line(screen, GRAY, (0, y), (SCREEN_WIDTH, y))

    def check_collision(self, shape, x, y):
        for row_index, row in enumerate(shape):
            for col_index, cell in enumerate(row):
                if cell:
                    grid_x = x + col_index
                    grid_y = y + row_index
                    if not (0 <= grid_x < (SCREEN_WIDTH // GRID_SIZE) and 0 <= grid_y < (SCREEN_HEIGHT // GRID_SIZE) and self.grid[grid_y][grid_x] == 0):
                        return True
        return False

    def run(self, clock):
        self.fall_time += clock.get_rawtime()
        if self.fall_time / 1000 > self.fall_speed:
            self.fall_time = 0
            self.block_y += 1
            if self.check_collision(self.current_block.shape, self.block_x, self.block_y):
                self.block_y -= 1
                self.lock_block()

    def lock_block(self):
        for row_index, row in enumerate(self.current_block.shape):
            for col_index, cell in enumerate(row):
                if cell:
                    self.grid[self.block_y + row_index][self.block_x + col_index] = self.current_block.color
        self.clear_lines()
        self.current_block = self.next_block
        self.next_block = self.new_block()
        self.block_x = (SCREEN_WIDTH // GRID_SIZE) // 2 - 1
        self.block_y = 0
        if self.check_collision(self.current_block.shape, self.block_x, self.block_y):
            self.game_over = True

    def clear_lines(self):
        lines_cleared = 0
        for i in range(len(self.grid) - 1, -1, -1):
            if 0 not in self.grid[i]:
                lines_cleared += 1
                del self.grid[i]
                self.grid.insert(0, [0 for _ in range(SCREEN_WIDTH // GRID_SIZE)])
        self.score += lines_cleared * 10

    def draw(self, screen):
        self.current_block.draw(screen, self.block_x, self.block_y)
        for y, row in enumerate(self.grid):
            for x, color in enumerate(row):
                if color != 0:
                    pygame.draw.rect(screen, color, (x * GRID_SIZE, y * GRID_SIZE, GRID_SIZE, GRID_SIZE), 0)
                    pygame.draw.rect(screen, WHITE, (x * GRID_SIZE, y * GRID_SIZE, GRID_SIZE, GRID_SIZE), 1)

    def draw_next_block(self, screen):
        next_block_text = pygame.font.Font("assets/wqy-zenhei.ttc", 24).render("下一個", True, WHITE)
        screen.blit(next_block_text, (420, 150))
        shape = self.next_block.shape
        for y, row in enumerate(shape):
            for x, cell in enumerate(row):
                if cell:
                    pygame.draw.rect(screen, self.next_block.color, (420 + x * GRID_SIZE, 200 + y * GRID_SIZE, GRID_SIZE, GRID_SIZE), 0)
                    pygame.draw.rect(screen, WHITE, (420 + x * GRID_SIZE, 200 + y * GRID_SIZE, GRID_SIZE, GRID_SIZE), 1)
