from core.menu import select_file, select_translations, run_menu
from core.trainer import run_quiz


def main():
    run_menu()
    selected_file = select_file()
    translations = select_translations(selected_file)
    run_quiz(translations, selected_file)

if __name__ == "__main__":
    main()
