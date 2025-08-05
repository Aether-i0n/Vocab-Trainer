from core.trainer import run_quiz
from core.menu import run_menu, select_file, select_translations

def main():
    run_menu()
    selected_file = select_file()
    translations = select_translations(selected_file)
    run_quiz(translations, selected_file)

if __name__ == "__main__":
    main()
