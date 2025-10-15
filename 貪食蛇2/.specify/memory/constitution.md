<!--
SYNC IMPACT REPORT
- Version change: 0.0.0 → 1.0.0
- Added sections:
  - Project Name
  - Versioning
  - Governance
  - Principle 1: 遊戲開發框架 (Game Development Framework)
  - Principle 2: 核心遊戲功能 (Core Gameplay Features)
  - Principle 3: 程式碼風格與註解 (Code Style and Comments)
  - Principle 4: 虛擬環境管理 (Virtual Environment Management)
  - Principle 5: 文件導向 (Documentation-Oriented)
- Removed sections: None
- Templates requiring updates:
  - ✅ .specify/templates/plan-template.md (created)
  - ✅ .specify/templates/spec-template.md (created)
  - ✅ .specify/templates/tasks-template.md (created)
- Follow-up TODOs: None
-->

# 專案章程：貪食蛇2

## [PROJECT_NAME]

貪食蛇2

## 版本

- **章程版本**: 1.0.0
- **批准日期**: 2025-10-15
- **最後修訂日期**: 2025-10-15

## 治理

本章程是專案的最高指導原則。所有開發工作和貢獻都必須遵守。

- **修訂流程**: 任何對章程的修改都必須經過團隊討論，並在更新後反映於 `LAST_AMENDED_DATE` 和 `CONSTITUTION_VERSION`。
- **版本控制**:
  - **MAJOR**: 重大或不相容的原則變更。
  - **MINOR**: 新增原則或擴展現有原則。
  - **PATCH**: 文字修正、澄清或格式調整。

---

## 原則

### 原則 1: 遊戲開發框架 (Game Development Framework)

**規則**: 專案必須使用 `pygame` 函式庫進行開發。

**理由**: 為了保持技術堆疊的一致性，並專注於學習和應用 `pygame` 的相關知識。

### 原則 2: 核心遊戲功能 (Core Gameplay Features)

**規則**: 遊戲必須實現以下核心功能：計分、等級制度、背景音樂和音效。

**理由**: 這些是構成一個完整且富有趣味性的貪食蛇遊戲的基礎元素，能提供良好的玩家體驗。

### 原則 3: 程式碼風格與註解 (Code Style and Comments)

**規則**: 所有 Python 程式碼都必須遵循 PEP 8 風格指南。對於複雜的演算法或遊戲邏輯，必須添加清晰的繁體中文註解。

**理由**: 統一的程式碼風格有助於提高可讀性。清晰的註解能讓協作者（包括 AI）更容易理解程式碼的意圖，方便後續維護和迭代。

### 原則 4: 虛擬環境管理 (Virtual Environment Management)

**規則**: 專案的 Python 環境和相依套件必須使用 `uv` 進行管理。

**理由**: 確保開發環境的獨立性、一致性和可重現性，避免與系統或其他專案產生衝突。

### 原則 5: 文件導向 (Documentation-Oriented)

**規則**: 專案的頂層目標、AI 的工作範圍和特定指示應記錄在根目錄的 `GEMINI.md` 檔案中。

**理由**: 為 AI 協作者提供清晰的上下文和指導，確保其行為符合專案預期。
