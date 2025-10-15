# player.py

import json
import os

class ScoreManager:
    def __init__(self, filepath):
        self.filepath = filepath
        self.scores = self.load_scores()

    def load_scores(self) -> dict:
        """從 JSON 檔案載入分數，如果檔案不存在或為空，則返回空字典。"""
        if not os.path.exists(self.filepath):
            return {}
        try:
            with open(self.filepath, 'r', encoding='utf-8') as f:
                return json.load(f)
        except (json.JSONDecodeError, FileNotFoundError):
            return {}

    def get_high_score(self, username: str) -> int:
        """獲取特定玩家的最高分，如果玩家不存在則返回 0。"""
        return self.scores.get(username, 0)

    def update_score(self, username: str, new_score: int):
        """更新玩家的分數（僅當新分數更高時），並儲存回檔案。"""
        current_high_score = self.get_high_score(username)
        if new_score > current_high_score:
            self.scores[username] = new_score
            try:
                with open(self.filepath, 'w', encoding='utf-8') as f:
                    json.dump(self.scores, f, ensure_ascii=False, indent=4)
            except IOError as e:
                print(f"無法寫入分數檔案：{e}")
