from core.file_selector import select_vocab_file
from core.loader import load_translations_progress
from core.menu import main_menu
from core.results import run_results
from core.trainer import run_vocabulary_quiz
from core.translations_selector import select_translations


def main():
    main_menu()
    selected_file = select_vocab_file()
    use_saved = load_translations_progress(selected_file)
    selected_translations = select_translations(use_saved, selected_file)
    run_vocabulary_quiz(selected_translations, selected_file)
    run_results(selected_translations, selected_file)

if __name__ == "__main__":
    main()
