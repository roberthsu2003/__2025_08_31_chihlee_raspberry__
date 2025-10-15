# 資料模型：貪食蛇遊戲

本文件定義了遊戲中使用的主要資料實體和結構。

---

## 1. 持久化實體

這些是需要儲存到檔案系統中的資料。

### PlayerScore

代表一個玩家的紀錄。

- **欄位**:
  - `username` (String): 唯一的玩家名稱，作為主鍵。
  - `high_score` (Integer): 該玩家的歷史最高分。

- **儲存格式**: 整個專案的玩家分數將被儲存在一個 JSON 檔案中，格式如下：

  ```json
  {
    "player1_name": 150,
    "player2_name": 200
  }
  ```

---

## 2. 記憶體中實體

這些是遊戲運行時存在於記憶體中的資料結構。

### GameState

代表整個遊戲應用程式的當前狀態。

- **欄位**:
  - `current_state` (String): 當前的遊戲狀態，為以下其中之一：
    - `'MAIN_MENU'`: 主選單畫面
    - `'GET_PLAYER_NAME'`: 輸入玩家名稱畫面
    - `'PLAYING'`: 遊戲進行中
    - `'GAME_OVER'`: 遊戲結束畫面
  - `player_name` (String): 當前登入的玩家名稱。
  - `high_score` (Integer): 當前玩家的最高分。
  - `current_score` (Integer): 本局遊戲的即時分數。
  - `level` (Integer): 當前的遊戲等級/速度。

### Snake

代表遊戲中的蛇。

- **欄位**:
  - `body` (List of Tuples): 一個座標 `(x, y)` 的列表，代表蛇身體的每一節。列表的第一個元素是蛇頭。
  - `direction` (String): 蛇的前進方向，為以下其中之一：`'UP'`, `'DOWN'`, `'LEFT'`, `'RIGHT'`。

### Food

代表遊戲中的食物。

- **欄位**:
  - `position` (Tuple): 食物所在的座標 `(x, y)`。
