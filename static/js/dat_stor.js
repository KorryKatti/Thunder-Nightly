// Store the variables in localStorage
localStorage.setItem("username", username);
localStorage.setItem("email", email);
localStorage.setItem("pfp", pfp);

// Retrieve them if needed
console.log(localStorage.getItem("username"));
console.log(localStorage.getItem("email"));
console.log(localStorage.getItem("pfp"));
