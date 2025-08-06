from json import load
from pathlib import Path
from typing import List

from core.utils import Data, make_progress_path, Translation


def load_progress(file_path: Path) -> List[Translation]:
    progress_file = make_progress_path(file_path)
    if progress_file.exists():
        with progress_file.open("r", encoding="utf-8") as f:
            return [Translation(data_translation["prompts"], data_translation["answers"], data_translation["attempts"], data_translation["correct"]) for data_translation in load(f)]
    return []

def load_vocab(file_path: str) -> Data:
    ext = Path(file_path).suffix
    if ext != '.json':
        raise ValueError("Only JSON vocab files are supported in this version.")
    
    with open(file_path, 'r', encoding='utf-8') as f:
        data_json = load(f)
        if "languages" not in data_json or "vocab" not in data_json:
            raise ValueError("JSON vocab must contain 'languages' and 'vocab' keys.")
        return Data(data_json)

def load_previous_progress(selected_file: Path):
    progress_file = make_progress_path(selected_file)
    if progress_file.exists():
        choice = input("Resume previous session? (y/n): ").strip().lower()
        return choice == "y"
    return False