""" Handles user interaction for selecting a vocabulary file to use in the session. """

from collections import defaultdict
from json import load
from pathlib import Path
from typing import List, Dict, Any

from core.utils import build_progress_path


VOCAB_DIR = Path("vocab")

def select_vocab_file() -> Path:
    """ Prompts the user to select a vocabulary file from available folders and files.
    Returns the selected file path, or None if no files are found. """
    
    grouped_files = get_grouped_vocab_files()
    if not grouped_files:
        display_no_files_found()
        return None

    folder = prompt_folder_selection(grouped_files)
    file = prompt_file_selection(grouped_files[folder])
    display_selected_file(file)
    return file

def get_grouped_vocab_files() -> Dict[str, List[Path]]:
    """ Returns a dictionary grouping all .json vocab files by their folder names. """
    
    files = find_vocab_files()
    return group_files_by_folder(files)

def find_vocab_files() -> List[Path]:
    """ Returns a list of all .json files in the VOCAB_DIR directory and subdirectories. """
    
    return [file for file in VOCAB_DIR.rglob("*.json") if file.is_file()]

def group_files_by_folder(files: List[Path]) -> Dict[str, List[Path]]:
    """ Groups a list of files by their parent folder names. """
    
    grouped = defaultdict(list)

    for file in files:
        folder = str(file.relative_to(VOCAB_DIR).parent)
        grouped[folder].append(file)
    
    return dict(grouped)

def display_no_files_found():
    """ Prints a message indicating no vocab files were found. """
    
    print("⚠️ No vocab files found in the 'vocab/' directory.")

def prompt_folder_selection(grouped: Dict[str, List[Path]]) -> str:
    """ Prompts the user to select a folder from the available grouped folders.
    Returns the selected folder name. """

    folders = sorted(grouped.keys())
    display_folders(folders)

    return get_valid_selection(folders, "\nChoose a folder by number: ")

def display_folders(folders: List[str]):
    """ Displays the available folders to the user. """

    print("\n📁 Available Folders:")

    for i, folder in enumerate(folders):
        print(f"  [{i}] {folder}")

def prompt_file_selection(files: List[Path]) -> Path:
    """ Prompts the user to select a vocabulary file from the list.
    Returns the selected file path. """

    display_files(files)
    return get_valid_selection(files, "\nChoose a vocab set by number: ")

def display_files(files: List[Path]):
    """ Displays the available vocabulary files with word count and progress info. """
    
    print("\n📚 Vocabulary Files:")

    for i, file in enumerate(files):
        word_count = get_word_count(file)
        pending_count = get_pending_progress_count(file)
        info = f"🧠 {word_count} words"

        if pending_count is not None:
            info += f" | 💾 {pending_count} pending"
        print(f"  [{i}] {file.name} ({info})")

def get_valid_selection(options: List[Any], prompt: str) -> Any:
    """ Prompts the user to select an option by number and returns the selected item. """

    while True:
        choice = input(prompt).strip()

        if choice.isdigit() and 0 <= int(choice) < len(options):
            return options[int(choice)]
        
        print("❌ Invalid choice. Please enter a valid number.")

def get_word_count(file_path: Path) -> int:
    """ Returns the number of words in the given vocabulary file. """

    try:
        with open(file_path, "r", encoding="utf-8") as f:
            data: Dict[str, List[Any]] = load(f)
        
        return len(data.get("vocab", []))
    
    except Exception:
        return 0

def get_pending_progress_count(file_path: Path) -> int:
    """ Returns the number of pending (not correct) translations in the progress file.
    Returns None if the progress file does not exist or cannot be read. """

    progress_file = build_progress_path(file_path)

    if not progress_file.exists():
        return None
    
    try:
        with open(progress_file, "r", encoding="utf-8") as f:
            data: List[Dict[str, Any]] = load(f)
        
        return sum(1 for translation in data if not translation.get("correct", False))
    
    except Exception:
        return None

def display_selected_file(file: Path):
    """ Prints the selected vocabulary file relative to VOCAB_DIR. """

    print(f"\n🔹 Selected: {file.relative_to(VOCAB_DIR)}\n")