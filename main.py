import sys
from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import QTranslator, QLocale
from game_logic import GameLogic
from ui.main_window import MainWindow

def main():
    app = QApplication(sys.argv)
    
    translator = QTranslator()
    locale = QLocale.system().name()
    translation_file = f"translations/adventure_rpg_{locale}.qm"
    if translator.load(translation_file):
        app.installTranslator(translator)
    else:
        print(f"Translation file '{translation_file}' not found, using default language.")

    game = GameLogic()
    main_window = MainWindow(game)
    main_window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
