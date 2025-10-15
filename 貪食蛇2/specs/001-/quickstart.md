# Quickstart Guide for 視窗版繁體中文貪食蛇遊戲

## 快速開始

本指南將協助您快速啟動並執行貪食蛇遊戲。

### 1. 環境設定

確保您的系統已安裝 Python 3.x。建議使用 `uv` 建立虛擬環境以管理專案依賴。

```bash
# 進入專案根目錄
cd /home/pi/Documents/GitHub/2025_08_31_chihlee_raspberry/貪食蛇2

# 建立並啟用虛擬環境 (如果尚未建立)
uv venv
source .venv/bin/activate

# 安裝專案依賴 (Pygame)
uv add pygame
```

### 2. 執行遊戲

在虛擬環境啟用後，您可以直接執行 `main.py` 來啟動遊戲。

```bash
python src/main.py
```

### 3. 遊戲操作

- **方向鍵**: 控制蛇的移動方向。
- **遊戲結束畫面**: 提供「重新開始」和「離開遊戲」選項。

### 4. 玩家紀錄

- 遊戲開始前會提示輸入玩家姓名。
- 玩家的最高分數將儲存在 `scores.json` 檔案中。
