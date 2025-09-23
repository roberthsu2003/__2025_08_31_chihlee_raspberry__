# Todolist 應用程式 (mongo專案2)

這是一個使用 FastAPI、MongoDB 和純 HTML/CSS/JavaScript 建立的簡單待辦事項 (Todolist) 網頁應用程式。它提供了一個簡潔的介面來新增、檢視、更新和刪除任務。

## 功能

- **新增任務**：在輸入框中輸入新任務並新增到清單中。
- **檢視任務**：在頁面上查看所有待辦事項。
- **標記完成**：點擊任務文字即可將其標記為已完成（或取消標記）。
- **刪除任務**：點擊每個任務旁邊的「刪除」按鈕來移除它。

## 技術棧

- **後端**: [FastAPI](https://fastapi.tiangolo.com/) - 一個現代、高效能的 Python Web 框架。
- **資料庫**: [MongoDB](https://www.mongodb.com/) - 一個 NoSQL 資料庫，使用 `pymongo` 進行操作。
- **前端**:
    - HTML
    - CSS
    - JavaScript
- **環境管理**: `uv`

---

## 設定與安裝

1.  **啟動虛擬環境**:
    在開始之前，請確保您已經啟動了專案根目錄下的 `uv` 虛擬環境。從 `mongo專案2` 目錄中，您可以使用以下指令來啟動：

    ```bash
    source ../.venv/bin/activate
    ```

2.  **環境變數**:
    在專案的根目錄 (`mongo專案2/`) 下，您需要建立一個 `.env` 檔案來存放您的 MongoDB 資料庫連線字串。

    ```env
    # mongo專案2/.env
    MONGODB_URI=mongodb://your_username:your_password@your_host:your_port
    ```
    請將 `your_username`, `your_password`, `your_host`, 和 `your_port` 替換成您自己的 MongoDB 設定。

3.  **安裝依賴套件**:
    本專案的 Python 依賴套件由根目錄的 `uv` 虛擬環境統一管理。請確保您已經在專案的根目錄下安裝了所有必要的套件，例如 `fastapi`, `uvicorn`, `pymongo[srv]`, `python-dotenv`, 和 `jinja2`。

---

## 如何啟動應用程式

1.  **切換目錄**:
    首先，請確定您的終端機位於 `mongo專案2` 目錄下。

    ```bash
    cd path/to/your/project/mongo專案2
    ```

2.  **啟動伺服器**:
    使用 `uvicorn` 來啟動 FastAPI 應用程式。我們加上 `--host 0.0.0.0` 參數，是為了讓區域網路內的其他電腦也能連線到這個服務。`--reload` 參數則會讓伺服器在程式碼變更時自動重啟，非常適合開發。

    ```bash
    uvicorn main:app --reload --host 0.0.0.0
    ```

3.  **開啟應用程式**:
    伺服器啟動後，您可以在**您自己的電腦**（而非伺服器本機）的瀏覽器中，透過伺服器的 IP 位址開啟應用程式：
    `http://<伺服器的IP位址>:8000`

    例如：`http://192.168.1.100:8000`

---

## `main.py` 程式碼說明

`main.py` 是這個應用程式的後端核心，它定義了所有的 API 端點和資料庫互動邏輯。

- **初始化與設定**:
    - 載入 `.env` 檔案中的環境變數。
    - 初始化 FastAPI 應用程式。
    - 連線到 MongoDB 資料庫。
    - 掛載 `static` 目錄以提供 CSS 和 JavaScript 檔案。
    - 設定 `Jinja2Templates` 以渲染 HTML 頁面。

- **Pydantic 模型**:
    - `Todo`: 用於 API 回應和資料庫互動的基礎模型，包含 `id`, `task`, 和 `completed` 欄位。
    - `CreateTodo`: 用於**新增**待辦事項的請求模型，只包含 `task` 欄位。
    - `UpdateTodo`: 用於**更新**待辦事項的請求模型，包含可選的 `task` 和 `completed` 欄位。

- **API 端點 (Routes)**:
    - `GET /`: 根路徑，回傳並渲染 `templates/index.html` 前端頁面。
    - `GET /api/todos`: 從資料庫中讀取並回傳所有待辦事項的列表。
    - `POST /api/todos`: 接收一個新的任務，將其存入資料庫，並回傳新建的待辦事項。
    - `PUT /api/todos/{todo_id}`: 根據提供的 ID 更新一個現有的待辦事項（例如，更新任務內容或完成狀態）。
    - `DELETE /api/todos/{todo_id}`: 根據提供的 ID 從資料庫中刪除一個待辦事項。
