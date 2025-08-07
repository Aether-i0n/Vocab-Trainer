""" Runs the vocabulary quiz logic, manages quiz rounds, and tracks correctness and attempts for each translation. """

from colorama import Fore, Style
from pathlib import Path
from random import choice, shuffle
from typing import List

from core.saver import save_failed_translations
from core.utils import convert_markdown_to_text, PromptGroup, TranslationPair, WordGroup


PROGRESS_DIR = Path("data")

def run_vocabulary_quiz(pairs: List[TranslationPair], file_path: Path) -> None:
    """ Runs the vocabulary quiz until all entries are answered correctly.
    Displays progress after each round and saves progress to file. """

    round_number = 1

    while has_incorrect_answers(pairs):
        entries_left = count_incorrect(pairs)
        display_round_header(round_number, entries_left)
        pairs = conduct_quiz_round(pairs)
        save_failed_translations(pairs, file_path)
        round_number += 1

    display_completion_message()

def has_incorrect_answers(pairs: List[TranslationPair]) -> bool:
    """ Returns True if there are entries not answered correctly. """

    return any(not pair.correct for pair in pairs)

def count_incorrect(pairs: List[TranslationPair]) -> int:
    """ Counts the number of entries not answered correctly. """

    return sum(1 for pair in pairs if not pair.correct)

def display_round_header(round_number: int, entries_left: int) -> None:
    """ Displays the header for the current quiz round. """

    print(f"\n--- {Fore.YELLOW}Round {round_number}{Style.RESET_ALL}: {entries_left} entry(ies) to review ---\n")

def conduct_quiz_round(pairs: List[TranslationPair]) -> List[TranslationPair]:
    """ Conducts a single round of the quiz, asking questions for each entry.
    Returns the updated list of pairs. """

    shuffle(pairs)
    for pair in pairs:
        ask_translation_question(pair)
    return pairs

def ask_translation_question(pair: TranslationPair) -> None:
    """ Asks the user a question for the given entry.
    Updates the entry's correctness and attempts. """

    if pair.correct:
        return

    prompt_text = select_prompt(pair.prompt)
    print(f"{pair.prompt.categorie} ➜ {Fore.CYAN}{convert_markdown_to_text(prompt_text)}{Style.RESET_ALL}")
    print("----------")

    user_inputs: List[tuple[str, WordGroup]] = []

    for answer_group in pair.answers.groups:
        print(f"{answer_group.categorie} ➜ ", end="")
        user_input = input().strip()
        user_inputs.append((user_input, answer_group))

    incorrect_groups: List[WordGroup] = []
    correct = True
    for user_input, answer_group in user_inputs:
        if not is_correct_answer(user_input, answer_group):
            correct = False
            incorrect_groups.append(answer_group)

    if correct:
        display_correct_message()
        pair.correct = True
    else:
        display_incorrect_message()
        for group in incorrect_groups:
            correct_answers = ', '.join([word.text for word in group.words])
            print(f"{Fore.RED}Correct answer(s): {group.categorie} ➜ {convert_markdown_to_text(correct_answers)}{Style.RESET_ALL}")

    pair.attempts += 1
    print()

def select_prompt(prompt_group: PromptGroup) -> str:
    """ Selects a prompt from the entry's prompt group. """

    return choice(prompt_group.words).text

def is_correct_answer(user_input: str, answer_group: WordGroup) -> bool:
    """ Checks if the user's input matches any of the correct answers.
    Ignores case and asterisks. """

    normalized_input = user_input.lower().replace("*", "")
    normalized_answers = ["".join(word.text.lower().split("*")) for word in answer_group.words]
    return normalized_input in normalized_answers

def display_correct_message() -> None:
    """ Displays a message for a correct answer. """

    print(f"{Fore.GREEN}✅ Correct!{Style.RESET_ALL}")

def display_incorrect_message() -> None:
    """ Displays a message for an incorrect answer, showing the correct answers. """

    print(f"{Fore.RED}❌ Incorrect !!{Style.RESET_ALL}")

def display_completion_message() -> None:
    """ Displays a message when all entries are answered correctly. """

    print(f"{Fore.GREEN}🎉 All entries answered correctly!{Style.RESET_ALL}\n")
