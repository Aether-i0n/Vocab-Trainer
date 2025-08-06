from colorama import init, Style
from pathlib import Path
from typing import Any, Dict, List


init(autoreset=True)

class Data:
    def __init__(self, data_json: Dict[str, List[Any]]):
        languages: List[str] = data_json["languages"]
        vocab: List[List[str]] = data_json["vocab"]

        self.lang1 = languages[0]
        self.lang2 = languages[1]
        self.vocab = vocab

class Translation:
    def __init__(self, prompts: List[str], answers: List[str], attempts: int = 0, correct: bool = False):
        self.prompts = prompts
        self.answers = answers
        self.attempts = attempts
        self.correct = correct

def make_progress_path(file_path: Path):
    relative = file_path.relative_to("vocab")
    progress_path = Path("data") / relative.with_suffix('').with_name(relative.stem + "_progress.json")
    # progress_path.parent.mkdir(parents=True, exist_ok=True)
    return progress_path

def markdown_to_text(markdown: str):
    parts = markdown.split("*")
    return "".join([[Style.NORMAL, Style.BRIGHT][i % 2] + part for i, part in enumerate(parts)]) + Style.NORMAL