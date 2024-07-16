from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QToolTip
from PyQt6.QtCore import Qt, QCoreApplication, QPoint

class CharacterDetails(QWidget):
    def __init__(self):
        super().__init__()
        self.layout = QVBoxLayout(self)

        self.name_label = QLabel(self)
        self.layout.addWidget(self.name_label)

        self.affinity_label = QLabel(self)
        self.layout.addWidget(self.affinity_label)
        self.affinity_label.setMouseTracking(True)  # 启用鼠标跟踪
        self.affinity_label.installEventFilter(self)  # 安装事件过滤器

        self.affinity_label_to_player = QLabel(self)
        self.layout.addWidget(self.affinity_label_to_player)
        self.affinity_label_to_player.setMouseTracking(True)
        self.affinity_label_to_player.installEventFilter(self)

        self.affinity_label_from_player = QLabel(self)
        self.layout.addWidget(self.affinity_label_from_player)
        self.affinity_label_from_player.setMouseTracking(True)
        self.affinity_label_from_player.installEventFilter(self)

        self.attributes_title = QLabel(QCoreApplication.translate("CharacterDetails", "Attributes:"))
        self.layout.addWidget(self.attributes_title)

        self.strength_label = QLabel(self)
        self.layout.addWidget(self.strength_label)
        self.agility_label = QLabel(self)
        self.layout.addWidget(self.agility_label)
        self.charisma_label = QLabel(self)
        self.layout.addWidget(self.charisma_label)
        self.intelligence_label = QLabel(self)
        self.layout.addWidget(self.intelligence_label)

        self.skills_title = QLabel(QCoreApplication.translate("CharacterDetails", "Skills:"))
        self.layout.addWidget(self.skills_title)

        self.running_label = QLabel(self)
        self.layout.addWidget(self.running_label)
        self.riding_label = QLabel(self)
        self.layout.addWidget(self.riding_label)
        self.management_label = QLabel(self)
        self.layout.addWidget(self.management_label)
        self.eloquence_label = QLabel(self)
        self.layout.addWidget(self.eloquence_label)
        self.gathering_label = QLabel(self)
        self.layout.addWidget(self.gathering_label)

        self.traits_title = QLabel(QCoreApplication.translate("CharacterDetails", "Traits:"))
        self.layout.addWidget(self.traits_title)

        self.traits_labels = []

        self.setLayout(self.layout)

    def update_details(self, character, player_character):
        self.character = character
        self.player_character = player_character

        self.name_label.setText(QCoreApplication.translate("CharacterDetails", "Name: {name}").format(name=character.name))
        
        # 计算并显示好感度
        affinity_to_player = character.calculate_affinity(player_character)
        affinity_from_player = player_character.calculate_affinity(character)
        self.affinity_label_to_player.setText(QCoreApplication.translate("CharacterDetails", "Affinity to Player: {value}").format(value=affinity_to_player))
        self.affinity_label_from_player.setText(QCoreApplication.translate("CharacterDetails", "Affinity from Player: {value}").format(value=affinity_from_player))
        
        self.strength_label.setText(QCoreApplication.translate("CharacterDetails", "Strength: {value}").format(value=character.attributes["Strength"]))
        self.agility_label.setText(QCoreApplication.translate("CharacterDetails", "Agility: {value}").format(value=character.attributes["Agility"]))
        self.charisma_label.setText(QCoreApplication.translate("CharacterDetails", "Charisma: {value}").format(value=character.attributes["Charisma"]))
        self.intelligence_label.setText(QCoreApplication.translate("CharacterDetails", "Intelligence: {value}").format(value=character.attributes["Intelligence"]))
        self.running_label.setText(QCoreApplication.translate("CharacterDetails", "Running: {value}").format(value=character.skills["Running"]))
        self.riding_label.setText(QCoreApplication.translate("CharacterDetails", "Riding: {value}").format(value=character.skills["Riding"]))
        self.management_label.setText(QCoreApplication.translate("CharacterDetails", "Management: {value}").format(value=character.skills["Management"]))
        self.eloquence_label.setText(QCoreApplication.translate("CharacterDetails", "Eloquence: {value}").format(value=character.skills["Eloquence"]))
        self.gathering_label.setText(QCoreApplication.translate("CharacterDetails", "Gathering: {value}").format(value=character.skills["Gathering"]))

        # 更新特质显示
        for label in self.traits_labels:
            self.layout.removeWidget(label)
            label.deleteLater()
        self.traits_labels = []
        for trait in character.traits:
            label = QLabel(f"{trait.name}", self)
            self.traits_labels.append(label)
            self.layout.addWidget(label)

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
