from pathlib import Path
from shutil import rmtree
from typing import List


VOCAB_DIR = Path("vocab")

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

def clear_all_progress():
    confirm = input("⚠️ Are you sure you want to delete ALL saved progress? (yes/no): ").strip().lower()
    if confirm == 'yes':
        if Path("data").exists():
            rmtree("data")
            print("✅ All progress cleared.\n")
        else:
            print("ℹ️ No saved progress to delete.\n")
    else:
        print("❌ Cancelled.\n")
