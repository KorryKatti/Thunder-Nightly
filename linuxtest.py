import os

def main():
    # Get current directory
    current_dir = os.getcwd()

    # Save the current location to a file
    save_location(current_dir)

    # Create run.py and open.sh on the desktop
    create_files_on_desktop(current_dir)

def save_location(location):
    with open('current_location.txt', 'w') as f:
        f.write(location)

def create_files_on_desktop(location):
    desktop_path = os.path.expanduser("~/Desktop")
    run_py_path = os.path.join(desktop_path, "run.py")
    open_sh_path = os.path.join(desktop_path, "open.sh")

    with open(run_py_path, 'w') as run_file:
        run_file.write(f"import os\nos.chdir('{location}')\nos.system('./run.sh')")

    with open(open_sh_path, 'w') as open_file:
        open_file.write(f"#!/bin/bash\npython3 {run_py_path}")

    # Make open.sh executable
    os.chmod(open_sh_path, 0o755)

if __name__ == "__main__":
    main()
