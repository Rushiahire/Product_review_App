from pymongo import MongoClient


url = "127.0.0.1:27017"
client = MongoClient(url)

database_name = "mini_project"
database = client[database_name]


