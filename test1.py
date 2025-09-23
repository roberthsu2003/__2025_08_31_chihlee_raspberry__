import os
from dotenv import load_dotenv
from pymongo import MongoClient

load_dotenv()

MONGODB_URI = os.getenv('MONGODB_URI')
client = MongoClient(MONGODB_URI)
for db_info in client.list_database_names():
    print(db_info)

db = client['test']
print("-"*50)
for item in db['data1'].find():
    print(item)
