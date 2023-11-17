// document.addEventListener("DOMContentLoaded", function() {
const usernameForm = document.getElementById("username-form");
const usernameInput = document.getElementById("username");
const startGameButton = document.getElementById("start-game");
const gameGrid = document.getElementById("game");
const guessForm = document.getElementById("guess-form");
const signOutButton = document.getElementById("sign-out");

function startGame(username) {
    const url = `/start/${username}`;
    console.log("Calling /start:", url);
    fetch(url, {method: 'get'});
}

function getWins(username) {
    const url = `/getWins`;
    fetch(url, {method: 'get'})
    .then(response => response.json())
    .then(data => {
        if (data.success) {
        // Redirect to the other page
        window.location.href = `/wins/${usernameInput.value}`;
    } else {
        console.error('Failed to change the page.');
    }
    })
}
signOutButton.addEventListener("click", function () {
    location.reload();
});

startGameButton.addEventListener("click", function() {
    const username = usernameInput.value;
    usernameForm.style.display = "none";
    startGame(username);
    initializeGame(username);
    document.getElementById("sign-out").style.display = "block";
});

function initializeGame(username) {
    const state = {
        grid: Array(6).fill().map(() => Array(5).fill('')),
        currentRow: 0,
        currentCol: 0,
    };
    var winsButton = document.createElement("button");
    winsButton.textContent = "Click to see win percentage";
    winsButton.type = "button";
    winsButton.onclick = getWins;
    document.body.appendChild(winsButton);
    function drawGrid(container) {
        const grid = document.createElement('div');
        grid.className = 'grid';

        for (let i = 0; i < 6; i++) {
            for (let j = 0; j < 5; j++) {
                drawBox(grid, i, j);
            }
        }

        container.appendChild(grid);
    }

    function updateGrid() {
        for (let i = 0; i < state.grid.length; i++) {
            for (let j = 0; j < state.grid[i].length; j++) {
                const box = document.getElementById(`box${i}${j}`);
                box.textContent = state.grid[i][j];
            }
        }
    }

    function drawBox(container, row, col, letter = '') {
        const box = document.createElement('div');
        box.className = 'box';
        box.textContent = letter;
        box.id = `box${row}${col}`;

        container.appendChild(box);
        return box;
    }

    function registerKeyboardEvents() {
        document.body.onkeydown = (e) => {
            const key = e.key;
            if (key === 'Enter') {
                if (state.currentCol === 5) {
                    const guess = state.grid[state.currentRow].join('');
                    makeGuess(username, guess);
                    state.currentRow++;
                    state.currentCol = 0;
                }
            }
            if (key === 'Backspace') {
                removeLetter();
            }
            if (isLetter(key)) {
                addLetter(key);
            }

            updateGrid();
        };
    }

    function isLetter(key) {
        return key.length === 1 && key.match(/[a-z]/i);
    }

    function addLetter(letter) {
        if (state.currentCol === 5) return;
        state.grid[state.currentRow][state.currentCol] = letter;
        state.currentCol++;
    }

    function removeLetter() {
        if (state.currentCol === 0) return;
        state.grid[state.currentRow][state.currentCol - 1] = '';
        state.currentCol--;
    }

    function makeGuess(username, guess) {
        // Send the guess to the server and handle the response
        const url = `/guess/${username}`;
        fetch(url, {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({ guess }),
        })
        .then(response => response.json())
        .then(data => handleGuessResponse(data))
        .catch(error => console.error("An error occurred:", error));
    }

    function handleGuessResponse(data) {
        // Process the feedback received from the server
        if (data.message) {
            const message = document.getElementById("message");
            message.textContent = data.message;
        }

        if (data.feedback) {
            const feedback = document.getElementById("feedback");
            const feedbackText = data.feedback;
            feedback.innerHTML = '';

            let i = 0;
            for (const char of feedbackText) {
                const span = document.createElement('span');
                span.classList.add('feedback-char');
                span.textContent = char;

                let box = document.getElementById(`box${state.currentRow -1}${i}`);

                if (char === '🟩') {
                    span.classList.add('green');
                    box.style.backgroundColor = 'green';
                } else if (char === '🟨') {
                    span.classList.add('yellow');
                    box.style.backgroundColor = 'yellow';
                } else if (char === '🟥') {
                    span.classList.add('red');
                    box.style.backgroundColor = 'red';
                }
                feedback.appendChild(span);
                i = i + 1;
            }
        }
    }

    drawGrid(gameGrid);
    registerKeyboardEvents();
}
// });