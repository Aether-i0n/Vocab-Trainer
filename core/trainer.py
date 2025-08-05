import random
import json
from pathlib import Path
from colorama import Fore, Style
from typing import List
from core.utils import Data, Translation, make_progress_path, markdown_to_text

PROGRESS_DIR = Path("data")

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

def run_quiz(remaining: List[Translation], file_path: Path) -> None:
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

    
