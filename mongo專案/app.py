import os
from flask import Flask, request, jsonify
from pymongo import MongoClient
from dotenv import load_dotenv
from bson.objectid import ObjectId, InvalidId

load_dotenv()

app = Flask(__name__)

# MongoDB connection
mongo_uri = os.getenv("MONGODB_URI")
client = MongoClient(mongo_uri)
db = client.mydatabase
items_collection = db.items

@app.route('/items', methods=['POST'])
def create_item():
    data = request.json
    if not data or 'name' not in data:
        return jsonify({"error": "名稱為必填項"}), 400
    
    result = items_collection.insert_one(data)
    return jsonify({"message": "項目已建立", "id": str(result.inserted_id)}), 201

@app.route('/items', methods=['GET'])
def get_items():
    limit = request.args.get('limit', type=int)
    items = []
    if limit:
        for item in items_collection.find().limit(limit):
            item['_id'] = str(item['_id'])
            items.append(item)
    else:
        for item in items_collection.find():
            item['_id'] = str(item['_id'])
            items.append(item)
    return jsonify(items), 200

@app.route('/items/<id>', methods=['GET'])
def get_item(id):
    try:
        item = items_collection.find_one({"_id": ObjectId(id)})
        if item:
            item['_id'] = str(item['_id'])
            return jsonify(item), 200
        return jsonify({"error": "未找到項目"}), 404
    except InvalidId:
        return jsonify({"error": "無效的ID格式"}), 400
    except Exception as e:
        return jsonify({"error": f"伺服器錯誤: {str(e)}"}), 500

@app.route('/items/<id>', methods=['PUT'])
def update_item(id):
    data = request.json
    if not data:
        return jsonify({"error": "未提供資料"}), 400
    
    try:
        result = items_collection.update_one({"_id": ObjectId(id)}, {"$set": data})
        if result.matched_count:
            return jsonify({"message": "項目已更新"}), 200
        return jsonify({"error": "未找到項目"}), 404
    except InvalidId:
        return jsonify({"error": "無效的ID格式"}), 400
    except Exception as e:
        return jsonify({"error": f"伺服器錯誤: {str(e)}"}), 500

@app.route('/items/<id>', methods=['DELETE'])
def delete_item(id):
    try:
        result = items_collection.delete_one({"_id": ObjectId(id)})
        if result.deleted_count:
            return jsonify({"message": "項目已刪除"}), 200
        return jsonify({"error": "未找到項目"}), 404
    except InvalidId:
        return jsonify({"error": "無效的ID格式"}), 400
    except Exception as e:
        return jsonify({"error": f"伺服器錯誤: {str(e)}"}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)
