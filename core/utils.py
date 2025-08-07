""" Provides utility functions and data structures (such as translation objects and markdown conversion) used across modules. """

from colorama import init, Style
from pathlib import Path
from typing import Any, Dict, List


init(autoreset=True)

class VocabData:
    def __init__(self, data_json: Dict[str, List[Any]]):
        self.languages: List[str] = data_json["categories"]
        self.entries: List[VocabEntry] = [
            VocabEntry([
                WordGroup([
                    Word(word)
                    for word in group
                ], self.languages[i])
                for i, group in enumerate(entry)
            ])
            for entry in data_json["vocab"]
        ]

class Word:
    def __init__(self, text: str):
        self.text = text

class WordGroup:
    def __init__(self, words: List[Word], categorie: str):
        self.words = words
        self.categorie = categorie

class VocabEntry:
    def __init__(self, groups: List[WordGroup]):
        self.groups = groups

class Prompt(Word):
    pass

class PromptGroup(WordGroup):
    pass

class Answer(Word):
    pass

class AnswerGroup(WordGroup):
    pass

class AnswerGroups(VocabEntry):
    pass

class TranslationPair:
    def __init__(self, prompt: PromptGroup, answers: AnswerGroups, attempts: int = 0, correct: bool = False):
        self.prompt = prompt
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