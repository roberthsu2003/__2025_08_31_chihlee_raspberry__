import pytest
from src.snake import Snake

def test_snake_initial_position_and_direction():
    snake = Snake()
    assert snake.body == [(10, 10), (9, 10), (8, 10)]
    assert snake.direction == (1, 0)

def test_snake_move_without_growing():
    snake = Snake()
    initial_body = list(snake.body)
    snake.move()
    assert len(snake.body) == len(initial_body)
    assert snake.body[0] == (11, 10) # Moved right
    assert snake.body[-1] == initial_body[1] # Tail moved to previous second segment

def test_snake_grow():
    snake = Snake()
    initial_length = len(snake.body)
    snake.grow_snake()
    snake.move()
    assert len(snake.body) == initial_length + 1
    assert snake.body[0] == (11, 10)

def test_snake_change_direction():
    snake = Snake()
    snake.change_direction((0, 1)) # Down
    assert snake.direction == (0, 1)
    snake.change_direction((-1, 0)) # Left
    assert snake.direction == (-1, 0)

def test_snake_prevent_reverse_direction():
    snake = Snake()
    snake.change_direction((-1, 0)) # Try to move left (opposite of initial right)
    assert snake.direction == (1, 0) # Should remain right
    snake.change_direction((0, 1)) # Change to down
    snake.change_direction((0, -1)) # Try to move up (opposite of down)
    assert snake.direction == (0, 1) # Should remain down
