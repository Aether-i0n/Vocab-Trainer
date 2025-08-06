from core.file_selector import select_file
from core.loader import load_previous_progress
from core.menu import run_menu
from core.trainer import run_quiz
from core.translations_selector import select_translations


def main():
    run_menu()
    selected_file = select_file()
    use_saved = load_previous_progress(selected_file)
    selected_translations = select_translations(use_saved, selected_file)
    run_quiz(selected_translations, selected_file)

if __name__ == "__main__":
    main()
