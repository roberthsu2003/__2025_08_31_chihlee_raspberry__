# mongo專案3 - TODO List

這是一個待辦事項列表，用於追蹤 `mongo專案3` 的開發進度。

## 第一階段：專案基礎設定

- [x] 建立 `main.py` 作為 FastAPI 應用程式的進入點。
- [x] 建立 `requirements.txt` 並加入 `fastapi`, `uvicorn`, `pymongo`, `python-dotenv`。
- [x] 建立 `.env` 檔案並設定 `MONGODB_URI`。
- [x] 建立 `static` 資料夾來存放 CSS 和 JavaScript 檔案。
- [x] 建立 `templates` 資料夾來存放 HTML 檔案。

## 第二階段：後端開發 (FastAPI)

- [x] 在 `main.py` 中建立 FastAPI 應用程式實例。
- [x] 實作與 MongoDB 的連線邏輯，並在啟動時連線，關閉時中斷。
- [x] 使用 Pydantic 建立 `Todo` 資料模型 (model)，應包含 `id`, `title`, `completed` 等欄位。
- [x] 建立 `POST /api/todos` API 端點來新增待辦事項。
- [x] 建立 `GET /api/todos` API 端點來讀取所有待辦事項。
- [x] 建立 `PUT /api/todos/{todo_id}` API 端點來更新待辦事項的狀態 (例如：標記為已完成)。
- [x] 建立 `DELETE /api/todos/{todo_id}` API 端點來刪除待辦事項。
- [x] 建立一個根路徑 `/` 來提供 `index.html` 頁面。

## 第三階段：前端開發 (HTML/CSS/JavaScript)

- [x] 在 `templates` 中建立 `index.html` 作為主要頁面。
- [x] 在 `index.html` 中設計待辦事項列表的 UI 結構，包含輸入框、新增按鈕、以及待辦事項列表。
- [x] 在 `static` 中建立 `style.css` 來美化頁面，使其具有現代感且易於使用。
- [x] 在 `static` 中建立 `script.js` 來處理所有前端互動邏輯。
- [x] 在 `script.js` 中實作以下功能：
    - [x] 頁面載入時，使用 `fetch` 從 `GET /api/todos` 取得並動態顯示所有待辦事項。
    - [x] 讓使用者可以透過表單新增待辦事項，並呼叫 `POST /api/todos` API。
    - [x] 成功新增後，重新整理列表以顯示新的待辦事項。
    - [x] 為每個待辦事項加上「完成」按鈕，點擊後呼叫 `PUT /api/todos/{todo_id}` API 來更新狀態。
    - [x] 為每個待辦事項加上「刪除」按鈕，點擊後呼叫 `DELETE /api/todos/{todo_id}` API 來刪除項目。
    - [x] 更新或刪除後，即時更新前端畫面。

## 第四階段：整合與測試

- [ ] 確保 FastAPI 可以正確提供靜態檔案 (CSS/JS) 和 HTML 模板。
- [ ] 完整測試前端與後端的 CRUD (新增、讀取、更新、刪除) 功能流程。
- [ ] 進行簡單的錯誤處理，例如：當後端 API 呼叫失敗時，在前端顯示提示。
- [ ] 撰寫 `README.md` 檔案，說明如何設定環境、安裝依賴套件以及如何執行此專案。