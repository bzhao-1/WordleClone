from collections import Counter
import csv
import pymongo
from pymongo import MongoClient
import random
#import requests
from flask import Flask, render_template, request, jsonify
from bson import ObjectId

app = Flask(__name__)


'''Starts the MongoDB server, builds DB connection and creates collection to store list of words'''
mongoClient = MongoClient("mongodb://db:27017/")
db = mongoClient['words']
userCollection = db['users']
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
    return word_to_guess, attempts_left, guessed_words


'''Takes in a guessed word and checks with Wordle logic to provide feedback to the user'''
def get_feedback(word, guess):
    feedback = ""
    wordCounter = Counter(word)
    guessCounter = Counter(guess)
    for i in range(len(word)):
        if word[i] == guess[i]:
            feedback += '🟩'
            wordCounter[word[i]] -= 1
            guessCounter[word[i]] -= 1
        elif guess[i] in wordCounter and wordCounter[guess[i]] > 0:
            feedback += '🟨'
            wordCounter[guess[i]] -= 1
        else:
            feedback += '🟥'    
    return feedback

@app.route('/getWins')
def winChange():
    return jsonify({'success': True})

@app.route('/', methods=['GET'])
def welcome():
    return render_template('index.html')


@app.route('/start/<username>', methods=['GET'])
def start_game(username): 
    user = userCollection.find_one({'username': username})
    
    if user:
        # The user already exists, update their total games played
        userCollection.find_one_and_update({'username': username}, {'$inc': {'total_games_played': 1}})
    else:
        # The user doesn't exist, so register them
        user_profile = {
            'username': username,
            'total_games_played': 1,
            'win_percentage': 0,
            'total_wins': 0,
            'total_losses': 0
        }
        userCollection.insert_one(user_profile)
    start_new_game()
    return jsonify({"message": "Game started. You have 6 attempts to guess the word."})

@app.route('/guess/<username>', methods=['POST'])
def guess_word(username):
    global attempts_left, guessed_words, word_to_guess
    print(word_to_guess)
    if attempts_left <= 0:
        return jsonify({"message": "You've used all your attempts. Start a new game."}), 400

    if request.content_type != 'application/json':
        return jsonify({"message": "Invalid request Content-Type. Please use 'application/json'."}), 400

    try:
        data = request.get_json()
        guess = data.get('guess', '').lower()
    except Exception as e:
        return jsonify({"message": "Invalid JSON data in the request."}), 400
   
    feedback = get_feedback(word_to_guess, guess)
    attempts_left -= 1
    if guess == word_to_guess: 
        userCollection.find_one_and_update({'username': username}, {'$inc': {'total_wins': 1}})
        userCollection.find_one_and_update({'username': username}, {'$set': {'win_percentage': (userCollection.find_one({'username': username})['total_wins'] / userCollection.find_one({'username': username})['total_games_played']) * 100}})
        feedback = '🟩' * 5
        return jsonify({"message": "Congratulations! You guessed the word.", "guessed_words": guessed_words, "feedback": feedback})
    
    
    guessed_words.append(guess)
    if attempts_left <= 0:
        userCollection.find_one_and_update({'username': username}, {'$inc': {'total_losses': 1}})
        return jsonify({"message": "Game over. The word was '{}'.".format(word_to_guess), "attempts_left": attempts_left, "guessed_words": guessed_words, "feedback": feedback })
    
    return jsonify({"attempts_left": attempts_left, "guessed_words": guessed_words, "feedback": feedback})


@app.route('/play/<username>', methods=['GET'])
def play(username):
    return render_template('index.html')



@app.route('/register/<username>', methods=['GET'])
def register(username):
    # username = request.form['username']
    usernameExists = userCollection.find_one({'username': username})
    if usernameExists:
        return jsonify({"message": "Username already exists pick a new username."})
    user_profile = {
        'username': username,
        'total_games_played': 0,
        'win_percentage': 0,
        'total_wins': 0,
        'total_losses': 0
    }
    userCollection.insert_one(user_profile)
    return jsonify({"message": "User created"})

@app.route('/wins/<username>')
def wins(username):
    return render_template('wins.html', username=username)

@app.route('/getWins')
def getWins():
    return jsonify({'success': True})
    
@app.route('/profile/<username>', methods=['GET'])
def view_profile(username):
    user_profile = userCollection.find_one({"username": username})
    if user_profile:
        user_profile['_id'] = str(user_profile['_id'])
        user_profile.pop('_id', None)
        return jsonify(user_profile)
    else:
        return "User not found", 404


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)



csvFile.close()




