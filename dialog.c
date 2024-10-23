#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define FILENAME "localdata/userdata.json"
#define USERNAME_MAX_LENGTH 30
#define EMAIL_MAX_LENGTH 320
#define PFP_URL_MAX_LENGTH 2083
#define DESCRIPTION_MAX_LENGTH 500

void clearScreen() {
    printf("\033[2J\033[H");  // Clear the terminal screen
    fflush(stdout);
}

void getInput(char *prompt, char *buffer, int maxLength) {
    printf("%s", prompt);
    printf("> ");
    fflush(stdout);
    fgets(buffer, maxLength, stdin);
    buffer[strcspn(buffer, "\n")] = 0; // Remove the trailing newline character
}

void saveToFile(const char *username, const char *email, const char *pfp_url) {
    FILE *file = fopen(FILENAME, "w");
    if (file) {
        fprintf(file, "{\n");
        fprintf(file, "    \"username\": \"%s\",\n", username);
        fprintf(file, "    \"email\": \"%s\",\n", email);
        fprintf(file, "    \"profile_picture\": \"%s\"\n", pfp_url);
        fprintf(file, "}\n");
        fclose(file);
    } else {
        printf("Could not open file for writing.\n");
    }
}

int main() {
    char username[USERNAME_MAX_LENGTH + 1] = "";
    char email[EMAIL_MAX_LENGTH + 1] = "";
    char pfp_url[PFP_URL_MAX_LENGTH + 1] = "";
    
    // Get username
    clearScreen();
    getInput("Enter Username (3-30 characters): ", username, sizeof(username));
    saveToFile(username, email, pfp_url);  // Save after entering username

    // Get email
    clearScreen();
    getInput("Enter Email: ", email, sizeof(email));
    saveToFile(username, email, pfp_url);  // Save after entering email

    // Get profile picture URL
    clearScreen();
    getInput("Enter Profile Picture URL (or press Enter to skip): ", pfp_url, sizeof(pfp_url));
    saveToFile(username, email, pfp_url);  // Save after entering URL

    // Show saved data
    clearScreen();
    printf("Saved Information:\n");
    printf("Username: %s\n", username);
    printf("Email: %s\n", email);
    printf("Profile Picture URL: %s\n", pfp_url);
    return 0;
}
