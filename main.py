import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QLabel, QVBoxLayout, QWidget
from PyQt6.QtCore import QTimer, QTime, QDateTime

class AdventureRPG(QMainWindow):
    def __init__(self):
        super().__init__()

        # 初始化时间和距离
        self.game_time = QTime(0, 0)
        self.day_count = 1
        self.distance = 0.0
        self.speed_per_minute = 100  # 每分钟100米

        # 设置窗口
        self.setWindowTitle("Adventure RPG")
        self.setGeometry(100, 100, 300, 200)

        # 创建标签
        self.time_label = QLabel(self)
        self.distance_label = QLabel(self)
        self.update_labels()

        # 布局
        layout = QVBoxLayout()
        layout.addWidget(self.time_label)
        layout.addWidget(self.distance_label)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

        # 设置计时器
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_time_and_distance)
        self.timer.start(1000)  # 每秒触发一次

    def update_time_and_distance(self):
        # 更新游戏时间
        self.game_time = self.game_time.addSecs(60)
        if self.game_time.hour() == 0 and self.game_time.minute() == 0:
            self.day_count += 1

        # 更新距离
        self.distance += self.speed_per_minute

        # 更新标签显示
        self.update_labels()

    def update_labels(self):
        time_text = f"Day {self.day_count}, {self.game_time.toString('HH:mm')}"
        distance_text = f"Distance traveled: {self.distance:.2f} meters"
        self.time_label.setText(time_text)
        self.distance_label.setText(distance_text)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    rpg = AdventureRPG()
    rpg.show()
    sys.exit(app.exec())
