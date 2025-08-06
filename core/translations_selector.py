from pathlib import Path
from random import randint
from typing import List

from core.loader import load_vocab, load_progress
from core.utils import Translation, Data


def select_translations(use_saved: bool, selected_file: Path) -> List[Translation]:
    if use_saved:
        return load_progress(selected_file)
    else:

        vocab_data = load_vocab(selected_file)

        mode = input(f"Mode? ({vocab_data.lang1} / {vocab_data.lang2} / random): ").strip().lower()
        if mode not in [vocab_data.lang1, vocab_data.lang2, 'random']:
            print(f"Invalid mode. Defaulting to {vocab_data.lang1}.")
            mode = vocab_data.lang1
        
        all_pairs = prepare_pairs(vocab_data, {vocab_data.lang1: "forward", vocab_data.lang2: "reverse", "random": "random"}[mode])
        return [Translation(p, a) for p, a in all_pairs]

def prepare_pairs(vocab_data: Data, mode: str) -> List[tuple[str, str]]:
    vocab = vocab_data.vocab
    if mode == "reverse":
        return [(b, a) for a, b in vocab]
    elif mode == "random":
        return [(a, b) if randint(0, 1) else (b, a) for a, b in vocab]
    else:
        return [(a, b) for a, b in vocab]