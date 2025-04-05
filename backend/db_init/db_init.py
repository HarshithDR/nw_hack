import os
import time
from pymongo import MongoClient
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()
mongo_uri = os.environ.get('MONGO_URI')

client = MongoClient(mongo_uri)
db = client["NWHDB"]
collection = db["UserLogin"]

print(collection)

user_doc ={
    "username": "nishchal",
    "password": "wow"
}

result = collection.insert_one(user_doc)

print("Inserted ID:", result.inserted_id)
