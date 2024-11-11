// Retrieve username from localStorage
const username = localStorage.getItem("username");

// Update the HTML element if username exists
if (username) {
    document.getElementById("username-placeholder").textContent = username;
} else {
    document.getElementById("username-placeholder").textContent = "Guest";
}

function loadIframe(url) {
    const iframe = document.getElementById('content-frame');
    if (url && url.startsWith("http")) {
        iframe.src = url;
    } else {
        iframe.src = ""; // Clear the iframe if no valid URL
    }
}
