import pytest
import pygame
from unittest.mock import MagicMock
from src.game import Game
from src.snake import Snake
from src.food import Food
from src.config import GRID_WIDTH, GRID_HEIGHT, INITIAL_GAME_SPEED

# Mock pygame screen for testing drawing methods
@pytest.fixture
def mock_screen():
    return MagicMock()

@pytest.fixture
def game_instance(mock_screen):
    game = Game(mock_screen)
    game.snake = Snake()
    game.food = Food()
    game.food.position = (5, 5) # Set a predictable food position
    game.snake.body = [(10, 10), (9, 10), (8, 10)] # Set a predictable snake position
    game.snake.direction = (1, 0) # Moving right
    return game

def test_game_initialization(game_instance):
    assert game_instance.running is True
    assert game_instance.game_over is False
    assert game_instance.score == 0
    assert game_instance.level == 1

def test_game_snake_eats_food(game_instance):
    # Set snake head to be one step left of food, moving right
    game_instance.snake.body = [(4, 5), (3, 5)]
    game_instance.snake.direction = (1, 0) # Moving right
    game_instance.food.position = (5, 5) # Food at (5,5)
    game_instance.update() # Snake moves to (5,5) and eats food
    assert game_instance.score == 1
    assert len(game_instance.snake.body) == 3 # Snake should grow
    assert game_instance.food.position != (5, 5) # Food should have moved

def test_game_snake_collides_with_wall(game_instance):
    game_instance.snake.body = [(GRID_WIDTH - 1, 10), (GRID_WIDTH - 2, 10)] # Snake near right wall
    game_instance.snake.direction = (1, 0) # Move right
    game_instance.update()
    assert game_instance.game_over is True

    game_instance.game_over = False # Reset for next test
    game_instance.snake.body = [(0, 10), (1, 10)] # Snake near left wall
    game_instance.snake.direction = (-1, 0) # Move left
    game_instance.update()
    assert game_instance.game_over is True

    game_instance.game_over = False # Reset for next test
    game_instance.snake.body = [(10, GRID_HEIGHT - 1), (10, GRID_HEIGHT - 2)] # Snake near bottom wall
    game_instance.snake.direction = (0, 1) # Move down
    game_instance.update()
    assert game_instance.game_over is True

    game_instance.game_over = False # Reset for next test
    game_instance.snake.body = [(10, 0), (10, 1)] # Snake near top wall
    game_instance.snake.direction = (0, -1) # Move up
    game_instance.update()
    assert game_instance.game_over is True

def test_game_snake_collides_with_self(game_instance):
    # Snake body: head at (10,10), next segment at (10,11)
    game_instance.snake.body = [(10, 10), (10, 11), (10, 12)]
    game_instance.snake.direction = (0, 1) # Try to move down, new head will be (10,11)
    game_instance.update()
    assert game_instance.game_over is True

def test_game_level_and_speed_progression(game_instance):
    initial_speed = game_instance.game_speed
    # Simulate eating 10 food items to level up
    for _ in range(10):
        # Set snake head to be one step left of food, moving right
        game_instance.snake.body = [(4, 5), (3, 5)]
        game_instance.snake.direction = (1, 0)
        game_instance.food.position = (5, 5) # Food at (5,5)
        game_instance.update() # Snake moves to (5,5) and eats food
        # After eating, randomize food position for next iteration
        game_instance.food.randomize_position() # Ensure food is not at (5,5) for next iteration
    assert game_instance.score == 10
    assert game_instance.level == 2
    assert game_instance.game_speed < initial_speed # Speed should have increased (delay decreased)

    # Simulate eating another 10 food items
    for _ in range(10):
        game_instance.snake.body = [(4, 5), (3, 5)]
        game_instance.snake.direction = (1, 0)
        game_instance.food.position = (5, 5)
        game_instance.update()
        game_instance.food.randomize_position()
    assert game_instance.score == 20
    assert game_instance.level == 3
    assert game_instance.game_speed < initial_speed # Speed should have increased further
