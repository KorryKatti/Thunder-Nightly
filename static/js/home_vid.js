// Start video muted
const video = document.getElementById('myVideo');

// Function to unmute on user interaction
function unmuteVideo() {
    video.muted = false;
    video.play();  // Ensure the video continues playing after unmuting
    // Remove the event listener after the first interaction
    window.removeEventListener('click', unmuteVideo);
}

// Add an event listener to unmute on first user interaction
window.addEventListener('click', unmuteVideo);
