""" Displays the main menu and manages user choices for starting, resuming, or configuring a session. """

from pathlib import Path
from shutil import rmtree
from typing import List


def main_menu():
    """ Displays the main menu for the Vocab Trainer application.
    Shows saved progress and prompts the user to start a quiz or clear progress. """
    
    print("📘 Welcome to Vocab Trainer")
    progress_files = find_progress_files()
    display_progress_summary(progress_files)

    if progress_files:
        display_menu_options()
        handle_menu_choice()

def find_progress_files() -> List[Path]:
    """ Searches for all saved progress files in the 'data' directory.
    Returns a list of Path objects for each progress file found. """
    
    return list(Path("data").rglob("*_progress.json"))

def display_progress_summary(progress_files: List[Path]):
    """ Prints a summary of all vocab sets with saved progress.
    If none are found, notifies the user. """
    
    if not progress_files:
        print("📂 No saved progress found.\n")
        return

    print(f"📦 {len(progress_files)} vocab set(s) in progress:")
    for file in progress_files:
        print(f"  • {get_vocab_set_name(file)}")
    print()

def get_vocab_set_name(progress_file: Path) -> str:
    """ Extracts and formats the vocab set name from a progress file path.
    Returns a readable string representing the vocab set. """
    
    rel_path = progress_file.relative_to("data").with_suffix("").as_posix()
    return rel_path.replace("_progress", "")

def display_menu_options():
    """ Displays the available menu options to the user. """
    
    print("1. Start quiz")
    print("2. Clear all saved progress")

def handle_menu_choice():
    """ Handles the user's menu selection and triggers the appropriate action. """
    
    choice = input("Choose an option (1/2): ").strip()
    if choice == "2":
        confirm_and_clear_progress()

def confirm_and_clear_progress():
    """ Asks the user for confirmation before deleting all saved progress.
    Deletes the 'data' directory if confirmed. """

    confirm = input("⚠️ Are you sure you want to delete ALL saved progress? (yes/no): ").strip().lower()
    if confirm == 'yes':
        delete_progress_data()
    else:
        print("❌ Cancelled.\n")

def delete_progress_data():
    """ Deletes the 'data' directory containing all saved progress files.
    Notifies the user of the result. """

    if Path("data").exists():
        rmtree("data")
        print("✅ All progress cleared.\n")
    else:
        print("ℹ️ No saved progress to delete.\n")
