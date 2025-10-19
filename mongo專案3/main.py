from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pymongo import MongoClient
from dotenv import load_dotenv
import os
from pydantic import BaseModel, Field
from bson import ObjectId
from typing import Optional, List

from typing import Any, Optional, List
from pydantic import BaseModel, Field, GetJsonSchemaHandler
from pydantic.json_schema import JsonSchemaValue
from pydantic_core import core_schema

# 處理 BSON ObjectId，相容 Pydantic v2
class PyObjectId(ObjectId):
    @classmethod
    def __get_pydantic_core_schema__(
        cls,
        _source_type: Any,
        _handler: Any,
    ) -> core_schema.CoreSchema:
        def validate(v: str) -> ObjectId:
            if not ObjectId.is_valid(v):
                raise ValueError(f"Invalid ObjectId: {v}")
            return ObjectId(v)

        return core_schema.json_or_python_schema(
            python_schema=core_schema.union_schema(
                [
                    core_schema.is_instance_schema(ObjectId),
                    core_schema.chain_schema([core_schema.str_schema(), core_schema.no_info_plain_validator_function(validate)]),
                ]
            ),
            json_schema=core_schema.str_schema(
                pattern=r"^[0-9a-fA-F]{24}$",
            ),
            serialization=core_schema.plain_serializer_function_ser_schema(lambda x: str(x)),
        )

# 載入 .env 檔案中的環境變數
load_dotenv()
MONGODB_URI = os.getenv("MONGODB_URI")

# --- Pydantic 模型 ---
class TodoCreate(BaseModel):
    title: str
    completed: bool = False

class TodoUpdate(BaseModel):
    title: Optional[str] = None
    completed: Optional[bool] = None

class Todo(BaseModel):
    id: PyObjectId = Field(alias="_id")
    title: str
    completed: bool

    class Config:
        populate_by_name = True
        arbitrary_types_allowed = True
        json_schema_extra = {
            "example": {
                "id": "60d5ec49e7afde3a8a2e8e21",
                "title": "範例事項",
                "completed": False,
            }
        }

# --- FastAPI 應用程式 ---
app = FastAPI()

# 掛載靜態檔案目錄
app.mount("/static", StaticFiles(directory="static"), name="static")
# 設定模板目錄
templates = Jinja2Templates(directory="templates")

client = None
db = None

@app.on_event("startup")
async def startup_db_client():
    global client, db
    # 建立 MongoDB 連線
    client = MongoClient(MONGODB_URI)
    db = client.get_database("todo_db")
    print("成功連線到 MongoDB...")

@app.on_event("shutdown")
async def shutdown_db_client():
    global client
    # 關閉 MongoDB 連線
    client.close()
    print("MongoDB 連線已關閉。")

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

# --- API Endpoints ---

@app.post("/api/todos", response_model=Todo, response_model_by_alias=False)
async def create_todo(todo: TodoCreate):
    todo_data = todo.model_dump()
    new_todo = db.todos.insert_one(todo_data)
    created_todo = db.todos.find_one({"_id": new_todo.inserted_id})
    return created_todo

@app.get("/api/todos", response_model=List[Todo], response_model_by_alias=False)
async def get_todos():
    todos = list(db.todos.find({}))
    return todos

@app.put("/api/todos/{todo_id}", response_model=Todo, response_model_by_alias=False)
async def update_todo(todo_id: str, todo: TodoUpdate):
    update_data = todo.model_dump(exclude_unset=True)
    if len(update_data) >= 1:
        db.todos.update_one({"_id": ObjectId(todo_id)}, {"$set": update_data})
    
    updated_todo = db.todos.find_one({"_id": ObjectId(todo_id)})
    if updated_todo:
        return updated_todo
    return {"error": "Todo not found"}

@app.delete("/api/todos/{todo_id}")
async def delete_todo(todo_id: str):
    try:
        delete_result = db.todos.delete_one({"_id": ObjectId(todo_id)})
        if delete_result.deleted_count == 1:
            return {"message": "Todo deleted successfully"}
        return {"error": "Todo not found"}
    except Exception:
        # 當傳入的 todo_id 不是有效的 ObjectId 格式時，捕捉例外
        return {"error": "Invalid ID format"}
