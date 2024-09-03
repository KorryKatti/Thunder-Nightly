
const quotes = [
    "The only limit to our realization of tomorrow is our doubts of today.",
    "Do not watch the clock. Do what it does. Keep going.",
    "The future belongs to those who believe in the beauty of their dreams.",
    "It does not matter how slowly you go as long as you do not stop.",
    "Success is not final, failure is not fatal: It is the courage to continue that counts."
];

function displayRandomQuote() {
    const randomIndex = Math.floor(Math.random() * quotes.length);
    const quoteElement = document.getElementById('quote');
    quoteElement.textContent = quotes[randomIndex];
}

// Display a random quote when the page loads
window.onload = displayRandomQuote;

