from collections import defaultdict
from json import load
from pathlib import Path
from typing import List, Dict, Any

from core.utils import make_progress_path


VOCAB_DIR = Path("vocab")

def select_file() -> Path:
    grouped = group_files_by_folder()
    if not grouped:
        print("⚠️ No vocab files found in the 'vocab/' directory.")
        return

    folder = choose_folder(grouped)
    selected_file = choose_file(grouped[folder])
    print(f"\n🔹 Selected: {selected_file.relative_to(VOCAB_DIR)}\n")

    return selected_file

def group_files_by_folder() -> Dict[str, List[Path]]:
    grouped = defaultdict(list)
    for file in VOCAB_DIR.rglob("*.json"):
        if file.is_file():
            relative = file.relative_to(VOCAB_DIR)
            folder = relative.parent  # could be empty
            grouped[str(folder)].append(file)
    return dict(grouped)

def choose_folder(grouped: Dict[str, List[Path]]):
    folders = sorted(grouped.keys())
    print("\n📁 Available Folders:")
    for i, folder in enumerate(folders):
        print(f"  [{i}] {folder}")

    while True:
        choice = input("\nChoose a folder by number: ").strip()
        if choice.isdigit() and 0 <= int(choice) < len(folders):
            return folders[int(choice)]
        else:
            print("❌ Invalid choice. Please enter a valid number.")

def choose_file(files: List[Path]):
    print("\n📚 Vocabulary Files:")
    for i, file in enumerate(files):
        word_count = count_words_in_file(file)
        progress_left = get_progress_info(file)
        info = f"🧠 {word_count} words"
        if progress_left is not None:
            info += f" | 💾 {progress_left} pending"
        print(f"  [{i}] {file.name} ({info})")

    while True:
        choice = input("\nChoose a vocab set by number: ").strip()
        if choice.isdigit() and 0 <= int(choice) < len(files):
            return files[int(choice)]
        else:
            print("❌ Invalid choice. Please enter a valid number.")

def count_words_in_file(file_path: Path):
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            data: Dict[str, List[Any]] = load(f)
        return len(data.get("vocab", []))
    except:
        return 0

def get_progress_info(file_path: Path):
    progress_file = make_progress_path(file_path)
    if not progress_file.exists():
        return None
    try:
        with open(progress_file, "r", encoding="utf-8") as f:
            data: List[Dict[str, List[Any]]] = load(f)
        return sum([1 for translation in data if not translation["correct"]])
    except:
        return None