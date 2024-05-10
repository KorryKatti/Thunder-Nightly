import os
import winshell
from pathlib import Path

def main():
    # Get current directory
    current_dir = os.getcwd()

    # Save the current location to a file
    save_location(current_dir)

    # Create run.py and open.bat on the desktop
    create_files_on_desktop(current_dir)

    # Create desktop shortcut
    create_desktop_shortcut()

def save_location(location):
    with open('current_location.txt', 'w') as f:
        f.write(location)

def create_files_on_desktop(location):
    desktop_path = Path(winshell.desktop())
    run_py_path = desktop_path / "run.py"
    open_bat_path = desktop_path / "open.bat"

    with open(run_py_path, 'w') as run_file:
        run_file.write(f"import os\nos.chdir(r'{location}')\nos.system('run.bat')")

    with open(open_bat_path, 'w') as open_file:
        open_file.write(f"@echo off\npython {run_py_path}")

def create_desktop_shortcut():
    desktop_path = Path(winshell.desktop())
    shortcut_path = desktop_path / "Thunder.lnk"
    target_path = Path(__file__).resolve()
    icon_path = "media\\Icon.ico" 

    winshell.CreateShortcut(
        Path(shortcut_path),
        Target=target_path,
        Icon=(icon_path, 0),
        Description="Thunder Shortcut"
    )

if __name__ == "__main__":
    main()
