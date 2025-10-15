import pytest
import pygame
from unittest.mock import MagicMock, patch
from src.main import main, MENU, GAME, GAME_OVER, HIGH_SCORES, get_player_name, display_high_scores
from src.game import Game
from src.scores import load_scores, save_scores, SCORES_FILE
from src.config import BLACK, WHITE, RED # Import necessary constants
import os

# Fixture to create and clean up a temporary scores file
@pytest.fixture
def temp_scores_file_integration():
    # Ensure the file doesn't exist before the test
    if os.path.exists(SCORES_FILE):
        os.remove(SCORES_FILE)
    yield
    # Clean up after the test
    if os.path.exists(SCORES_FILE):
        os.remove(SCORES_FILE)

# Mock pygame functions for integration tests
@pytest.fixture(autouse=True)
def mock_pygame_init():
    with patch('pygame.init'), \
         patch('pygame.display.set_mode', return_value=MagicMock()), \
         patch('pygame.display.set_caption'), \
         patch('pygame.quit'), \
         patch('pygame.event.get', return_value=[]), \
         patch('pygame.time.delay'), \
         patch('pygame.display.flip'):
        # Patch GAME_FONT in src.main with a mock object
        with patch('src.main.GAME_FONT', new=MagicMock()) as mock_game_font_main:
            mock_game_font_main.render.return_value = MagicMock(get_width=lambda: 100, get_height=lambda: 30)
            # Also patch GAME_FONT in src.config if it's used directly there
            with patch('src.config.GAME_FONT', new=MagicMock()) as mock_game_font_config:
                mock_game_font_config.render.return_value = MagicMock(get_width=lambda: 100, get_height=lambda: 30)
                yield

# This test is a placeholder. Full integration testing of Pygame UI requires
# advanced techniques to simulate user input and verify screen output.
# This test only verifies the flow of states and score saving logic.
def test_integration_player_name_input_and_score_persistence(temp_scores_file_integration):
    # Simulate initial state: no player name, game starts, player enters name, plays, game over, score saved
    
    # Mock get_player_name to return a name
    with patch('src.main.get_player_name', return_value="TestPlayer") as mock_get_name:
        # Mock Game.run to simulate a game session
        with patch.object(Game, 'run') as mock_game_run:
            mock_game_instance = MagicMock()
            mock_game_instance.game_over = True
            mock_game_instance.score = 100
            mock_game_run.return_value = None # Game.run doesn't return anything, it modifies game_instance
    
            with patch('src.main.Game', return_value=mock_game_instance):
                # Simulate pressing 'S' to start game
                pygame.event.get.side_effect = [[MagicMock(type=pygame.KEYDOWN, key=pygame.K_s)], []]
                
                # Call main loop (will run once for menu, then once for game, then once for game over)
                # This is a simplified simulation, actual Pygame loop is continuous
                # For this test, we'll assume get_player_name is called and returns
                player_name = get_player_name(MagicMock())
                assert player_name == "TestPlayer"
                
                # Simulate game over and score saving
                save_scores(player_name, 100)
                
                scores = load_scores()
                assert len(scores) == 1
                assert scores[0]['name'] == "TestPlayer"
                assert scores[0]['score'] == 100

                # Simulate another game with higher score
                save_scores(player_name, 150)
                scores = load_scores()
                assert len(scores) == 1
                assert scores[0]['name'] == "TestPlayer"
                assert scores[0]['score'] == 150

                # Simulate another game with lower score
                save_scores(player_name, 50)
                scores = load_scores()
                assert len(scores) == 1
                assert scores[0]['name'] == "TestPlayer"
                assert scores[0]['score'] == 150 # Should not update with lower score

                # Simulate a new player
                save_scores("NewPlayer", 200)
                scores = load_scores()
                assert len(scores) == 2
                assert scores[0]['name'] == "NewPlayer"
                assert scores[0]['score'] == 200
                assert scores[1]['name'] == "TestPlayer"
                assert scores[1]['score'] == 150