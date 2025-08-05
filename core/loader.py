import json
from pathlib import Path
from core.utils import Data, Translation, make_progress_path
from typing import List

def load_vocab(file_path: str) -> Data:
    ext = Path(file_path).suffix
    if ext != '.json':
        raise ValueError("Only JSON vocab files are supported in this version.")
    
    with open(file_path, 'r', encoding='utf-8') as f:
        data_json = json.load(f)
        if "languages" not in data_json or "vocab" not in data_json:
            raise ValueError("JSON vocab must contain 'languages' and 'vocab' keys.")
        return Data(data_json)

def load_progress(file_path: Path) -> List[Translation]:
    progress_file = make_progress_path(file_path)
    if progress_file.exists():
        with progress_file.open("r", encoding="utf-8") as f:
            return [Translation(data_translation["prompts"], data_translation["answers"], data_translation["attempts"], data_translation["correct"]) for data_translation in json.load(f)]
    return []
