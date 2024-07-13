from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel
from PyQt6.QtCore import QCoreApplication

class CharacterDetails(QWidget):
    def __init__(self):
        super().__init__()

        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        self.name_label = QLabel(QCoreApplication.translate("CharacterDetails", "Name: "))
        self.layout.addWidget(self.name_label)

        self.id_label = QLabel(QCoreApplication.translate("CharacterDetails", "ID: "))
        self.layout.addWidget(self.id_label)

        self.attributes_label = QLabel(QCoreApplication.translate("CharacterDetails", "Attributes: "))
        self.layout.addWidget(self.attributes_label)

        self.skills_label = QLabel(QCoreApplication.translate("CharacterDetails", "Skills: "))
        self.layout.addWidget(self.skills_label)

    def update_details(self, character):
        self.name_label.setText(QCoreApplication.translate("CharacterDetails", "Name: {name}").format(name=character.name))
        self.id_label.setText(QCoreApplication.translate("CharacterDetails", "ID: {id}").format(id=character.id))
        self.attributes_label.setText(QCoreApplication.translate("CharacterDetails", "Attributes: {attributes}").format(
            attributes=", ".join(f"{k}: {v}" for k, v in character.attributes.items())))
        self.skills_label.setText(QCoreApplication.translate("CharacterDetails", "Skills: {skills}").format(
            skills=", ".join(f"{k}: {v}" for k, v in character.skills.items())))
