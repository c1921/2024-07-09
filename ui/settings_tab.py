from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QComboBox
from PyQt6.QtCore import QCoreApplication

class SettingsTab(QWidget):
    def __init__(self, main_window):
        super().__init__()
        
        self.main_window = main_window
        
        layout = QVBoxLayout()
        
        self.language_label = QLabel(QCoreApplication.translate("SettingsTab", "Select Language"))
        self.language_combo = QComboBox()
        self.language_combo.addItems(["English", "中文"])
        self.language_combo.currentIndexChanged.connect(self.change_language)

        layout.addWidget(self.language_label)
        layout.addWidget(self.language_combo)
        
        self.setLayout(layout)

    def change_language(self):
        language = self.language_combo.currentText()
        if language == "English":
            self.main_window.set_language("en")
        elif language == "中文":
            self.main_window.set_language("zh")
