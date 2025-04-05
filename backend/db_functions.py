import os
from pymongo import MongoClient
from dotenv import load_dotenv
from datetime import datetime
from bson import ObjectId
from pymongo.errors import PyMongoError
from typing import Dict, Any, Optional


load_dotenv()
mongo_uri = os.environ.get('MONGO_URI')

client = MongoClient(mongo_uri)
db = client["NWHDB"]
collection = db["UserLogin"]

def validate_db_connection() -> bool:
    """
    Checks if the database connection is alive.
    Returns True if connected, False otherwise.
    """
    try:
        client.admin.command('ping')
        print("✅ MongoDB connection is valid.")
        return True
    except PyMongoError as e:
        print(f"❌ Failed to connect to MongoDB: {e}")
        return False

def create_user(username: str, password: str) -> Optional[Dict[str, Any]]:
    """
    Inserts a document with username and password into the UserLogin collection.
    Returns the inserted document ID or None if insertion failed.
    """
    if validate_db_connection():
        if not username or not password:
            print("❗ Username and password cannot be empty.")
            return None
        try:
            user_doc = {
                "username": username,
                "password": password,
            }
            result = collection.insert_one(user_doc)
            print(f"✅ User created with ID: {result.inserted_id}")
            return {"_id": str(result.inserted_id)}
        except PyMongoError as e:
            print(f"❌ Error inserting user: {e}")
            return None
        
def validate_login(username: str, password: str) -> Optional[Dict[str, Any]]:
    """
    Validates user login by checking if the provided username and password match a record in the database.
    Returns the user's unique ID if successful, otherwise returns None.
    """
    if validate_db_connection():
        if not username or not password:
            print("❗ Username and password cannot be empty.")
            return None
        try:
            user = collection.find_one({"username": username, "password": password})
            if user:
                print(f"✅ Login successful for user: {username}")
                return {"_id": str(user["_id"]), "username": user["username"]}
            else:
                print("❌ Invalid username or password.")
                return None
        except PyMongoError as e:
            print(f"❌ Error validating login: {e}")
            return None

 
 
if __name__ == "__main__":
    create_user("test", "WOWOWOW")
    print(validate_login("test", "WOWOWOW"))
