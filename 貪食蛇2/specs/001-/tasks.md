# Tasks for 視窗版繁體中文貪食蛇遊戲

## Feature: 視窗版繁體中文貪食蛇遊戲

本文件列出了開發「視窗版繁體中文貪食蛇遊戲」的詳細任務，並依據使用者故事的優先級進行組織。

## Implementation Strategy

本專案將採用 MVP (最小可行產品) 優先、增量交付的策略。首先完成核心遊戲流程，然後逐步加入難度調整和玩家紀錄功能。

## Dependencies

使用者故事的完成順序如下：

1.  **User Story 1 - 核心遊戲流程** (P1)
2.  **User Story 2 - 遊戲進程與難度** (P2)
3.  **User Story 3 - 玩家紀錄** (P3)

每個使用者故事內部任務的完成順序將遵循：測試 (若有) → 模型 → 服務 → 端點/UI → 整合。

## Parallel Execution Examples

- **User Story 1**: 蛇的移動邏輯 (`src/snake.py`) 和食物生成邏輯 (`src/food.py`) 可以獨立開發。
- **User Story 3**: 玩家姓名輸入介面和高分榜顯示介面可以獨立開發。

## Phase 1: Setup (專案初始化)

- [X] T001 建立 `src/config.py` 檔案，定義遊戲視窗大小、顏色、速度等基本設定。
- [X] T002 在 `src/main.py` 中初始化 Pygame 模組和遊戲視窗。

## Phase 2: Foundational (基礎功能)

- [X] T003 建立 `src/snake.py` 檔案，實作蛇的初始化、移動、獲取頭部和身體位置的方法。
- [X] T004 建立 `src/food.py` 檔案，實作食物的初始化和隨機生成方法。
- [X] T005 建立 `src/game_state.py` 檔案，定義遊戲狀態的資料結構 (分數、等級、蛇、食物位置)。
- [X] T006 建立 `src/game.py` 檔案，實作遊戲主循環的骨架，包含初始化、事件處理、狀態更新和渲染的空方法。
- [X] T007 在 `src/main.py` 中整合 `Game` 模組，建立遊戲實例並呼叫其主循環方法。

## Phase 3: User Story 1 - 核心遊戲流程 [P1]

**目標**: 玩家可以啟動遊戲，使用方向鍵控制蛇的移動來吃食物、獲得分數，並在蛇死亡時看到遊戲結束畫面。

**獨立測試標準**: 啟動遊戲，玩一局直到遊戲結束，確認遊戲循環正常，蛇能移動、吃食物、成長、得分，並在碰撞後顯示遊戲結束畫面。

- [X] T008 [US1] 在 `src/snake.py` 中實作蛇的成長邏輯。
- [X] T009 [US1] 在 `src/snake.py` 中實作蛇與牆壁及自身碰撞的檢測邏輯。
- [X] T010 [US1] 在 `src/game.py` 的 `update_game_state` 方法中，實作蛇吃到食物後，食物消失、蛇成長、分數增加的邏輯。
- [X] T011 [US1] 在 `src/game.py` 的 `update_game_state` 方法中，實作碰撞後遊戲結束的邏輯。
- [X] T012 [US1] 在 `src/game.py` 的 `draw_elements` 方法中，渲染蛇、食物、分數和遊戲結束畫面。
- [X] T013 [US1] 在 `src/game.py` 中實作重新開始遊戲的選項和邏輯。
- [X] T014 [US1] 在 `src/game.py` 的 `handle_input` 方法中，處理鍵盤方向鍵輸入以控制蛇的移動方向。

## Phase 4: User Story 2 - 遊戲進程與難度 [P2]

**目標**: 隨著玩家分數的提高，遊戲速度會加快，從而增加遊戲的挑戰性。

**獨立測試標準**: 玩遊戲並持續得分，觀察遊戲速度是否在達到特定分數閾值後明顯提升，並顯示正確的等級。

- [X] T015 [US2] 在 `src/game.py` 或 `src/config.py` 中定義等級提升的閾值和速度增加的固定值。
- [X] T016 [US2] 在 `src/game.py` 的 `update_game_state` 方法中，實作根據分數提升遊戲等級和速度的邏輯。
- [X] T017 [US2] 在 `src/game.py` 的 `draw_elements` 方法中，渲染當前遊戲等級。

## Phase 5: User Story 3 - 玩家紀錄 [P3]

**目標**: 遊戲開始前，系統會提示玩家輸入姓名。若已輸入，則遊戲結束後不再提示。系統會記錄玩家的姓名和本次分數，並在某處顯示歷史高分。

**獨立測試標準**: 啟動遊戲，確認在遊戲開始前會提示輸入姓名。輸入姓名後完成一局遊戲，檢查高分是否被記錄。重新啟動遊戲，確認不再提示輸入姓名。確認遊戲中顯示玩家名稱和個人最高紀錄，並在超越時有視覺提示。確認高分榜顯示正常。

- [X] T018 [US3] 建立 `src/scores.py` 檔案，實作 `load_scores()`、`save_scores(player_name, score)`、`get_player_high_score(player_name)` 和 `get_all_high_scores()` 方法，處理 `scores.json` 檔案。
- [X] T019 [US3] 在 `src/game.py` 中實作遊戲開始前提示玩家輸入姓名的邏輯，並處理已輸入姓名後不再提示的情況。
- [X] T020 [US3] 在 `src/game.py` 的 `draw_elements` 方法中，渲染當前玩家的名稱和個人最高分數。
- [X] T021 [US3] 在 `src/game.py` 的 `update_game_state` 方法中，實作當前分數超過個人最高紀錄時的視覺提示邏輯。
- [X] T022 [US3] 在 `src/game.py` 中實作顯示獨立高分榜畫面的邏輯。
- [X] T023 [US3] 在 `src/game.py` 中，遊戲結束時呼叫 `scores.save_scores()` 儲存玩家分數。

## Phase 6: Polish & Cross-Cutting Concerns (優化與跨領域考量)

- [X] T024 確保遊戲中所有文字（如分數、等級、選單、結束畫面）都以繁體中文顯示，並使用 `src/assets/fonts/NotoSansTC-Regular.otf` 字體。
- [X] T025 在 `src/game.py` 中實作玩家輸入極長或包含特殊字元姓名時的錯誤訊息處理。
- [X] T026 實作遊戲視窗被縮放或失去焦點時的處理 (例如：暫停遊戲)。
- [X] T027 在 `src/main.py` 或 `src/game.py` 中加入基本的錯誤日誌記錄，僅記錄關鍵錯誤。