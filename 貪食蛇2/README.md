# 視窗版繁體中文貪食蛇遊戲

這是一個使用 Python 和 Pygame 製作的貪食蛇遊戲。

## 功能特色

- 核心遊戲流程：控制蛇移動、吃食物、得分。
- 難度進程：分數越高，遊戲速度越快。
- 玩家紀錄：儲存玩家的最高分數，並顯示高分榜。
- 繁體中文介面。

## 安裝與執行

### 1. 環境設定

本專案使用 `uv` 進行虛擬環境和套件管理。

首先，建立虛擬環境：
```bash
uv venv
```

接著，啟用虛擬環境：

**在 Linux/macOS 上：**
```bash
source .venv/bin/activate
```

**在 Windows 上：**
```bash
.venv\Scripts\activate
```

### 2. 安裝依賴套件

啟用虛擬環境後，安裝所需的 `pygame` 和 `pytest` 套件：
```bash
uv add pygame
uv add pytest --group dev
```

### 3. 執行遊戲

從專案根目錄執行主程式碼：
```bash
python src/main.py
```

## 測試

執行單元測試：
```bash
pytest
```
