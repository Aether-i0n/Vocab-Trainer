""" Allows the user to select which translations to practice from the loaded vocabulary set. """

from pathlib import Path
from random import randint
from typing import List

from core.loader import load_vocab_data, load_translations_progress
from core.utils import AnswerGroup, AnswerGroups, PromptGroup, TranslationPair, VocabData, VocabEntry


def select_translations(use_saved: bool, selected_file: Path) -> List[TranslationPair]:
    """ Returns a list of Translation objects based on user selection.
    If use_saved is True, loads saved progress. Otherwise, prompts for mode and generates translation pairs. """
    
    if use_saved:
        return load_translations_progress(selected_file)
    
    vocab_data = load_vocab_data(selected_file)
    mode = get_translation_mode(vocab_data)
    pairs = generate_translation_pairs(vocab_data, mode)

    return [TranslationPair(prompt, answers) for prompt, answers in pairs]

def get_translation_mode(vocab_data: VocabData) -> str:
    """ Prompts the user to select a translation mode: lang1, lang2, or random.
    Returns the selected mode as a string. """
    
    options = vocab_data.languages + ["random"]
    mode = input(f"Mode? ({' / '.join(options)}): ").strip().lower()
    if mode not in options:
        print(f"Invalid mode. Defaulting to {vocab_data.languages[0]}.")
        return vocab_data.languages[0]
    return mode

def generate_translation_pairs(vocab_data: VocabData, mode: str):
    """ Builds translation pairs based on the selected mode.
    If mode is 'random', generates pairs with randomly selected prompt languages.
    Otherwise, generates pairs with the specified prompt language. """

    if mode == "random":
        return [random_pair(entry, vocab_data.languages) for entry in vocab_data.entries]
    
    idx = vocab_data.languages.index(mode)
    return [forward_pair(entry, idx, vocab_data.languages) for entry in vocab_data.entries]

def forward_pair(entry: VocabEntry, idx: int, languages: List[str]):
    """ Constructs a translation pair for a specific language index. """

    prompt_group = PromptGroup(entry.groups[idx].words, languages[idx])
    answer_groups = AnswerGroups([
        AnswerGroup(entry.groups[i].words, languages[i])
        for i in range(len(entry.groups)) if i != idx
    ])
    return (prompt_group, answer_groups)

def random_pair(entry: VocabEntry, languages: List[str]):
    """ Constructs a translation pair with a randomly selected prompt language. """

    idx = randint(0, len(entry.groups) - 1)
    return forward_pair(entry, idx, languages)
