# CS347-Final

Final Project for CS347

# Wordle

## Abstract

This is our version of Wordle, it is based off the original Wordle game. 


### Contributers

| Name           | Email                 |
| -------------- | --------------------- |
| Ben Zhao       | benzhao90@gmail.com   |
| Khizar Qureshi | qureshik@carleton.edu |
| Duy Nguyen     | nguyend2@carleton.edu |
| Ntense Obono   | obonon@carleton.edu   |
| Bem Abebayehu  | abebayehub@carleton.edu |



## Contents

- [Description](#description)
- [Folders Organization](#folders)
- [Instructions](#instructions)
- [Credits](#credits)

## Description

Our version of Wordle allows the user to guess a 5 letter word up to a maximum of 5 times. If a letter does not appear in the word, the box will turn red. If a letter appears in the word but is guessed in the wrong spot, the box will turn yellow. If a letter guessed is in the word and is guessed in the correct box, the box will turn green. Both words found in the Oxford English Dictionary and words that are not in the dictionary are valid guesses.  
What our game does not do:
We do not provide a keyboard showing which letters have already been guessed. This adds an extra layer of challenge to the game.
Have fun guessing!

## Instructions

Step 1: You need to install Docker and start Docker

Step 2: cd to the main folder

Step 3:

```bash
docker-compose up --build
```

Step 4:
Access the website  using 
```bash
http://localhost:8080/
```

Step 5:
Enter a username and hit start game. If your username does not exist, a new user will be created in our mongo database.

Step 6:
At any point during a game, you can see user stats by clicking on see win percentage 

## Folders
Our frontend html, css, and js files can be found in our game folder under templates and static directories. Our api and cli can be found within the main game directory. 
Additionally our dockerfile exists in this directory as well.
Our static frontend lives within its own directory and is a version of wordle that is not connected to our backend. 


## Credits
We would like to thank Prof. Matt Lepinski for all of the patience and help given to us throughout this term. He has been instrumental in guiding us in completing our project. 
We would also like to thank Ezra Barber for contributing a link to a page that shows the win percentage. He added the static html page for us and we filled in the specific features of the user profile that we wanted. 