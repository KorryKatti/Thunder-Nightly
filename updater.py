import subprocess
import sys

def install_requirements():
    # Install requirements
    subprocess.run([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])

def main():
    # Install requirements
    install_requirements()

    # Display "Done" message
    print("Done")

    # Launch index.py
    subprocess.run(["python", "main.py"])

if __name__ == "__main__":
    main()
