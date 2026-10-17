from pymongo import MongoClient


MONGO_URL = "mongodb://localhost:27017"

client = MongoClient(MONGO_URL)

database = client["employee_db"]

employees_collection = database["employees"]