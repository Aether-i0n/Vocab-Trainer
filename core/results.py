""" Processes and displays quiz results, including statistics and summary of user performance. """

from colorama import Fore, Style
from pathlib import Path
from typing import List

from core.utils import build_progress_path, convert_markdown_to_text, Translation


def run_results(remaining_translations: List[Translation], file_path: Path):
    """ Handles the end-of-session results, including identifying failed translations,
    offering review and retry options, and clearing progress files. """
    
    failed_translations = get_failed_translations(remaining_translations)
    if failed_translations:
        print("Some words had multiple wrong attempts before being solved.")
        if prompt_yes_no("Do you want to review your mistakes?"):
            review_failed_translations(failed_translations)
    clear_progress(file_path)

def get_failed_translations(translations: List[Translation]) -> List[Translation]:
    """ Returns a list of translations that had more than two failed attempts. """
    
    return [t for t in translations if t.attempts > 2]

def prompt_yes_no(message: str) -> bool:
    """ Prompts the user with a yes/no question and returns True for 'y', False otherwise. """
    
    return input(f"{message} (y/n): ").strip().lower() == "y"

def review_failed_translations(failed_translations: List[Translation]) -> None:
    """ Displays failed translations and offers the user a chance to retry them manually. """
    
    print(f"\n{Fore.YELLOW}Reviewing your mistakes:{Style.RESET_ALL}")
    for translation in failed_translations:
        show_failed_translation(translation)
    
    print()
    if prompt_yes_no("Would you like to retry these manually?"):
        retry_failed_translations(failed_translations)

def show_failed_translation(translation: Translation) -> None:
    """ Prints a single failed translation with its prompts, answers, and attempt count. """
    
    prompts = convert_markdown_to_text(', '.join(translation.prompts))
    answers = convert_markdown_to_text(', '.join(translation.answers))
    print(f"❌ {Fore.CYAN}{prompts} ➜ {answers}{Style.RESET_ALL} | Attempts: {translation.attempts}")

def retry_failed_translations(failed_translations: List[Translation]) -> None:
    """ Allows the user to manually retry each failed translation and provides feedback. """
    
    for translation in failed_translations:
        user_input = input(f"{', '.join(translation.prompts)} ➜ ").strip()
        if is_correct_answer(user_input, translation.answers):
            print(f"{Fore.GREEN}✅ Correct!{Style.RESET_ALL}\n")
        else:
            print(f"{Fore.RED}❌ Still incorrect. The answer(s) are: {', '.join(translation.answers)}{Style.RESET_ALL}\n")

def is_correct_answer(user_input: str, answers: List[str]) -> bool:
    """ Checks if the user's input matches any of the correct answers (case-insensitive, ignoring asterisks). """
    
    normalized_answers = ["".join(answer.lower().split("*")) for answer in answers]
    return user_input.lower() in normalized_answers

def clear_progress(file_path: Path) -> None:
    """ Removes the progress file and cleans up any empty parent directories up to the data root. """
    
    progress_file = build_progress_path(file_path)
    progress_file.unlink(missing_ok=True)
    remove_empty_parent_dirs(progress_file)
    print(f"{Fore.GREEN}Progress cleared!{Style.RESET_ALL}")

def remove_empty_parent_dirs(path: Path, root=Path("data")) -> None:
    """ Recursively deletes empty parent directories up to the specified root directory. """
    
    current = path.parent
    while current != root and current.exists() and not any(current.iterdir()):
        current.rmdir()
        current = current.parent