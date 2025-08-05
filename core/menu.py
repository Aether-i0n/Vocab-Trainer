from core.loader import load_vocab
from core.trainer import load_progress, prepare_pairs
from pathlib import Path
import json
from collections import defaultdict
from typing import List, Dict, Any
import shutil
from core.utils import Translation, make_progress_path

VOCAB_DIR = Path("vocab")
PROGRESS_DIR = Path("data")

def count_words_in_file(file_path: Path):
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            data: Dict[str, List[Any]] = json.load(f)
        return len(data.get("vocab", []))
    except:
        return 0

def get_progress_info(file_path: Path):
    progress_file = make_progress_path(file_path)
    if not progress_file.exists():
        return None
    try:
        with open(progress_file, "r", encoding="utf-8") as f:
            data: List[Dict[str, List[Any]]] = json.load(f)
        return sum([1 for translation in data if not translation["correct"]])
    except:
        return None

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

def clear_all_progress():
    confirm = input("⚠️ Are you sure you want to delete ALL saved progress? (yes/no): ").strip().lower()
    if confirm == 'yes':
        if Path("data").exists():
            shutil.rmtree("data")
            print("✅ All progress cleared.\n")
        else:
            print("ℹ️ No saved progress to delete.\n")
    else:
        print("❌ Cancelled.\n")

def summarize_saved_progress(progress_files: List[Path]):
    if not progress_files:
        print("📂 No saved progress found.\n")
        return

    print(f"📦 {len(progress_files)} vocab set(s) in progress:")
    for file in progress_files:
        # Display relative path for readability
        rel_path = file.relative_to("data").with_suffix("").as_posix().replace("_progress", "")
        print(f"  • {rel_path}")
    print()

def run_menu():
    print("📘 Welcome to Vocab Trainer")
    progress_files = list(Path("data").rglob("*_progress.json"))
    summarize_saved_progress(progress_files)

    if progress_files:
        print("1. Start quiz")
        print("2. Clear all saved progress")
        choice = input("Choose an option (1/2): ").strip()

        if choice == "2":
            clear_all_progress()
            return

def select_file() -> Path:
    grouped = group_files_by_folder()
    if not grouped:
        print("⚠️ No vocab files found in the 'vocab/' directory.")
        return

    folder = choose_folder(grouped)
    selected_file = choose_file(grouped[folder])
    print(f"\n🔹 Selected: {selected_file.relative_to(VOCAB_DIR)}\n")

    return selected_file

def select_translations(selected_file: Path) -> List[Translation]:
    # Load previous progress
    use_saved = False
    progress_file = make_progress_path(selected_file)
    if progress_file.exists():
        choice = input("Resume previous session? (y/n): ").strip().lower()
        use_saved = choice == "y"

    if use_saved:
        return load_progress(selected_file)
    else:

        vocab_data = load_vocab(selected_file)

        mode = input(f"Mode? ({vocab_data.lang1} / {vocab_data.lang2} / random): ").strip().lower()
        if mode not in [vocab_data.lang1, vocab_data.lang2, 'random']:
            print(f"Invalid mode. Defaulting to {vocab_data.lang1}.")
            mode = vocab_data.lang1
        
        all_pairs = prepare_pairs(vocab_data, {vocab_data.lang1: "forward", vocab_data.lang2: "reverse", "random": "random"}[mode])
        return [Translation(p, a) for p, a in all_pairs]