from colorama import Fore, Style
from pathlib import Path
from random import choice, shuffle
from typing import List

from core.saver import save_progress
from core.utils import markdown_to_text, Translation


PROGRESS_DIR = Path("data")

def run_quiz(remaining: List[Translation], file_path: Path) -> None:
    round_num = 1
    while remaining:

        shuffle(remaining)
        
        number_words_remaining = sum([1 for translation in remaining if not translation.correct])

        if not number_words_remaining:
            break

        print(f"\n--- {Fore.YELLOW}Round {round_num}{Style.RESET_ALL}: {number_words_remaining} word(s) to review ---\n")
        next_round: List[Translation] = []

        for translation in remaining:            
            if not translation.correct:
                prompts = translation.prompts
                prompt = choice(prompts)
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
