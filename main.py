import sys
import json
from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import QTranslator, QLocale
from game_logic import GameLogic
from ui.main_window import MainWindow

def load_settings():
    try:
        with open("settings.json", "r") as f:
            settings = json.load(f)
    except FileNotFoundError:
        settings = {"language": "en"}
    return settings

def main():
    app = QApplication(sys.argv)
    
    translator = QTranslator()
    settings = load_settings()
    language = settings.get("language", "en")
    translation_file = f"translations/{language}.qm"
    
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
