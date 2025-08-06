""" Allows the user to select which translations to practice from the loaded vocabulary set. """

from pathlib import Path
from random import randint
from typing import List

from core.loader import load_vocab_data, load_translations_progress
from core.utils import Translation, Data


def select_translations(use_saved: bool, selected_file: Path) -> List[Translation]:
    """ Returns a list of Translation objects based on user selection.
    If use_saved is True, loads saved progress. Otherwise, prompts for mode and generates translation pairs. """
    
    if use_saved:
        return load_translations_progress(selected_file)
    
    vocab_data = load_vocab_data(selected_file)
    mode = get_translation_mode(vocab_data)
    pairs = generate_translation_pairs(vocab_data, mode)

    return create_translation_objects(pairs)

def get_translation_mode(vocab_data: Data) -> str:
    """ Prompts the user to select a translation mode: lang1, lang2, or random.
    Returns the selected mode as a string. """

    mode_input = input(f"Mode? ({vocab_data.lang1} / {vocab_data.lang2} / random): ").strip().lower()
    valid_modes = [vocab_data.lang1, vocab_data.lang2, 'random']

    if mode_input not in valid_modes:
        print(f"Invalid mode. Defaulting to {vocab_data.lang1}.")
        return vocab_data.lang1
    
    return mode_input

def generate_translation_pairs(vocab_data: Data, mode: str) -> List[tuple[str, str]]:
    """ Generates translation pairs based on the selected mode.
    Modes:
        - vocab_data.lang1: forward (a, b)
        - vocab_data.lang2: reverse (b, a)
        - random: randomly selects (a, b) or (b, a) for each pair
    Returns a list of tuple pairs. """

    if mode == vocab_data.lang2:
        return reverse_pairs(vocab_data.vocab)
    
    elif mode == 'random':
        return randomize_pairs(vocab_data.vocab)
    
    return forward_pairs(vocab_data.vocab)

def forward_pairs(vocab: List[tuple[str, str]]) -> List[tuple[str, str]]:
    """ Returns translation pairs in forward order (a, b). """

    return [(a, b) for a, b in vocab]

def reverse_pairs(vocab: List[tuple[str, str]]) -> List[tuple[str, str]]:
    """ Returns translation pairs in reverse order (b, a). """

    return [(b, a) for a, b in vocab]

def randomize_pairs(vocab: List[tuple[str, str]]) -> List[tuple[str, str]]:
    """ Randomly selects forward or reverse order for each translation pair. """

    return [(a, b) if randint(0, 1) else (b, a) for a, b in vocab]

def create_translation_objects(pairs: List[tuple[str, str]]) -> List[Translation]:
    """ Converts a list of tuple pairs into a list of Translation objects. """

    return [Translation(prompt, answer) for prompt, answer in pairs]