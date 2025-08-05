from pathlib import Path
from typing import List
from colorama import Fore, Style
from core.utils import Translation, markdown_to_text, make_progress_path

def cleanup_empty_dirs(path: Path, root=Path("data")):
    """Recursively delete empty parent folders up to the root."""
    path = path.parent
    while path != root and path.exists() and not any(path.iterdir()):
        path.rmdir()
        path = path.parent

def review_mistakes(failed_data: List[Translation]) -> None:
    print(f"\n{Fore.YELLOW}Reviewing your mistakes:{Style.RESET_ALL}")
    for translation in failed_data:
        print(f"❌ {Fore.CYAN}{markdown_to_text(', '.join(translation.prompts))} ➜ {markdown_to_text(', '.join(translation.answers))}{Style.RESET_ALL} | Attempts: {translation.attempts}")
    print()

    retry = input("Would you like to retry these manually? (y/n): ").strip().lower()
    if retry == "y":
        for translation in failed_data:
            user_input = input(f"{', '.join(translation.prompts)} ➜ ").strip()
            if user_input.lower() in ["".join(answer.lower().split("*")) for answer in translation.answers]:
                print(f"{Fore.GREEN}✅ Correct!{Style.RESET_ALL}\n")
            else:
                print(f"{Fore.RED}❌ Still incorrect. The answer(s) are: {', '.join(translation.answers)}{Style.RESET_ALL}\n")

def run_results(remaining: List[Translation], file_path: Path):
    failed_data: List[Translation] = []
    for translation in remaining:
        if translation.attempts > 2:
            failed_data.append(translation)
    if failed_data:
        print("Some words had multiple wrong attempts before being solved.")
        if input("Do you want to review your mistakes? (y/n): ").strip().lower() == "y":
            review_mistakes(failed_data)
    
    progress_file = make_progress_path(file_path)
    progress_file.unlink(missing_ok=True)
    cleanup_empty_dirs(progress_file)
    print(f"{Fore.GREEN}Progress cleared!{Style.RESET_ALL}")