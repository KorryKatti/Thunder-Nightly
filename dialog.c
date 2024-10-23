#include <stdio.h>
#include <string.h>

void main() {
    char username[30];
    char password[50];
    char email[320];
    char pfp_url[2083];
    char description[500];

  
    const char *filename = "localdata/userdata.json";  

   
    FILE *file = fopen(filename, "r");  
    if (file) {
        printf("Yes, '%s' exists in the 'localdata' folder.\n", filename);
        fclose(file);  
    } else {
        printf("No, '%s' does not exist in the 'localdata' folder.\n", filename);
    }

    printf("Please enter your username: \n");
    scanf("%s", username);  

    printf("Please enter your password: \n");
    scanf("%s", password);  

   
    int valid_email;
    do {
        printf("Please enter your email: \n");
        scanf("%s", email);

        // Check for '@' using strchr
        valid_email = (strchr(email, '@') != NULL);  

        if (!valid_email) {
            printf("Invalid Email! Please re-enter.\n");
        }
    } while (!valid_email); 

    printf("Please enter your profile picture URL: \n");
    scanf("%s", pfp_url);  

    getchar(); 

    printf("Please enter your description (can include spaces): \n");
    scanf(" %[^\n]", description);  
    
    printf("\nUsername: %s\n", username);
    printf("Password: %s\n", password);
    printf("Email: %s\n", email);
    printf("Profile Picture URL: %s\n", pfp_url);
    printf("Description: %s\n", description);
}
