from fastapi import FastAPI, Request, Form, Depends, HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure
from bson import ObjectId
import os
from dotenv import load_dotenv

# 載入環境變數
load_dotenv()

import os

app = FastAPI()

# 取得目前檔案的絕對路徑
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# 掛載靜態檔案
app.mount("/static", StaticFiles(directory=os.path.join(BASE_DIR, "static")), name="static")

# 設定 Jinja2 模板
templates = Jinja2Templates(directory=os.path.join(BASE_DIR, "templates"))

# MongoDB 連線
MONGODB_URI = os.getenv("MONGODB_URI", "mongodb://localhost:27017")
client = None
db = None

@app.on_event("startup")
async def startup_db_client():
    global client, db
    try:
        client = MongoClient(MONGODB_URI)
        client.admin.command('ping')
        db = client.todolist_db
        print("MongoDB 連線成功！")
    except ConnectionFailure as e:
        print(f"MongoDB 連線失敗: {e}")
        raise HTTPException(status_code=500, detail="無法連線到資料庫")

@app.on_event("shutdown")
async def shutdown_db_client():
    global client
    if client:
        client.close()
        print("MongoDB 連線關閉。")

# 依賴注入，取得資料庫連線
def get_database():
    if db is None:
        raise HTTPException(status_code=500, detail="資料庫尚未連線")
    return db

# 路由：首頁 - 顯示所有待辦事項
@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request, db_conn = Depends(get_database)):
    todos = []
    try:
        todos_cursor = db_conn.todos.find({})
        for todo in todos_cursor:
            todo["_id"] = str(todo["_id"]) # 將 ObjectId 轉換為字串
            todos.append(todo)
    except Exception as e:
        print(f"讀取待辦事項失敗: {e}")
        raise HTTPException(status_code=500, detail="無法讀取待辦事項")
    return templates.TemplateResponse("index.html", {"request": request, "todos": todos})

# 路由：新增待辦事項
@app.post("/add", response_class=RedirectResponse)
async def add_todo(request: Request, title: str = Form(...), db_conn = Depends(get_database)):
    if not title.strip():
        raise HTTPException(status_code=400, detail="待辦事項標題不能為空")
    try:
        db_conn.todos.insert_one({"title": title, "completed": False})
    except Exception as e:
        print(f"新增待辦事項失敗: {e}")
        raise HTTPException(status_code=500, detail="無法新增待辦事項")
    return RedirectResponse(url="/", status_code=303)

# 路由：更新待辦事項狀態
@app.post("/update/{todo_id}", response_class=RedirectResponse)
async def update_todo(request: Request, todo_id: str, db_conn = Depends(get_database)):
    try:
        db_conn.todos.update_one({"_id": ObjectId(todo_id)}, {"$set": {"completed": True}})
    except Exception as e:
        print(f"更新待辦事項失敗: {e}")
        raise HTTPException(status_code=500, detail="無法更新待辦事項")
    return RedirectResponse(url="/", status_code=303)

# 路由：刪除待辦事項
@app.post("/delete/{todo_id}", response_class=RedirectResponse)
async def delete_todo(request: Request, todo_id: str, db_conn = Depends(get_database)):
    try:
        db_conn.todos.delete_one({"_id": ObjectId(todo_id)})
    except Exception as e:
        print(f"刪除待辦事項失敗: {e}")
        raise HTTPException(status_code=500, detail="無法刪除待辦事項")
    return RedirectResponse(url="/", status_code=303)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
