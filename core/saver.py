from json import dump
from pathlib import Path
from typing import List

from core.utils import make_progress_path, Translation


def save_progress(failed_data: List[Translation], file_path: Path) -> None:
    progress_file = make_progress_path(file_path)
    progress_file.parent.mkdir(parents=True, exist_ok=True)
    with progress_file.open("w", encoding="utf-8") as f:
        dump([{"prompts": translation.prompts, "answers": translation.answers, "attempts": translation.attempts, "correct": translation.correct} for translation in failed_data], f, ensure_ascii=False, indent=2)
