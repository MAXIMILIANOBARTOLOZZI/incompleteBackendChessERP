# mongo_conn.py
from pymongo import MongoClient

def connect_mongo():
    client = MongoClient("mongodb://localhost:/")
    db = client[""]
    return db
