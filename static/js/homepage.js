// Retrieve username from localStorage
const username = localStorage.getItem("username");

// Update the HTML element if username exists
if (username) {
    document.getElementById("username-placeholder").textContent = username;
} else {
    document.getElementById("username-placeholder").textContent = "Guest";
}
