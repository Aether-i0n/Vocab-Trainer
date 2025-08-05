import random
import json
from pathlib import Path
from colorama import init, Fore, Style
from typing import List, Dict, Any
from core.loader import Data

class Translation:
    def __init__(self, prompts: List[str], answers: List[str], attempts: int = 0, correct: bool = False):
        self.prompts = prompts
        self.answers = answers
        self.attempts = attempts
        self.correct = correct

init(autoreset=True)

PROGRESS_DIR = Path("data")

def make_progress_path(file_path: Path):
    relative = file_path.relative_to("vocab")
    progress_path = Path("data") / relative.with_suffix('').with_name(relative.stem + "_progress.json")
    # progress_path.parent.mkdir(parents=True, exist_ok=True)
    return progress_path

def cleanup_empty_dirs(path, root=Path("data")):
    """Recursively delete empty parent folders up to the root."""
    path = path.parent
    while path != root and path.exists() and not any(path.iterdir()):
        path.rmdir()
        path = path.parent

def prepare_pairs(vocab_data: Data, mode: str) -> List[tuple]:
    vocab = vocab_data.vocab
    if mode == "reverse":
        return [(b, a) for a, b in vocab]
    elif mode == "random":
        return [(a, b) if random.random() < 0.5 else (b, a) for a, b in vocab]
    else:
        return [(a, b) for a, b in vocab]

def save_progress(failed_data: List[Translation], file_path: Path) -> None:
    progress_file = make_progress_path(file_path)
    progress_file.parent.mkdir(parents=True, exist_ok=True)
    with progress_file.open("w", encoding="utf-8") as f:
        json.dump([{"prompts": translation.prompts, "answers": translation.answers, "attempts": translation.attempts, "correct": translation.correct} for translation in failed_data], f, ensure_ascii=False, indent=2)

def load_progress(file_path: Path) -> List[Translation]:
    progress_file = make_progress_path(file_path)
    if progress_file.exists():
        with progress_file.open("r", encoding="utf-8") as f:
            return [Translation(data_translation["prompts"], data_translation["answers"], data_translation["attempts"], data_translation["correct"]) for data_translation in json.load(f)]
    return []

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

def markdown_to_text(markdown: str):
    parts = markdown.split("*")
    return "".join([[Style.NORMAL, Style.BRIGHT][i % 2] + part for i, part in enumerate(parts)]) + Style.NORMAL

def run_quiz(translations: List[Translation], file_path: Path) -> None:

    remaining = translations

    round_num = 1
    while remaining:

        random.shuffle(remaining)
        
        number_words_remaining = sum([1 for translation in remaining if not translation.correct])

        if not number_words_remaining:
            break

        print(f"\n--- {Fore.YELLOW}Round {round_num}{Style.RESET_ALL}: {number_words_remaining} word(s) to review ---\n")
        next_round: List[Translation] = []

        for translation in remaining:            
            if not translation.correct:
                prompts = translation.prompts
                prompt = random.choice(prompts)
                answers = translation.answers
                print(f"{Fore.CYAN}{markdown_to_text(prompt)}{Style.RESET_ALL} ➜ ", end="")
                user_input = input().strip()

                if user_input.lower() in ["".join(answer.lower().split("*")) for answer in answers]:
                    print(f"{Fore.GREEN}✅ Correct!{Style.RESET_ALL}\n")
                    translation.correct = True
                else:
                    print(f"{Fore.RED}❌ Incorrect. Correct answer(s): {markdown_to_text(', '.join(answers))}{Style.RESET_ALL}\n")
                    translation.prompts = [prompt]
                
                translation.attempts += 1
            
            next_round.append(translation)

        save_progress(next_round, file_path)
        remaining = next_round
        round_num += 1

    print(f"{Fore.GREEN}🎉 All words answered correctly!{Style.RESET_ALL}\n")

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
