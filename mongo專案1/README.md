# 待辦事項應用程式 (FastAPI + MongoDB)

這是一個使用 FastAPI 作為後端 API、MongoDB 作為資料庫，並以 HTML/CSS/JavaScript 作為前端的待辦事項應用程式。

## 功能

- **新增待辦事項**：輸入待辦事項標題並新增。
- **完成待辦事項**：將待辦事項標題標記為已完成。
- **刪除待辦事項**：從列表中移除待辦事項。
- **顯示所有待辦事項**：在首頁顯示所有待辦事項及其狀態。

## 專案結構

```
mongo專案1/
├── main.py
├── static/
│   ├── style.css
│   └── script.js
└── templates/
    └── index.html
```

## 環境變數 (.env)

請確保您的專案根目錄 (`/home/pi/Documents/GitHub/2025_08_31_chihlee_raspberry`) 下有一個 `.env` 檔案，並包含以下 MongoDB 連線字串：

```
MONGODB_URI=mongodb://pi:raspberry@localhost:27017
```

## 安裝與啟動

請依照以下步驟啟動應用程式：

1.  **啟用虛擬環境**：

    ```bash
    source ./.venv/bin/activate
    ```

2.  **安裝必要的 Python 套件**：

    ```bash
    uv add fastapi uvicorn pymongo python-multipart
    ```

3.  **啟動 FastAPI 應用程式**：

    ```bash
    uvicorn mongo專案1.main:app --reload --host 0.0.0.0 --port 8000
    ```

    *   `--reload` 參數會在程式碼變更時自動重載伺服器，方便開發。
    *   `--host 0.0.0.0` 允許從任何 IP 位址訪問應用程式。
    *   `--port 8000` 設定應用程式在 8000 埠運行。

啟動後，您可以在瀏覽器中訪問 `http://localhost:8000` 來使用待辦事項應用程式。

## `main.py` 說明

`main.py` 是 FastAPI 應用程式的核心檔案，負責處理以下功能：

-   **FastAPI 應用程式實例**：初始化 FastAPI 應用程式。
-   **靜態檔案掛載**：將 `static` 目錄下的 CSS 和 JavaScript 檔案掛載到 `/static` 路徑。
-   **Jinja2 模板設定**：設定 `templates` 目錄為 HTML 模板的存放位置。
-   **MongoDB 連線**：
    -   在應用程式啟動時 (startup event) 建立 MongoDB 連線。
    -   在應用程式關閉時 (shutdown event) 關閉 MongoDB 連線。
    -   使用 `MONGODB_URI` 環境變數來配置 MongoDB 連線字串。
-   **資料庫依賴注入**：提供 `get_database` 函數，用於在路由中方便地取得 MongoDB 資料庫連線。
-   **路由定義**：
    -   `GET /`：顯示所有待辦事項的 HTML 頁面。
    -   `POST /add`：處理新增待辦事項的請求。
    -   `POST /update/{todo_id}`：處理更新待辦事項狀態（標記為完成）的請求。
    -   `POST /delete/{todo_id}`：處理刪除待辦事項的請求。
-   **錯誤處理**：對資料庫連線失敗、無效輸入等情況進行錯誤處理。

這個應用程式提供了一個完整的 CRUD 範例，展示了如何將 FastAPI 與 MongoDB 和 Jinja2 模板結合使用來建立一個簡單的網頁應用程式。