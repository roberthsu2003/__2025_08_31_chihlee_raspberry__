import json
import os

SCORES_FILE = "scores.json"

def _get_scores_file_path():
    # Assuming scores.json is in the root directory of the project
    # Adjust this path if scores.json is located elsewhere
    current_dir = os.path.dirname(__file__)
    project_root = os.path.abspath(os.path.join(current_dir, os.pardir, os.pardir))
    return os.path.join(project_root, SCORES_FILE)

def load_scores():
    scores_path = _get_scores_file_path()
    if not os.path.exists(scores_path):
        return {}
    with open(scores_path, 'r', encoding='utf-8') as f:
        return json.load(f)

def save_scores(player_name, score):
    scores = load_scores()
    if player_name in scores:
        if score > scores[player_name]:
            scores[player_name] = score
    else:
        scores[player_name] = score

    scores_path = _get_scores_file_path()
    with open(scores_path, 'w', encoding='utf-8') as f:
        json.dump(scores, f, ensure_ascii=False, indent=4)

def get_player_high_score(player_name):
    scores = load_scores()
    return scores.get(player_name, 0)

def get_all_high_scores():
    scores = load_scores()
    # Sort scores by value in descending order
    sorted_scores = sorted(scores.items(), key=lambda item: item[1], reverse=True)
    return sorted_scores