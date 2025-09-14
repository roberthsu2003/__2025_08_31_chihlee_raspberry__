# Gemini CLI 啟動說明

本文件說明如何啟動和使用 Gemini 命令列介面 (CLI)。

## 1. 基本啟動

通常，Gemini CLI 會作為一個可執行檔提供。您可以在終端機中直接執行它。

### 執行 Gemini CLI
```bash
gemini
```

### 獲取幫助資訊
要查看可用的命令和選項，可以使用 `--help` 參數：
```bash
gemini --help
```
或者針對特定命令獲取幫助：
```bash
gemini [command] --help
```
例如：
```bash
gemini chat --help
```

## 2. 帶有參數啟動

您可以透過在啟動時傳遞參數來配置 Gemini CLI 的行為，例如指定模型、設定 API 金鑰或調整輸出格式。

### 設定 API 金鑰 (範例)
如果您的 Gemini CLI 需要 API 金鑰，通常會透過環境變數或啟動參數來設定：

**透過環境變數 (推薦)**
```bash
export GEMINI_API_KEY="YOUR_API_KEY_HERE"
gemini chat "Hello, Gemini!"
```
**透過命令列參數 (如果支援)**
```bash
gemini chat --api-key "YOUR_API_KEY_HERE" "Hello, Gemini!"
```
請查閱您的 Gemini CLI 文件以了解確切的 API 金鑰設定方式。

### 執行特定命令
Gemini CLI 通常包含多個子命令，用於執行不同的任務。

**範例：進行聊天**
```bash
gemini chat "請幫我寫一首關於秋天的詩。"
```

**範例：生成程式碼**
```bash
gemini code "用 Python 寫一個計算斐波那契數列的函數。"
```

## 3. 配置檔案 (如果支援)

某些 Gemini CLI 工具可能支援透過配置檔案來管理設定，例如 `~/.gemini/config.yaml` 或專案根目錄下的 `.geminirc`。請查閱相關文件以了解配置檔案的使用方法。

## 4. 更新 Gemini CLI

為了獲得最新的功能和錯誤修復，請定期更新您的 Gemini CLI。更新方法會根據您的安裝方式而有所不同。

### 透過套件管理器 (範例：npm, pip)
如果 CLI 是透過套件管理器安裝的：
```bash
npm update -g gemini-cli # 如果是 Node.js 應用
pip install --upgrade gemini-cli # 如果是 Python 應用
```

### 透過下載最新版本
如果 CLI 是直接下載的可執行檔，您可能需要從官方來源下載最新版本並替換舊版本。

---

**請注意：** 上述指令是通用範例。請務必參考您所使用的 Gemini CLI 的官方文件，以獲取最準確和最新的啟動與使用說明。

