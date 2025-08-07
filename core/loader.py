""" Loads vocabulary translations and user progress from files, preparing data for the quiz. """

from json import load
from pathlib import Path
from typing import Any, Dict, List

from core.utils import VocabData, build_progress_path, TranslationPair, PromptGroup, Word, AnswerGroups, AnswerGroup


def get_progress_file(file_path: Path) -> Path:
    """ Returns the path to the progress file associated with the given file path. """
    
    return build_progress_path(file_path)

def file_exists(file_path: Path) -> bool:
    """ Checks if the given file path exists. """
    
    return file_path.exists()

def read_json_file(file_path: Path) -> List[Dict[str, Any]]:
    """ Reads and returns the JSON content from the specified file path. """
    
    with file_path.open("r", encoding="utf-8") as f:
        return load(f)

def parse_translations(data: List[Dict[str, Any]]) -> List[TranslationPair]:
    """ Converts a list of translation dictionaries to a list of TranslationPair objects. """
    
    return [
        TranslationPair(
            PromptGroup(
                [
                Word(text)
                for text in item["prompts"]["words"]
                ],
                item["prompts"]["categorie"]
            ),
            AnswerGroups(
                [
                AnswerGroup(
                    [
                    Word(text)
                    for text in answer["words"]
                    ],
                    answer["categorie"]
                )
                for answer in item["answers"]
                ]
            ),
            item["attempts"],
            item["correct"]
        )
        for item in data
    ]

def load_translations_progress(file_path: Path) -> List[TranslationPair]:
    """ Loads the progress of translations from the associated progress file.
    Returns a list of TranslationPair objects if the file exists, otherwise an empty list. """
    
    progress_file = get_progress_file(file_path)
    if file_exists(progress_file):
        data = read_json_file(progress_file)
        return parse_translations(data)
    return []

def validate_vocab_json(data_json: dict) -> None:
    """ Validates that the vocab JSON contains required keys."""
    
    if "categories" not in data_json or "vocab" not in data_json:
        raise ValueError("JSON vocab must contain 'categories' and 'vocab' keys.")

def load_vocab_data(file_path: str) -> VocabData:
    """ Loads vocabulary data from a JSON file and returns a VocabData object.
    Raises an error if the file extension is not .json or required keys are missing. """
    
    ext = Path(file_path).suffix
    if ext != '.json':
        raise ValueError("Only JSON vocab files are supported in this version.")
    with open(file_path, 'r', encoding='utf-8') as f:
        data_json = load(f)
        validate_vocab_json(data_json)
        return VocabData(data_json)

def should_resume_previous_session(file_path: Path) -> bool:
    """ Checks if a previous progress file exists and prompts the user to resume the session.
    Returns True if the user chooses to resume, otherwise False. """

    progress_file = get_progress_file(file_path)
    if file_exists(progress_file):
        print("Resume previous session? (y/n): ", end="")
        choice = input().strip().lower()
        return choice == "y"
    return False