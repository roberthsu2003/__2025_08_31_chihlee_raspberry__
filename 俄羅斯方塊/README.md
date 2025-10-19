# 俄羅斯方塊

## GEMINI CLI 設定

### System and User Prompt

*   **System Prompt**: 用於設定 AI 的核心行為和角色。例如，在 `.gemini/settings.json` 中設定 AI 為一位有耐心的 Python 老師。
*   **User Prompt**: 使用者在每次對話中輸入的指令或問題。

### Project Prompt

*   **Project Prompt**: 通常儲存在專案根目錄下的 `GEMINI.md` 檔案中。這個檔案提供了專案特定的上下文，讓 AI 在處理您的請求時，能夠有更一致和貼切的表現。

#### 範例 `GEMINI.md`

```markdown
---
Context from: ../../../.gemini/GEMINI.md
---
## AI遵守行為
- 所有回覆請使用繁體中文版
- 你是一個有耐心的python老師
--- End of Context from: ../../../.gemini/GEMINI.md
---
```

## GEMINI CLI 安裝與操作

### 安裝

```bash
# 透過 pipx 安stall
pipx install google-gemini-cli
```

### 基本操作

```bash
# 登入您的 Google 帳號
gemini auth login

# 開始對話
gemini chat

# 執行特定指令
gemini --prompt "請幫我寫一個 python 函式來計算費氏數列"
```

## AI遵守行為
- 所有回覆請使用繁體中文版
- 你是一個有耐心的python老師