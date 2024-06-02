import sys
from PyQt6.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QLabel


class GameWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setStyleSheet("background-color: #87CEEB;")
        self.setWindowTitle('Игра')
        self.setGeometry(0, 0, 800, 600)
        self.center()

        track1_btn = QPushButton('Трасса 1', self)
        track1_btn.move(130, 180)
        track1_btn.setFixedSize(130, 30)
        track1_btn.setStyleSheet("background-color: #FF0000; color: white;")
        track1_btn.clicked.connect(self.select_track1)

        track2_btn = QPushButton('Трасса 2', self)
        track2_btn.move(550, 180)
        track2_btn.setFixedSize(130, 30)
        track2_btn.setStyleSheet("background-color: #FF0000; color: white;")
        track2_btn.clicked.connect(self.select_track2)

        back_btn = QPushButton('Назад', self)
        back_btn.move(340, 110)
        back_btn.setFixedSize(130, 30)
        back_btn.setStyleSheet("background-color: #FF0000; color: white;")
        back_btn.clicked.connect(self.back_to_menu)

    def back_to_menu(self):
        self.close()
        global game_menu
        game_menu.show()
    def center(self):
        frameGm = self.frameGeometry()
        centerPoint = QApplication.primaryScreen().availableGeometry().center()
        frameGm.moveCenter(centerPoint)
        self.move(frameGm.topLeft())


    def select_track1(self):
        print()

    def select_track2(self):
        print()

    def select_track1(self):
        self.hide()  # Скрываем текущее окно
        self.track1_window = Track1Window()  # Создаем новое окно для трассы 1
        self.track1_window.show()  # Показываем новое окно


class Track1Window(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setStyleSheet("background-color: #87CEEB;")
        self.setWindowTitle('Трасса 1')
        self.setGeometry(0, 0, 800, 600)
        self.center()
    def center(self):
        frameGm = self.frameGeometry()
        centerPoint = QApplication.primaryScreen().availableGeometry().center()
        frameGm.moveCenter(centerPoint)
        self.move(frameGm.topLeft())




class RulesWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Правила')
        self.setGeometry(0, 0, 800, 600)
        self.setStyleSheet("background-color: 0000;")
        self.center()

        rules_label = QLabel("Правила игры", self)
        rules_label.setStyleSheet("font-size: 18px; color: black;")
        rules_label.move(150, 30)

        back_btn = QPushButton('Назад', self)
        back_btn.move(320, 500)
        back_btn.setFixedSize(170, 40)
        back_btn.setStyleSheet("background-color: #FF0000; color: white;")
        back_btn.clicked.connect(self.back_to_menu)

    def back_to_menu(self):
        self.close()
        global game_menu
        game_menu.show()



    def center(self):
        frameGm = self.frameGeometry()
        centerPoint = QApplication.primaryScreen().availableGeometry().center()
        frameGm.moveCenter(centerPoint)
        self.move(frameGm.topLeft())


class GameMenu(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setStyleSheet("background-color: #87CEEB;")

        word_label = QLabel('ГОНКИ НА БУМАГЕ', self)
        word_label.setStyleSheet("font-size: 22px; color: black;")

        play_btn = QPushButton('Играть', self)
        play_btn.setFixedSize(120, 30)
        play_btn.setStyleSheet("background-color: #32CD32; color: white;")

        rules_btn = QPushButton('Правила', self)
        rules_btn.setFixedSize(120, 30)
        rules_btn.setStyleSheet("background-color: #ff9763; color: white;")

        exit_btn = QPushButton('Выход', self)
        exit_btn.setFixedSize(120, 30)
        exit_btn.setStyleSheet("background-color: #FF0000; color: white;")

        play_btn.move(340, 225)
        word_label.move(310, 10)
        rules_btn.move(340, 280)
        exit_btn.move(340, 330)

        self.setWindowTitle('Меню игры')
        self.setGeometry(0, 0, 800, 600)
        self.center()

        play_btn.clicked.connect(self.open_game_window)
        rules_btn.clicked.connect(self.open_rules_window)
        exit_btn.clicked.connect(self.close)

    def center(self):
        frameGm = self.frameGeometry()
        centerPoint = QApplication.primaryScreen().availableGeometry().center()
        frameGm.moveCenter(centerPoint)
        self.move(frameGm.topLeft())

    def open_game_window(self):
        self.game_window = GameWindow()
        self.game_window.show()
        self.close()

    def open_rules_window(self):
        global rules_window
        rules_window = RulesWindow()
        rules_window.show()
        self.close()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    game_menu = GameMenu()
    game_menu.show()
    rules_window = None
    sys.exit(app.exec())








