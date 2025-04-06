import os
from pymongo import MongoClient
from dotenv import load_dotenv
from datetime import datetime
from bson import ObjectId
import gridfs
from pymongo.errors import PyMongoError
from typing import Dict, Any, Optional, Union

load_dotenv()
mongo_uri = os.environ.get('MONGO_URI')

client = MongoClient(mongo_uri)
db = client["NWHDB"]
login_collection = db["UserLogin"]
fs = gridfs.GridFS(db)
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
            user = login_collection.find_one({"username": username, "password": password})
            if user:
                print(f"✅ Login successful for user: {username}")
                return {"_id": str(user["_id"]), "username": user["username"]}
            else:
                print("❌ Invalid username or password.")
                return None
        except PyMongoError as e:
            print(f"❌ Error validating login: {e}")
            return None

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
        result = login_collection.insert_one(user_doc)
        print(f"✅ User created with ID: {result.inserted_id}")
        return {"_id": str(result.inserted_id)}
    except PyMongoError as e:
        print(f"❌ Error inserting user: {e}")
        return None


def create_profile(id: str, geo_location: Dict[str, Union[float, Any]], acres: Union[float, int]) -> Optional[Dict[str, Any]]:
    """
    Inserts a document into ProfileCollection with name, geo_location, and acres.
    """
    if not id or not geo_location or acres is None:
        print("❗ Name, geo_location, and acres are required.")
        return None

    try:
        profile_doc = {
            "id": id,
            "geo_location": geo_location,  
            "acres": acres,
        }
        result = profile_collection.insert_one(profile_doc)
        print(f"✅ Profile created with ID: {result.inserted_id}")
        return {"_id": str(result.inserted_id)}
    except PyMongoError as e:
        print(f"❌ Error inserting profile: {e}")
        return None

def upload_image(file_data, filename):
    try:
        file_id = fs.put(file_data, filename=filename)
        return file_id
    except Exception as e:
        print(f"Error uploading image: {e}")
        return None

def get_image(filename):
    try:
        file = fs.find_one({"filename": filename})
        if file:
            return file.read()
        return None
    except Exception as e:
        print(f"Error retrieving image: {e}")
        return None


def create_or_update_user_collection(user_id: str, descreption: str, response: str) -> Optional[Dict[str, Any]]:
    """
    Creates or updates a collection for the user based on user_id.
    If the collection already exists, it will append new documents.
    """
    if not user_id or not descreption or not response:
        print("❗ User ID, description, and response are required.")
        return None
    
    user_collection_name = f"user_{user_id}_collection"
    
    try:
        user_collection = db[user_collection_name]
        
        new_doc = {
            "desc": descreption,
            "response": response,
            "timestamp": datetime.now()  
        }
        
        result = user_collection.insert_one(new_doc)
        print(f"✅ Document inserted into {user_collection_name} with ID: {result.inserted_id}")
        
        return {"_id": str(result.inserted_id)}
    
    except PyMongoError as e:
        print(f"❌ Error inserting/updating collection for user {user_id}: {e}")
        return None


if __name__ == "__main__":
    if validate_db_connection():
        create_profile('Rohan', 340, 202220)
        
        create_or_update_user_collection('Rohan', "Rohan's first desc", "Rohan's first response")
        create_or_update_user_collection('Rohan', "Rohan's second desc", "Rohan's second response")