""" Saves user progress and failed translations to files for future review or session resumption. """

from json import dump
from pathlib import Path
from typing import List

from core.utils import build_progress_path, Translation


def serialize_translation(translation: Translation) -> dict:
    """ Converts a Translation object into a serializable dictionary. """
    
    return {
        "prompts": translation.prompts,
        "answers": translation.answers,
        "attempts": translation.attempts,
        "correct": translation.correct
    }

def ensure_directory_exists(path: Path) -> None:
    """ Ensures that the parent directory of the given path exists. """
    
    path.parent.mkdir(parents=True, exist_ok=True)

def write_json_to_file(data: List[dict], file_path: Path) -> None:
    """ Writes a list of dictionaries to a file in JSON format. """
    
    with file_path.open("w", encoding="utf-8") as f:
        dump(data, f, ensure_ascii=False, indent=2)

def save_failed_translations(failed_translations: List[Translation], original_file_path: Path) -> None:
    """ Saves the progress of failed translations to a JSON file.
    Each Translation object is serialized and written to a progress file
    determined by the original file path. """
    
    progress_file = build_progress_path(original_file_path)
    ensure_directory_exists(progress_file)
    serialized_data = [serialize_translation(t) for t in failed_translations]
    write_json_to_file(serialized_data, progress_file)
