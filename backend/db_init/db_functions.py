import os
from pymongo import MongoClient
from dotenv import load_dotenv
from datetime import datetime
from bson import ObjectId
from pymongo.errors import PyMongoError
from typing import Dict, Any, Optional, Union

import sys
sys.path.append('../')

load_dotenv()
mongo_uri = os.environ.get('MONGO_URI')

client = MongoClient(mongo_uri)
db = client["NWHDB"]
collection = db["UserLogin"]
profile_collection = db['ProfileCollection']

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


def create_profile(name: str, geo_location: Dict[str, Union[float, Any]], acres: Union[float, int]) -> Optional[Dict[str, Any]]:
    """
    Inserts a document into ProfileCollection with name, geo_location, and acres.
    """
    if not name or not geo_location or acres is None:
        print("❗ Name, geo_location, and acres are required.")
        return None

    try:
        profile_doc = {
            "name": name,
            "geo_location": geo_location,  
            "acres": acres,
        }
        result = profile_collection.insert_one(profile_doc)
        print(f"✅ Profile created with ID: {result.inserted_id}")
        return {"_id": str(result.inserted_id)}
    except PyMongoError as e:
        print(f"❌ Error inserting profile: {e}")
        return None


if __name__ == "__main__":
    if validate_db_connection():
        create_profile('Harshith', 340, 202220)
