""" Runs the vocabulary quiz logic, manages quiz rounds, and tracks correctness and attempts for each translation. """

from colorama import Fore, Style
from pathlib import Path
from random import choice, shuffle
from typing import List

from core.saver import save_failed_translations
from core.utils import convert_markdown_to_text, Translation


PROGRESS_DIR = Path("data")

def run_vocabulary_quiz(translations: List[Translation], file_path: Path) -> None:
    """ Runs the vocabulary quiz until all translations are answered correctly.
    Displays progress after each round and saves progress to file. """

    round_number = 1

    while has_incorrect_answers(translations):
        words_left = count_incorrect(translations)
        display_round_header(round_number, words_left)
        translations = conduct_quiz_round(translations)
        save_failed_translations(translations, file_path)
        round_number += 1
    
    display_completion_message()

def has_incorrect_answers(translations: List[Translation]) -> bool:
    """ Returns True if there are translations not answered correctly. """
    
    return any(not t.correct for t in translations)

def count_incorrect(translations: List[Translation]) -> int:
    """ Counts the number of translations not answered correctly. """
    
    return sum(1 for t in translations if not t.correct)

def display_round_header(round_number: int, words_left: int) -> None:
    """ Displays the header for the current quiz round. """
    
    print(f"\n--- {Fore.YELLOW}Round {round_number}{Style.RESET_ALL}: {words_left} word(s) to review ---\n")

def conduct_quiz_round(translations: List[Translation]) -> List[Translation]:
    """ Conducts a single round of the quiz, asking questions for each translation.
    Returns the updated list of translations. """
    
    shuffle(translations)
    for translation in translations:
        ask_translation_question(translation)
    return translations

def ask_translation_question(translation: Translation) -> None:
    """ Asks the user a question for the given translation.
    Updates the translation's correctness and attempts. """
    
    if translation.correct:
        return
    
    prompt = select_prompt(translation)
    print(f"{Fore.CYAN}{convert_markdown_to_text(prompt)}{Style.RESET_ALL} ➜ ", end="")
    user_input = input().strip()

    if is_correct_answer(user_input, translation.answers):
        display_correct_message()
        translation.correct = True
    else:
        display_incorrect_message(translation.answers)
        translation.prompts = [prompt]
    
    translation.attempts += 1

def select_prompt(translation: Translation) -> str:
    """ Selects a prompt from the translation's prompts. """
    
    return choice(translation.prompts)

def is_correct_answer(user_input: str, answers: List[str]) -> bool:
    """ Checks if the user's input matches any of the correct answers.
    Ignores case and asterisks. """
    
    normalized_input = user_input.lower()
    normalized_answers = ["".join(ans.lower().split("*")) for ans in answers]
    return normalized_input in normalized_answers

def display_correct_message() -> None:
    """ Displays a message for a correct answer. """
    
    print(f"{Fore.GREEN}✅ Correct!{Style.RESET_ALL}\n")

def display_incorrect_message(answers: List[str]) -> None:
    """ Displays a message for an incorrect answer, showing the correct answers. """
    
    correct_text = convert_markdown_to_text(', '.join(answers))
    print(f"{Fore.RED}❌ Incorrect. Correct answer(s): {correct_text}{Style.RESET_ALL}\n")

def display_completion_message() -> None:
    """ Displays a message when all words are answered correctly. """
    
    print(f"{Fore.GREEN}🎉 All words answered correctly!{Style.RESET_ALL}\n")