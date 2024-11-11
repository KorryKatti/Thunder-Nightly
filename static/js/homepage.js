// Declare a variable to store the original width of the iframe
let originalIframeWidth = '90%';

// Function to handle actions based on the rightmost dropdown selection
function handleRightDropdownChange(value) {
    if (value === "chat") {
        toggleChatPopup(); // Show or hide the chat popup
    } else if (value === "maximize" || value === "minimize") {
        toggleMaximizeIframe(value); // Maximize or minimize the iframe based on the value
    }
}

// Toggle the maximized state for the iframe
function toggleMaximizeIframe(action) {
    const iframeContainer = document.querySelector('.iframe-container');
    const iframe = document.getElementById('content-frame');
    const sideImages = document.querySelectorAll('.side-image'); // Get both side images

    if (action === "maximize") {
        // If iframe is not already maximized
        if (!iframeContainer.classList.contains('maximized')) {
            // Save the current width as the original width (in case of minimize)
            originalIframeWidth = iframe.style.width || '90%'; // Default to 90% if not set
            iframe.style.width = '100%'; // Maximize the iframe to full width
            sideImages.forEach(image => image.style.display = 'none'); // Hide side images
            iframeContainer.classList.add('maximized'); // Add maximized class
        }
    } else if (action === "minimize") {
        // If iframe is maximized, revert to the original state
        if (iframeContainer.classList.contains('maximized')) {
            iframe.style.width = originalIframeWidth; // Restore iframe width
            sideImages.forEach(image => image.style.display = 'flex'); // Show side images
            iframeContainer.classList.remove('maximized'); // Remove maximized class
        }
    }
}

// Function to load iframe content based on URL or route
function loadIframe(url) {
    const iframe = document.getElementById('content-frame');
    if (url) {
        iframe.src = url; // Set the iframe src to the URL or relative path
    } else {
        iframe.src = ""; // Clear the iframe if no valid URL
    }
}

// Function to toggle the visibility of the chat popup
function toggleChatPopup() {
    const popup = document.getElementById('chat-popup');
    popup.style.display = popup.style.display === 'flex' ? 'none' : 'flex';
}

// Retrieve username from localStorage and update the HTML element if it exists
const usernameElement = document.getElementById("username-placeholder");
if (usernameElement) {
    const username = localStorage.getItem("username");
    usernameElement.textContent = username || "Guest";
}
