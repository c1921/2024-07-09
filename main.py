import sys
from PyQt6.QtWidgets import QApplication
from game_logic import GameLogic
from ui.main_window import MainWindow

def main():
    app = QApplication(sys.argv)
    game = GameLogic()
    main_window = MainWindow(game)
    main_window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
