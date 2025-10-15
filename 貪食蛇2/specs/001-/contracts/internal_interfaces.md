# Internal Interfaces for 視窗版繁體中文貪食蛇遊戲

## Module Interfaces

### Game Module

- **功能**: 管理遊戲主循環、狀態更新、事件處理和渲染。
- **介面**:
    - `init_game()`: 初始化 Pygame 和遊戲視窗。
    - `run_game()`: 啟動遊戲主循環。
    - `handle_input()`: 處理玩家輸入 (鍵盤事件)。
    - `update_game_state()`: 更新蛇、食物、分數、等級等遊戲狀態。
    - `draw_elements()`: 渲染所有遊戲元素到螢幕。
    - `display_game_over_screen()`: 顯示遊戲結束畫面。
    - `display_high_score_prompt()`: 顯示輸入玩家姓名的提示。
    - `display_high_score_list()`: 顯示高分榜。

### Snake Module

- **功能**: 管理蛇的行為，包括移動、成長、碰撞檢測。
- **介面**:
    - `__init__(start_position)`: 初始化蛇的身體和方向。
    - `move()`: 根據當前方向移動蛇。
    - `grow()`: 增加蛇的長度。
    - `check_collision(head_position)`: 檢查蛇頭是否與牆壁或自身碰撞。
    - `get_head_position()`: 獲取蛇頭的當前位置。
    - `get_body_positions()`: 獲取蛇身體所有節點的位置。

### Food Module

- **功能**: 管理食物的生成和位置。
- **介面**:
    - `__init__(game_area)`: 初始化食物。
    - `spawn_food()`: 在隨機位置生成食物。
    - `get_position()`: 獲取食物的當前位置。

### Scores Module

- **功能**: 管理玩家分數的載入、儲存和更新。
- **介面**:
    - `load_scores()`: 從 `scores.json` 載入所有玩家的最高分數。
    - `save_scores(player_name, score)`: 儲存或更新玩家的最高分數到 `scores.json`。
    - `get_player_high_score(player_name)`: 獲取指定玩家的最高分數。
    - `get_all_high_scores()`: 獲取所有玩家的最高分數列表。

### Config Module

- **功能**: 儲存遊戲的設定參數，如視窗大小、顏色、速度等。
- **介面**:
    - 提供常數或函數來獲取配置值。
