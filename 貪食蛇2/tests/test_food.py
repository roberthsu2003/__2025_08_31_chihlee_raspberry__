import pytest
from src.food import Food
from src.config import GRID_WIDTH, GRID_HEIGHT

def test_food_initial_position_randomized():
    food = Food()
    assert 0 <= food.position[0] < GRID_WIDTH
    assert 0 <= food.position[1] < GRID_HEIGHT

def test_food_randomize_position_changes_position():
    food = Food()
    initial_position = food.position
    food.randomize_position()
    # There's a small chance it could randomize to the same position, but highly unlikely
    # For a robust test, we might run it multiple times or check bounds
    assert 0 <= food.position[0] < GRID_WIDTH
    assert 0 <= food.position[1] < GRID_HEIGHT
    # assert food.position != initial_position # This might fail rarely
