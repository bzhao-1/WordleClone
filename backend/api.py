import pymongo
from pymongo import MongoClient

mongoClient = MongoClient()
db = mongoClient['words']
collection = db['word']






