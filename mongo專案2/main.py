import os
from fastapi import FastAPI, HTTPException, Body, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pymongo import MongoClient
from dotenv import load_dotenv
from bson import ObjectId
from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime

# 從 .env 檔案載入環境變數
load_dotenv()

# 初始化 FastAPI 應用
app = FastAPI()

# 設定靜態檔案和模板目錄
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

# 連線到 MongoDB
client = MongoClient(os.getenv("MONGODB_URI"))
db = client.todolist
collection = db.todos

class Todo(BaseModel):
    id: str = Field(..., alias="_id")
    task: str
    date: str
    completed: bool

class CreateTodo(BaseModel):
    task: str

class UpdateTodo(BaseModel):
    task: Optional[str] = None
    date: Optional[str] = None
    completed: Optional[bool] = None

# API Routes
@app.get("/", response_class=HTMLResponse)
async def read_home(request: Request):
    active_count = collection.count_documents({"completed": False})
    completed_count = collection.count_documents({"completed": True})
    return templates.TemplateResponse("home.html", {
        "request": request,
        "active_count": active_count,
        "completed_count": completed_count
    })

@app.get("/tasks", response_class=HTMLResponse)
async def read_tasks(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/settings", response_class=HTMLResponse)
async def read_settings(request: Request):
    return templates.TemplateResponse("settings.html", {"request": request})

@app.get("/api/todos", response_model=List[Todo])
async def get_todos(completed: Optional[bool] = None):
    query = {}
    if completed is not None:
        query["completed"] = completed
    
    todos = []
    # Sort by _id descending to show newest first
    for todo in collection.find(query).sort("_id", -1):
        todo["_id"] = str(todo["_id"])
        if "date" not in todo:
            todo["date"] = "日期未設定"
        todos.append(todo)
    return todos

@app.post("/api/todos", response_model=Todo)
async def create_todo(todo: CreateTodo):
    new_todo = {
        "task": todo.task,
        "date": datetime.now().strftime("%Y年%m月%d日"),
        "completed": False
    }
    result = collection.insert_one(new_todo)
    created_todo = collection.find_one({"_id": result.inserted_id})
    created_todo["_id"] = str(created_todo["_id"])
    return created_todo

# 更新待辦事項
@app.put("/api/todos/{todo_id}", response_model=Todo)
async def update_todo(todo_id: str, todo: UpdateTodo = Body(...)):
    try:
        obj_id = ObjectId(todo_id)
    except Exception:
        raise HTTPException(status_code=400, detail="無效的 ObjectId")

    # 建立只包含已提供欄位的更新資料
    update_data = {k: v for k, v in todo.dict().items() if v is not None}

    if not update_data:
        raise HTTPException(status_code=400, detail="沒有要更新的欄位")

    result = collection.update_one({"_id": obj_id}, {"$set": update_data})

    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="找不到指定的待辦事項")

    updated_todo = collection.find_one({"_id": obj_id})
    updated_todo["_id"] = str(updated_todo["_id"])
    return Todo(**updated_todo)

# 刪除待辦事項
@app.delete("/api/todos/{todo_id}", response_model=dict)
async def delete_todo(todo_id: str):
    try:
        obj_id = ObjectId(todo_id)
    except Exception:
        raise HTTPException(status_code=400, detail="無效的 ObjectId")
        
    result = collection.delete_one({"_id": obj_id})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="找不到指定的待辦事項")
    return {"message": "待辦事項已成功刪除"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

@app.delete("/api/todos/completed", status_code=204)
async def delete_completed_todos():
    collection.delete_many({"completed": True})
    return

@app.delete("/api/todos/all", status_code=204)
async def delete_all_todos():
    collection.delete_many({})
    return

@app.delete("/api/todos/completed", status_code=204)
async def delete_completed_todos():
    collection.delete_many({"completed": True})
    return

@app.delete("/api/todos/all", status_code=204)
async def delete_all_todos():
    collection.delete_many({})
    return

