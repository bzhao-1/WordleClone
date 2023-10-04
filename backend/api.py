import csv
import pymongo
from pymongo import MongoClient
import random

'''Starts the MongoDB server, builds DB connection and creates collection to store list of words'''
mongoClient = MongoClient()
db = mongoClient['words']
collection = db['word']

'''Reads the CSV file and inserts each word into the collection'''
header = ['Number', 'Word']
csvFile = open('5_letter_words.csv', 'r')
reader = csv.DictReader(csvFile)
for row in reader:
    data = {
        'Number': row['Number'],
        'Word': row['Word']
    }
    collection.insert_one(data)

'''Randomly selects a word from the collection by generating a random number between 0 and the total number of words in the collection'''
totalCount = collection.count_documents({})
if totalCount > 0:
    random_index = random.randint(0, totalCount - 1)
    randomWord = collection.find().skip(random_index).limit(1)
    randomValue = next(randomWord, None)
    if randomValue:
        print("Random word:", randomValue['Word'])
else:
    print("The collection is empty.")

csvFile.close()




