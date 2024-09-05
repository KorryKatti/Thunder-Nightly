
const quotes = [
    "This project is open source at github.com/korrykatti/Thunder",
    "You can contribute to Thunder at the nightly repository",
    " Initially the gui was fully designed in python using tkinter",
    "If you have any suggestions or questions, please let us know at github.com/korrykatti/Thunder",
    "Thank you for using Thunder",
    "If you liked the project, please consider giving it a star on github.com/korrykatti/Thunder",
    "If you have any feedback, please let us know at github.com/korrykatti/Thunder",
    "Thunder's website is at thunderenv.glitch.me",
    "We have our own imageboard at korrykatti.pythonanywhere.com"
];

function displayRandomQuote() {
    const randomIndex = Math.floor(Math.random() * quotes.length);
    const quoteElement = document.getElementById('quote');
    quoteElement.textContent = quotes[randomIndex];
}

// Display a random quote when the page loads
window.onload = displayRandomQuote;
