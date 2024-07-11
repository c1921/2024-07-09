from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel

class CharacterDetails(QWidget):
    def __init__(self):
        super().__init__()

        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        self.name_label = QLabel("Name: ")
        self.layout.addWidget(self.name_label)

        self.id_label = QLabel("ID: ")
        self.layout.addWidget(self.id_label)

        self.attributes_label = QLabel("Attributes: ")
        self.layout.addWidget(self.attributes_label)

        self.skills_label = QLabel("Skills: ")
        self.layout.addWidget(self.skills_label)

    def update_details(self, character):
        self.name_label.setText(f"Name: {character.name}")
        self.id_label.setText(f"ID: {character.id}")
        self.attributes_label.setText("Attributes: " + ", ".join(f"{k}: {v}" for k, v in character.attributes.items()))
        self.skills_label.setText("Skills: " + ", ".join(f"{k}: {v}" for k, v in character.skills.items()))
