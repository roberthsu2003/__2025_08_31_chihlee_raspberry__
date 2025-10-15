from dataclasses import dataclass
from src.snake import Snake
from src.food import Food

@dataclass
class GameState:
    score: int
    level: int
    snake: Snake
    food: Food
    game_over: bool
    current_player_name: str = ""
    current_player_high_score: int = 0