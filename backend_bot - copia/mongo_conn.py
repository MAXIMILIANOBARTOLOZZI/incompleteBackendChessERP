# mongo_conn.py
from pymongo import MongoClient

def connect_mongo():
    client = MongoClient("mongodb://localhost:27017/")
    db = client["sio_global"]
    return db
