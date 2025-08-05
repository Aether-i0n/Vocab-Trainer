import json
from pathlib import Path
from core.utils import Data

def load_vocab(file_path: str) -> Data:
    ext = Path(file_path).suffix
    if ext != '.json':
        raise ValueError("Only JSON vocab files are supported in this version.")
    
    with open(file_path, 'r', encoding='utf-8') as f:
        data_json = json.load(f)
        if "languages" not in data_json or "vocab" not in data_json:
            raise ValueError("JSON vocab must contain 'languages' and 'vocab' keys.")
        return Data(data_json)
