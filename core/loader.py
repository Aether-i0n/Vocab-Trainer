""" Loads vocabulary translations and user progress from files, preparing data for the quiz. """

from json import load
from pathlib import Path
from typing import List

from core.utils import Data, build_progress_path, Translation


def get_progress_file(file_path: Path) -> Path:
    """ Returns the path to the progress file associated with the given file path. """
    
    return build_progress_path(file_path)

def file_exists(file_path: Path) -> bool:
    """ Checks if the given file path exists. """
    
    return file_path.exists()

def read_json_file(file_path: Path) -> list:
    """ Reads and returns the JSON content from the specified file path. """
    
    with file_path.open("r", encoding="utf-8") as f:
        return load(f)

def parse_translations(data: list) -> List[Translation]:
    """ Converts a list of translation dictionaries to a list of Translation objects. """
    
    return [
        Translation(
            item["prompts"],
            item["answers"],
            item["attempts"],
            item["correct"]
        )
        for item in data
    ]

def load_translations_progress(file_path: Path) -> List[Translation]:
    """ Loads the progress of translations from the associated progress file.
    Returns a list of Translation objects if the file exists, otherwise an empty list. """
    
    progress_file = get_progress_file(file_path)
    if file_exists(progress_file):
        data = read_json_file(progress_file)
        return parse_translations(data)
    return []

def validate_vocab_json(data_json: dict) -> None:
    """ Validates that the vocab JSON contains required keys."""
    
    if "languages" not in data_json or "vocab" not in data_json:
        raise ValueError("JSON vocab must contain 'languages' and 'vocab' keys.")

def load_vocab_data(file_path: str) -> Data:
    """ Loads vocabulary data from a JSON file and returns a Data object.
    Raises an error if the file extension is not .json or required keys are missing. """
    
    ext = Path(file_path).suffix
    if ext != '.json':
        raise ValueError("Only JSON vocab files are supported in this version.")
    with open(file_path, 'r', encoding='utf-8') as f:
        data_json = load(f)
        validate_vocab_json(data_json)
        return Data(data_json)

def should_resume_previous_session(selected_file: Path) -> bool:
    """ Checks if a previous progress file exists and prompts the user to resume the session.
    Returns True if the user chooses to resume, otherwise False. """
    
    progress_file = get_progress_file(selected_file)
    if file_exists(progress_file):
        choice = input("Resume previous session? (y/n): ").strip().lower()
        return choice == "y"
    return False