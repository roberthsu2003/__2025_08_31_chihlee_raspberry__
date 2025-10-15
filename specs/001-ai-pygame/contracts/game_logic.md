# 模組介面合約：貪食蛇遊戲

本文件定義了遊戲各個模組的職責和公開介面（函式簽名）。

---

## 檔案結構

```
src/
├── main.py           # 遊戲主入口和主迴圈
├── game.py           # 核心遊戲邏輯與狀態管理
├── player.py         # 玩家資料和分數管理器
├── ui.py             # UI 元件，如選單和文字渲染
├── settings.py       # 遊戲設定，如顏色、螢幕大小等
└── assets/           # 存放字型、圖片、音效等資源
    └── scores.json   # 儲存分數的檔案
```

---

## 模組詳解

### 1. `main.py`

- **職責**: 初始化 Pygame、管理主遊戲迴圈和處理遊戲狀態轉換（根據狀態機模式）。
- **介面**:
  - `main()`: 遊戲主入口函式。

### 2. `game.py`

- **職責**: 包含 `Game` 類別，管理核心遊戲世界的邏輯，包括蛇的移動、碰撞偵測、食物生成等。
- **介面 (`Game` class)**:
  - `__init__(self, screen, player_name, high_score)`: 初始化遊戲世界。
  - `run(self)`: 啟動並管理「遊戲中」狀態的迴圈。
  - `_handle_input(self, event)`: 處理玩家輸入。
  - `_update_logic(self)`: 更新遊戲狀態（蛇移動、吃食物、檢查碰撞）。
  - `_draw_elements(self)`: 將所有遊戲元素（蛇、食物、分數）繪製到螢幕上。

### 3. `player.py`

- **職責**: 負責載入、儲存和管理所有玩家的分數。
- **介面 (`ScoreManager` class)**:
  - `__init__(self, filepath)`: 初始化，指定分數檔案的路徑。
  - `load_scores(self) -> dict`: 從 JSON 檔案載入所有分數。
  - `get_high_score(self, username: str) -> int`: 獲取特定玩家的最高分，如果玩家不存在則返回 0。
  - `update_score(self, username: str, new_score: int)`: 更新玩家的分數（僅當新分數更高時），並儲存回檔案。

### 4. `ui.py`

- **職責**: 提供繪製使用者介面元素的函式，例如主選單、遊戲結束畫面和文字。
- **介面**:
  - `draw_main_menu(screen) -> bool`: 繪製主選單，等待玩家操作（例如「開始遊戲」）。如果玩家選擇開始，返回 `True`。
  - `draw_game_over_screen(screen, final_score) -> bool`: 繪製遊戲結束畫面，顯示最終分數，並等待玩家選擇「重新開始」。如果選擇重新開始，返回 `True`。
  - `draw_text(screen, text, size, x, y, color)`: 在指定位置繪製文字的輔助函式。
  - `get_player_name(screen) -> str`: 繪製一個畫面讓玩家輸入名稱。

### 5. `settings.py`

- **職責**: 集中管理所有遊戲的常數，如螢幕尺寸、顏色定義、蛇的速度等。
- **介面**: 無函式，僅包含常數變數，例如：
  - `SCREEN_WIDTH = 800`
  - `SCREEN_HEIGHT = 600`
  - `COLORS = {'WHITE': (255, 255, 255), ...}`
