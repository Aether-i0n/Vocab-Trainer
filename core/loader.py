import json
from pathlib import Path
from typing import List, Dict, Any

class Data:
    def __init__(self, data_json: Dict[str, List[Any]]):
        languages: List[str] = data_json["languages"]
        vocab: List[List[str]] = data_json["vocab"]

        self.lang1 = languages[0]
        self.lang2 = languages[1]
        self.vocab = vocab

def load_vocab(file_path: str) -> Data:
    ext = Path(file_path).suffix
    if ext != '.json':
        raise ValueError("Only JSON vocab files are supported in this version.")
    
    with open(file_path, 'r', encoding='utf-8') as f:
        data_json = json.load(f)
        if "languages" not in data_json or "vocab" not in data_json:
            raise ValueError("JSON vocab must contain 'languages' and 'vocab' keys.")
        return Data(data_json)
