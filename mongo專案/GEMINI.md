## AI工作目錄

/mongo專案

## 專案目標

使用 Streamlit、Flask 和 MongoDB 建立一個具備完整 CRUD (Create, Read, Update, Delete) 功能的 Todo List 網頁應用程式。

## 技術棧

- **前端 (Frontend):** Streamlit
- **後端 (Backend):** Flask
- **資料庫 (Database):** MongoDB

## 專案結構

```
.
├── app.py              # Flask 後端 API 伺服器
├── streamlit_app.py    # Streamlit 前端 UI 應用
├── .env                # 環境變數檔案
└── README.md           # 專案說明文件
```

## 環境設定

### 1. 虛擬環境

此專案使用位於根目錄 (`2025_08_31_chihlee_raspberry`) 的 `uv` 虛擬環境。

- **進入虛擬環境:**
  ```bash
  source ../.venv/bin/activate
  ```

### 2. 安裝套件

必要的 Python 套件如下。如果尚未安裝，請使用 `uv add`：
```bash
uv add flask pymongo python-dotenv streamlit requests
```

### 3. 環境變數

在 `/mongo專案` 目錄下建立 `.env` 檔案，內容如下：
```
MONGODB_URI=mongodb://pi:raspberry@localhost:27017
```

## 如何執行

應用程式需要同時執行後端和前端兩個部分。

1.  **執行後端 (Flask):**
    開啟一個終端機，進入 `/mongo專案` 目錄，然後執行：
    ```bash
    ../.venv/bin/python app.py
    ```
    伺服器將會啟動在 `http://127.0.0.1:5001`。

2.  **執行前端 (Streamlit):**
    開啟**另一個**終端機，進入 `/mongo專案` 目錄，然後執行：
    ```bash
    ../.venv/bin/streamlit run streamlit_app.py
    ```
    在瀏覽器中打開 Streamlit 提供的 URL (通常是 `http://localhost:8501`) 即可使用。

## 程式碼重點

### 後端 API (`app.py`)

- 使用 **Flask** 建立 RESTful API。
- **Endpoints:**
  - `GET /todos`: 取得所有待辦事項。
  - `POST /todos`: 新增一筆待辦事項。
  - `PUT /todos/<id>`: 更新指定 ID 的待辦事項 (完成狀態)。
  - `DELETE /todos/<id>`: 刪除指定 ID 的待辦事項。
- 使用 **Pymongo** 與 MongoDB 互動。
- 使用 **python-dotenv** 讀取 `.env` 中的資料庫連線字串。

### 前端介面 (`streamlit_app.py`)

- 使用 **Streamlit** 快速建立互動式網頁介面。
- 使用 **requests** 套件呼叫後端 Flask API。
- **UI 元件:**
  - `st.text_input` 和 `st.button` 用於新增任務。
  - `st.checkbox` 用於更新任務完成狀態。
  - `st.columns` 用於排版。
  - `st.rerun()` 在操作後立即刷新介面，提供流暢的使用體驗。
