import os
from pymongo import MongoClient
import gridfs
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# MongoDB connection

client = MongoClient(os.getenv('MONGO_URI'))
db = client["NWHDB"]  # This will get the default database
fs = gridfs.GridFS(db)  # Initialize GridFS

# Example function to upload a file
def upload_file(file_name, file_data):
    # Store the file in GridFS
    file_id = fs.put(file_data, filename=file_name)
    return file_id

# Example function to fetch a file by its filename
def fetch_file(file_name):
    # Find file by filename
    file = fs.find_one({"filename": file_name})
    if file:
        return file.read()  # Return the file data
    return None
