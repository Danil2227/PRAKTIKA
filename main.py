import sys
from PyQt6.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QLabel, QGridLayout, QHBoxLayout, QSlider
from PyQt6.QtCore import Qt, QSize, QRect, QPoint, QTimer
from PyQt6.QtGui import QPainter, QColor, QBrush, QPen

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

    def select_track2(self):
        self.hide()  # Скрываем текущее окно
        self.track2_window = Track2Window()  # Создаем новое окно для трассы 2
        self.track2_window.show()  # Показываем новое окно

class Track2Window(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setStyleSheet("background-color: #FFFFFF;")
        self.setWindowTitle('Трасса 2')
        self.setGeometry(0, 0, 800, 600)
        self.center()

        self.grid_size = 20
        self.track = self.create_track()
        self.start_position = (1, 1)
        self.finish_position = (self.grid_size - 2, 1)
        self.player_positions = [self.start_position, (1, 2)]
        self.speeds = [1, 1]
        self.current_player = 0

        self.layout = QVBoxLayout()
        self.grid_layout = QGridLayout()
        self.update_grid()

        self.button_layout = QHBoxLayout()
        self.forward_button = QPushButton('Вперед')
        self.forward_button.setFixedSize(100, 30)
        self.forward_button.clicked.connect(lambda: self.move_car(0, 1))
        self.right_diag_button = QPushButton('По правой диагонали')
        self.right_diag_button.setFixedSize(100, 30)
        self.right_diag_button.clicked.connect(lambda: self.move_car(1, 1))
        self.left_diag_button = QPushButton('По левой диагонали')
        self.left_diag_button.setFixedSize(100, 30)
        self.left_diag_button.clicked.connect(lambda: self.move_car(-1, 1))

        self.increase_speed_button = QPushButton('Увеличить скорость')
        self.increase_speed_button.setFixedSize(150, 30)
        self.increase_speed_button.clicked.connect(self.increase_speed)
        self.decrease_speed_button = QPushButton('Уменьшить скорость')
        self.decrease_speed_button.setFixedSize(150, 30)
        self.decrease_speed_button.clicked.connect(self.decrease_speed)

        self.button_layout.addWidget(self.forward_button)
        self.button_layout.addWidget(self.right_diag_button)
        self.button_layout.addWidget(self.left_diag_button)
        self.button_layout.addWidget(self.increase_speed_button)
        self.button_layout.addWidget(self.decrease_speed_button)

        self.speed_labels = [QLabel(f'Speed: {self.speeds[0]}'), QLabel(f'Speed: {self.speeds[1]}')]
        self.speed_labels[0].setStyleSheet("color: red;")
        self.speed_labels[1].setStyleSheet("color: blue;")

        self.layout.addLayout(self.grid_layout)
        self.layout.addLayout(self.button_layout)
        self.layout.addWidget(self.speed_labels[0], alignment=Qt.AlignmentFlag.AlignLeft)
        self.layout.addWidget(self.speed_labels[1], alignment=Qt.AlignmentFlag.AlignRight)

        self.setLayout(self.layout)

    def center(self):
        frameGm = self.frameGeometry()
        centerPoint = QApplication.primaryScreen().availableGeometry().center()
        frameGm.moveCenter(centerPoint)
        self.move(frameGm.topLeft())

    def create_track(self):
        track = [[0 for _ in range(self.grid_size)] for _ in range(self.grid_size)]
        for i in range(self.grid_size):
            track[0][i] = 1
            track[self.grid_size-1][i] = 1
            track[i][0] = 1
            track[i][self.grid_size-1] = 1

        for i in range(3, self.grid_size - 3):
            track[i][3] = 3
            track[i][self.grid_size - 3] = 3

        for j in range(2, self.grid_size - 3):
            track[2][j] = 3
            track[self.grid_size - 3][j] = 3

        for i in range(6, self.grid_size - 6):
            track[6][i] = 1
            track[self.grid_size - 7][i] = 1
            track[i][6] = 1
            track[i][self.grid_size - 7] = 1

        return track

    def update_grid(self):
        for i in range(self.grid_size):
            for j in range(self.grid_size):
                label = QLabel()
                if self.track[i][j] == 1:
                    label.setStyleSheet("background-color: black;")
                elif (i, j) in self.player_positions:
                    label.setStyleSheet("background-color: red;" if self.player_positions.index((i, j)) == 0 else "background-color: blue;")
                elif (i, j) == self.finish_position:
                    label.setStyleSheet("background-color: green;")
                else:
                    label.setStyleSheet("background-color: white;")
                self.grid_layout.addWidget(label, i, j)

    def move_car(self, dx, dy):
        x, y = self.player_positions[self.current_player]
        speed = self.speeds[self.current_player]
        new_x, new_y = x + dx * speed, y + dy * speed

        if (new_x, new_y) == self.finish_position:
            print(f"Player {self.current_player + 1} wins!")
            self.reset_game()
            return

        if 0 <= new_x < self.grid_size and 0 <= new_y < self.grid_size and self.track[new_x][new_y] == 0:
            self.player_positions[self.current_player] = (new_x, new_y)
        else:
            self.player_positions[self.current_player] = self.start_position
            self.speeds[self.current_player] = 1

        self.update_grid()
        self.speed_labels[self.current_player].setText(f'Speed: {self.speeds[self.current_player]}')
        self.current_player = 1 - self.current_player

    def increase_speed(self):
        self.speeds[self.current_player] += 1
        self.speed_labels[self.current_player].setText(f'Speed: {self.speeds[self.current_player]}')

    def decrease_speed(self):
        if self.speeds[self.current_player] > 1:
            self.speeds[self.current_player] -= 1
            self.speed_labels[self.current_player].setText(f'Speed: {self.speeds[self.current_player]}')

    def reset_game(self):
        self.player_positions = [self.start_position, (1, 2)]
        self.speeds = [1, 1]
        self.current_player = 0
        self.update_grid()
        self.speed_labels[0].setText(f'Speed: {self.speeds[0]}')
        self.speed_labels[1].setText(f'Speed: {self.speeds[1]}')

class Track1Window(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setStyleSheet("background-color: #FFFFFF;")  # Устанавливаем белый фон
        self.setWindowTitle('Трасса 1')
        self.setGeometry(0, 0, 800, 600)
        self.center()

        game_area = QWidget(self)
        game_area.setGeometry(0, 0, 600, 600)  # Игровое поле занимает 75% экрана
        game_area.setStyleSheet("background-color: #FFFFFF;")

        button_area = QWidget(self)
        button_area.setGeometry(600, 0, 200, 600)  # Поле для кнопок занимает 25% экрана
        button_area.setStyleSheet("background-color: #87CEEB;")  # Цветовой фон для кнопок

        play_btn1 = QPushButton('1', self)
        play_btn1.move(610, 120)
        play_btn1.setFixedSize(30, 30)
        play_btn1.setStyleSheet("background-color: #FF0000; color: white;")

        play_btn2 = QPushButton('2', self)
        play_btn2.move(650, 120)
        play_btn2.setFixedSize(30, 30)
        play_btn2.setStyleSheet("background-color: #FF0000; color: white;")

        play_btn3 = QPushButton('3', self)
        play_btn3.move(690, 120)
        play_btn3.setFixedSize(30, 30)
        play_btn3.setStyleSheet("background-color: #FF0000; color: white;")


        play_up = QPushButton('up', self)
        play_up.move(740, 100)
        play_up.setFixedSize(45, 30)
        play_up.setStyleSheet("background-color: #FF0000; color: white;")

        play_down = QPushButton('down', self)
        play_down.move(740, 140)
        play_down.setFixedSize(45, 30)
        play_down.setStyleSheet("background-color: #FF0000; color: white;")

        back_btn = QPushButton('Назад', button_area)
        back_btn.move(35, 500)
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








