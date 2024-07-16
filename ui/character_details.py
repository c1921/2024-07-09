from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QToolTip, QGroupBox, QHBoxLayout, QFormLayout
from PyQt6.QtCore import Qt, QCoreApplication, QPoint

class CharacterDetails(QWidget):
    def __init__(self):
        super().__init__()
        self.layout = QVBoxLayout(self)

        self.name_label = QLabel(self)
        self.layout.addWidget(self.name_label)

        # Affinity Group
        self.affinity_group = QGroupBox(QCoreApplication.translate("CharacterDetails", "Affinity"))
        self.affinity_layout = QVBoxLayout(self.affinity_group)
        self.affinity_label_to_player = QLabel(self)
        self.affinity_label_to_player.setMouseTracking(True)
        self.affinity_label_to_player.installEventFilter(self)
        self.affinity_layout.addWidget(self.affinity_label_to_player)
        self.affinity_label_from_player = QLabel(self)
        self.affinity_label_from_player.setMouseTracking(True)
        self.affinity_label_from_player.installEventFilter(self)
        self.affinity_layout.addWidget(self.affinity_label_from_player)
        self.layout.addWidget(self.affinity_group)

        # Attributes Group
        self.attributes_group = QGroupBox(QCoreApplication.translate("CharacterDetails", "Attributes"))
        self.attributes_layout = QFormLayout(self.attributes_group)
        self.strength_label = QLabel(self)
        self.attributes_layout.addRow(QCoreApplication.translate("CharacterDetails", "Strength:"), self.strength_label)
        self.agility_label = QLabel(self)
        self.attributes_layout.addRow(QCoreApplication.translate("CharacterDetails", "Agility:"), self.agility_label)
        self.charisma_label = QLabel(self)
        self.attributes_layout.addRow(QCoreApplication.translate("CharacterDetails", "Charisma:"), self.charisma_label)
        self.intelligence_label = QLabel(self)
        self.attributes_layout.addRow(QCoreApplication.translate("CharacterDetails", "Intelligence:"), self.intelligence_label)
        self.layout.addWidget(self.attributes_group)

        # Skills Group
        self.skills_group = QGroupBox(QCoreApplication.translate("CharacterDetails", "Skills"))
        self.skills_layout = QFormLayout(self.skills_group)
        self.running_label = QLabel(self)
        self.skills_layout.addRow(QCoreApplication.translate("CharacterDetails", "Running:"), self.running_label)
        self.riding_label = QLabel(self)
        self.skills_layout.addRow(QCoreApplication.translate("CharacterDetails", "Riding:"), self.riding_label)
        self.management_label = QLabel(self)
        self.skills_layout.addRow(QCoreApplication.translate("CharacterDetails", "Management:"), self.management_label)
        self.eloquence_label = QLabel(self)
        self.skills_layout.addRow(QCoreApplication.translate("CharacterDetails", "Eloquence:"), self.eloquence_label)
        self.gathering_label = QLabel(self)
        self.skills_layout.addRow(QCoreApplication.translate("CharacterDetails", "Gathering:"), self.gathering_label)
        self.layout.addWidget(self.skills_group)

        # Traits Group
        self.traits_group = QGroupBox(QCoreApplication.translate("CharacterDetails", "Traits"))
        self.traits_layout = QVBoxLayout(self.traits_group)
        self.layout.addWidget(self.traits_group)

        self.traits_labels = []

        self.setLayout(self.layout)

    def update_details(self, character, player_character):
        self.character = character
        self.player_character = player_character

        self.name_label.setText(QCoreApplication.translate("CharacterDetails", "Name: {name} {surname} ({gender})").format(name=character.name, surname=character.surname, gender=character.gender.capitalize()))
        
        # 计算并显示好感度
        affinity_to_player = character.calculate_affinity(player_character)
        affinity_from_player = player_character.calculate_affinity(character)
        self.affinity_label_to_player.setText(QCoreApplication.translate("CharacterDetails", "Affinity to Player: {value}").format(value=affinity_to_player))
        self.affinity_label_from_player.setText(QCoreApplication.translate("CharacterDetails", "Affinity from Player: {value}").format(value=affinity_from_player))
        
        self.strength_label.setText(QCoreApplication.translate("CharacterDetails", "{value}").format(value=character.attributes["Strength"]))
        self.agility_label.setText(QCoreApplication.translate("CharacterDetails", "{value}").format(value=character.attributes["Agility"]))
        self.charisma_label.setText(QCoreApplication.translate("CharacterDetails", "{value}").format(value=character.attributes["Charisma"]))
        self.intelligence_label.setText(QCoreApplication.translate("CharacterDetails", "{value}").format(value=character.attributes["Intelligence"]))
        self.running_label.setText(QCoreApplication.translate("CharacterDetails", "{value}").format(value=character.skills["Running"]))
        self.riding_label.setText(QCoreApplication.translate("CharacterDetails", "{value}").format(value=character.skills["Riding"]))
        self.management_label.setText(QCoreApplication.translate("CharacterDetails", "{value}").format(value=character.skills["Management"]))
        self.eloquence_label.setText(QCoreApplication.translate("CharacterDetails", "{value}").format(value=character.skills["Eloquence"]))
        self.gathering_label.setText(QCoreApplication.translate("CharacterDetails", "{value}").format(value=character.skills["Gathering"]))

        # 更新特质显示
        for label in self.traits_labels:
            self.traits_layout.removeWidget(label)
            label.deleteLater()
        self.traits_labels = []
        for trait in character.traits:
            label = QLabel(f"{trait.name}", self)
            self.traits_labels.append(label)
            self.traits_layout.addWidget(label)

    def eventFilter(self, source, event):
        if event.type() == event.Type.ToolTip:
            if source == self.affinity_label_to_player:
                tooltip_text = self.generate_tooltip_text(self.character, self.player_character)
                QToolTip.showText(event.globalPos(), tooltip_text, self.affinity_label_to_player)
            elif source == self.affinity_label_from_player:
                tooltip_text = self.generate_tooltip_text(self.player_character, self.character)
                QToolTip.showText(event.globalPos(), tooltip_text, self.affinity_label_from_player)
        return super().eventFilter(source, event)

    def generate_tooltip_text(self, from_character, to_character):
        # 计算角色对玩家的好感度详细信息
        affinity = from_character.calculate_affinity(to_character)
        
        details = []
        details.append(f"{from_character.name}'s affinity to {to_character.name}")

        for trait in from_character.traits:
            if trait in to_character.traits:
                details.append(f"Both have {trait.name} +20")
            if any(exclusive_trait in to_character.traits for exclusive_trait in trait.exclusive_traits):
                details.append(f"{trait.name} against {', '.join(trait.exclusive_traits)} -20")

        details.append(f"{to_character.name}'s charisma +{to_character.attributes['Charisma'] * 5}")
        
        details.append("——————————")
        details.append(f"{affinity}")

        return "\n".join(details)
