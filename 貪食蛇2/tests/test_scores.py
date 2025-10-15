import pytest
import json
import os
from src.scores import load_scores, save_scores, SCORES_FILE

# Fixture to create and clean up a temporary scores file
@pytest.fixture
def temp_scores_file():
    # Ensure the file doesn't exist before the test
    if os.path.exists(SCORES_FILE):
        os.remove(SCORES_FILE)
    yield
    # Clean up after the test
    if os.path.exists(SCORES_FILE):
        os.remove(SCORES_FILE)

def test_load_scores_empty_file(temp_scores_file):
    # Create an empty scores file
    with open(SCORES_FILE, "w") as f:
        f.write("")
    scores = load_scores()
    assert scores == []

def test_load_scores_non_existent_file(temp_scores_file):
    scores = load_scores()
    assert scores == []

def test_load_scores_valid_data(temp_scores_file):
    test_data = [
        {"name": "Player1", "score": 100},
        {"name": "Player2", "score": 150}
    ]
    with open(SCORES_FILE, "w", encoding="utf-8") as f:
        json.dump(test_data, f)
    scores = load_scores()
    assert scores == [
        {"name": "Player2", "score": 150},
        {"name": "Player1", "score": 100}
    ] # Should be sorted by score

def test_save_scores_new_player(temp_scores_file):
    save_scores("NewPlayer", 200)
    scores = load_scores()
    assert scores == [
        {"name": "NewPlayer", "score": 200}
    ]

def test_save_scores_update_existing_player_higher_score(temp_scores_file):
    save_scores("ExistingPlayer", 100)
    save_scores("ExistingPlayer", 150)
    scores = load_scores()
    assert scores == [
        {"name": "ExistingPlayer", "score": 150}
    ]

def test_save_scores_update_existing_player_lower_score(temp_scores_file):
    save_scores("ExistingPlayer", 100)
    save_scores("ExistingPlayer", 50)
    scores = load_scores()
    assert scores == [
        {"name": "ExistingPlayer", "score": 100}
    ]

def test_save_scores_multiple_players(temp_scores_file):
    save_scores("PlayerA", 50)
    save_scores("PlayerB", 150)
    save_scores("PlayerA", 100)
    scores = load_scores()
    assert scores == [
        {"name": "PlayerB", "score": 150},
        {"name": "PlayerA", "score": 100}
    ]
