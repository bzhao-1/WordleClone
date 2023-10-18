import csv
import pymongo
from pymongo import MongoClient
import random
from flask import Flask, request, jsonify

app = Flask(__name__)


'''Starts the MongoDB server, builds DB connection and creates collection to store list of words'''
mongoClient = MongoClient()
db = mongoClient['words']
collection = db['word']

'''Reads the CSV file and inserts each word into the collection'''
header = ['Number', 'Word']
csvFile = open('wordle.csv', 'r')
reader = csv.DictReader(csvFile)
for row in reader:
    data = {
        'Number': row['Number'],
        'Word': row['Word']
    }
    collection.insert_one(data)


'''Starts a new game bandomly selects a word from the collection by generating a random number between 0 and the total number of words in the collection'''
def start_new_game():
    global word_to_guess, attempts_left, guessed_words
    attempts_left = 6
    guessed_words = []
    totalCount = collection.count_documents({})
    if totalCount > 0:
        random_index = random.randint(0, totalCount - 1)
        randomWord = collection.find().skip(random_index).limit(1)
        randomValue = next(randomWord, None)
        if randomValue:
            word_to_guess = randomValue['Word']
            # print(word_to_guess)


'''Takes in a guessed word and checks if each letter matches the word to guess, if it does, then the represents as +, if word in guess represented as -, or " " if nothing, also needs to be implemented with frontend'''
def get_feedback(word, guess):
    feedback = ""
    for i in range(len(word)):
        if word[i] == guess[i]:
            feedback += '🟩'
        elif word[i] in guess:
            feedback += '🟨'
        else:
            feedback += '🟥'    
    return feedback


#Will change this later, just skeleton code for welcome screen for now, need to add with frontend
@app.route('/', methods=['GET'])
def welcome():
    return jsonify({"message": "Wordle"})


@app.route('/start', methods=['GET'])
def start_game(): 
    start_new_game()
    return jsonify({"message": "Game started. You have 6 attempts to guess the word."})

@app.route('/guess', methods=['POST'])
def guess_word():
    global attempts_left, guessed_words, word_to_guess
    if attempts_left <= 0:
        return jsonify({"message": "You've used all your attempts. Start a new game."}), 400

    guess = request.json.get('guess', '').lower()
    if len(guess) != 5 or not guess.isalpha():
        return jsonify({"message": "Invalid guess. Please provide a 5-letter word."}), 400

    if guess == word_to_guess:
        return jsonify({"message": "Congratulations! You guessed the word."})
    
    attempts_left -= 1
    guessed_words.append(guess)
    
    feedback = get_feedback(word_to_guess, guess)
    
    if attempts_left <= 0:
        return jsonify({"message": "Game over. The word was '{}'.".format(word_to_guess)})
    
    return jsonify({"attempts_left": attempts_left, "guessed_words": guessed_words, "feedback": feedback})

if __name__ == '__main__':
    app.run(debug=True)



csvFile.close()




