""" Provides utility functions and data structures (such as translation objects and markdown conversion) used across modules. """

from colorama import init, Style
from pathlib import Path
from typing import Any, Dict, List


init(autoreset=True)

class Data:
    """ Stores language and vocabulary data loaded from a JSON dictionary. """

    def __init__(self, data_json: Dict[str, List[Any]]):
        self.lang1 = data_json["languages"][0]
        self.lang2 = data_json["languages"][1]
        self.vocab = data_json["vocab"]

class Translation:
    """ Represents a translation attempt, including prompts, answers, number of attempts, and correctness. """
    
    def __init__(self, prompts: List[str], answers: List[str], attempts: int = 0, correct: bool = False):
        self.prompts = prompts
        self.answers = answers
        self.attempts = attempts
        self.correct = correct

def get_relative_vocab_path(file_path: Path) -> Path:
    """ Returns the relative path of the vocabulary file with respect to the 'vocab' directory. """

    return file_path.relative_to("vocab")

def get_progress_filename(stem: str) -> str:
    """ Returns the progress filename for a given stem. """

    return f"{stem}_progress.json"

def build_progress_path(file_path: Path) -> Path:
    """ Constructs the progress file path for a given vocabulary file path. """

    relative = get_relative_vocab_path(file_path)
    progress_filename = get_progress_filename(relative.stem)
    return Path("data") / relative.with_suffix('').with_name(progress_filename)

def convert_markdown_to_text(markdown: str) -> str:
    """ Converts markdown text with asterisks to styled text using colorama styles.
    Alternates between normal and bright styles for each section split by '*'. """
    
    parts = markdown.split("*")
    styled_parts = [(Style.NORMAL if i % 2 == 0 else Style.BRIGHT) + part for i, part in enumerate(parts)]
    return "".join(styled_parts) + Style.NORMAL