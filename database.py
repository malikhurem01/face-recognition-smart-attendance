from pymongo import MongoClient
from pymongo.server_api import ServerApi
from config import MONGODB_URI, DATABASE_NAME, VENUES_COLLECTION

client = MongoClient(MONGODB_URI, server_api=ServerApi('1'))
db = client[DATABASE_NAME]
venues_collection = db[VENUES_COLLECTION]

def init_db():
    try:
        client.admin.command('ping')
        print("Pinged your deployment. You successfully connected to MongoDB!")
    except Exception as e:
        print("MongoDB connection error:", e)
