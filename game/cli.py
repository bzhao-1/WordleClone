'''
cli.py

'''




from api import *


def main():
    print("Welcome to Wordle!")
    print("You have 6 attempts to guess the word.")
    gameVariables = start_new_game()
    word_to_guess = gameVariables[0]
    attempts_left = gameVariables[1]
    guessed_words = gameVariables[2]
    print(word_to_guess)
    while attempts_left > 0:
        print("You have {} attempts left.".format(attempts_left))
        print("Guessed words: {}".format(guessed_words))
        guess = input("Enter your guess: ").lower()
        if len(guess) != 5 or not guess.isalpha():
            print("Invalid guess. Please provide a 5-letter word.")
            continue
        if guess != word_to_guess:
            print("Incorrect guess. Try again.")
            attempts_left -= 1
        guessed_words.append(guess)
        feedback = get_feedback(word_to_guess, guess)
        print(feedback)
        if guess == word_to_guess:
            print("Congratulations! You guessed the word.")
            break


    
    


if __name__ == "__main__":
    main()