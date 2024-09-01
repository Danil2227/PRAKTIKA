import sys
from PyQt6.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QLabel, QGridLayout, QHBoxLayout
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QPixmap

class GameWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setStyleSheet("background-color: #87CEEB;")
        self.setWindowTitle('Выбор трассы')
        self.setGeometry(0, 0, 800, 600)
        self.center()

        track1_btn = QPushButton('Трасса 1', self)
        track1_btn.move(80, 180)
        track1_btn.setFixedSize(200, 40)
        track1_btn.setStyleSheet("background-color: #ff9763; color: white;font-size: 35px")
        track1_btn.clicked.connect(self.select_track1)

        track2_btn = QPushButton('Трасса 2', self)
        track2_btn.move(510, 180)
        track2_btn.setFixedSize(200, 40)
        track2_btn.setStyleSheet("background-color: #ff9763; color: white;font-size: 35px")
        track2_btn.clicked.connect(self.select_track2)

        back_btn = QPushButton('Назад', self)
        back_btn.move(295, 110)
        back_btn.setFixedSize(200, 40)
        back_btn.setStyleSheet("background-color: #FF0000; color: white; font-size: 35px")
        back_btn.clicked.connect(self.back_to_menu)

        # QLabel для отображения изображения трассы 1
        self.track1_label = QLabel(self)
        self.track1_pixmap = QPixmap(r'C:\Users\DANIL\PycharmProjects\GAME\TRASSA1.jpg')  # Укажите путь к изображению
        self.track1_label.setPixmap(self.track1_pixmap)
        self.track1_label.setScaledContents(True)  # Подгонка под размер QLabel
        self.track1_label.setFixedSize(350, 300)  # Задайте размер QLabel для изображения
        self.track1_label.move(15, 250)  # Расположите ниже кнопки трассы 1

        self.track2_label = QLabel(self)
        self.track2_pixmap = QPixmap(r'C:\Users\DANIL\PycharmProjects\GAME\TRASSA2.jpg')  # Укажите путь к изображению
        self.track2_label.setPixmap(self.track2_pixmap)
        self.track2_label.setScaledContents(True)  # Подгонка под размер QLabel
        self.track2_label.setFixedSize(350, 300)  # Задайте размер QLabel для изображения
        self.track2_label.move(435, 250)  # Расположите ниже кнопки трассы 1

        # Убедитесь, что QLabel отображается после кнопки
        self.show()

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
        self.hide()
        self.track1_window = Track1Window()
        self.track1_window.show()

    def select_track2(self):
        self.hide()
        self.track2_window = Track2Window()
        self.track2_window.show()



from PyQt6.QtWidgets import QWidget, QVBoxLayout, QGridLayout, QLabel, QPushButton, QApplication, QHBoxLayout
from PyQt6.QtCore import Qt

class Track2Window(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.speed_changed = False
        self.first_turn = True

    def initUI(self):
        self.setStyleSheet("background-color: #ADD8E6;")
        self.setWindowTitle('Трасса 2')
        self.setGeometry(0, 0, 800, 600)
        self.center()

        self.grid_size = 20
        self.track = self.create_track()
        self.start_positions = [(self.grid_size - 3, 1), (self.grid_size - 5, 1)]
        self.player_positions = self.start_positions.copy()
        self.speeds = [1, 1]
        self.current_player = 0

        self.layout = QVBoxLayout()
        self.grid_layout = QGridLayout()
        self.grid_labels = [[QLabel() for _ in range(self.grid_size)] for _ in range(self.grid_size)]
        self.update_grid()

        self.button_layout = QHBoxLayout()
        self.create_buttons()

        self.speed_labels = [QLabel(f'Speed: {self.speeds[0]}'), QLabel(f'Speed: {self.speeds[1]}')]
        self.speed_labels[0].setStyleSheet("color: red; font-size: 25px;")
        self.speed_labels[1].setStyleSheet("color: blue; font-size: 25px")

        self.turn_label = QLabel('Ход красной машинки')
        self.turn_label.setStyleSheet("color: red; font-size: 25px;")

        self.winner_label = QLabel('')
        self.winner_label.setStyleSheet("color: green; font-size: 24px;")
        self.winner_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.layout.addLayout(self.grid_layout)
        self.layout.addLayout(self.button_layout)
        self.layout.addWidget(self.turn_label, alignment=Qt.AlignmentFlag.AlignCenter)
        self.layout.addWidget(self.speed_labels[0], alignment=Qt.AlignmentFlag.AlignLeft)
        self.layout.addWidget(self.speed_labels[1], alignment=Qt.AlignmentFlag.AlignRight)
        self.layout.addWidget(self.winner_label, alignment=Qt.AlignmentFlag.AlignCenter)

        back_btn = QPushButton('В меню', self)
        back_btn.setFixedSize(150, 40)
        back_btn.setStyleSheet("background-color: #808080; color: white;font-size: 25px")
        back_btn.clicked.connect(self.back_to_menu)
        self.layout.addWidget(back_btn, alignment=Qt.AlignmentFlag.AlignCenter)

        self.setLayout(self.layout)

    def create_buttons(self):
        directions = [("←", 0, -1), ("↑", -1, 0), ("↓", 1, 0), ("→", 0, 1),
                      ("⭩", 1, -1), ("⭨", 1, 1), ("⭦", -1, -1), ("Ы", -1, 1)]
        for text, dx, dy in directions:
            button = QPushButton(text)
            button.setFixedSize(40, 40)
            button.setStyleSheet("background-color: yellow; font-size: 40px;")
            button.clicked.connect(lambda _, dx=dx, dy=dy: self.move_car(dx, dy))
            self.button_layout.addWidget(button)

        self.increase_speed_button = QPushButton('➕')
        self.increase_speed_button.setFixedSize(50, 30)
        self.increase_speed_button.setStyleSheet("background-color: green;  font-size: 25px")
        self.increase_speed_button.clicked.connect(self.increase_speed)
        self.increase_speed_button.setEnabled(False)

        self.decrease_speed_button = QPushButton('➖')
        self.decrease_speed_button.setFixedSize(50, 30)
        self.decrease_speed_button.setStyleSheet("background-color: red; font-size: 25px")
        self.decrease_speed_button.clicked.connect(self.decrease_speed)

        self.button_layout.addWidget(self.increase_speed_button)
        self.button_layout.addWidget(self.decrease_speed_button)

    def back_to_menu(self):
        self.close()
        global game_menu
        game_menu.show()

    def center(self):
        frameGm = self.frameGeometry()
        centerPoint = QApplication.primaryScreen().availableGeometry().center()
        frameGm.moveCenter(centerPoint)
        self.move(frameGm.topLeft())

    def create_track(self):
        track = [[0 for _ in range(self.grid_size)] for _ in range(self.grid_size)]
        for i in range(self.grid_size):
            track[0][i] = 1
            track[self.grid_size - 1][i] = 1
            track[i][0] = 1
            track[i][self.grid_size - 1] = 1

        for i in range(3, self.grid_size - 3):
            track[i][3] = 3
            track[i][self.grid_size - 3] = 3

        for j in range(2, self.grid_size - 3):
            track[2][j] = 3
            track[self.grid_size - 3][j] = 3

        for i in range(6, self.grid_size - 6):
            track[6][i] = 1
            track[7][i] = 1
            track[8][i] = 1
            track[9][i] = 1
            track[10][i] = 1
            track[11][i] = 1
            track[12][i] = 1
            track[self.grid_size - 7][i] = 1
            track[i][6] = 1
            track[i][4] = 1
            track[i][3] = 1
            track[i][2] = 1
            track[i][1] = 1
            track[i][5] = 1
            track[i][self.grid_size - 7] = 1

        for i in range(1, 6):
            track[i][self.grid_size - 20] = 4

        return track

    def update_grid(self):
        for i in range(self.grid_size):
            for j in range(self.grid_size):
                if self.track[i][j] == 1:
                    self.grid_labels[i][j].setStyleSheet("background-color: black;")
                elif self.track[i][j] == 4:
                    self.grid_labels[i][j].setStyleSheet("background-color: green;")
                elif (i, j) in self.player_positions:
                    index = self.player_positions.index((i, j))
                    self.grid_labels[i][j].setStyleSheet("background-color: red; " if index == 0 else "background-color: blue;")
                else:
                    self.grid_labels[i][j].setStyleSheet("background-color: white;")
                self.grid_layout.addWidget(self.grid_labels[i][j], i, j)

    def move_car(self, dx, dy):
        x, y = self.player_positions[self.current_player]
        speed = self.speeds[self.current_player]
        new_x, new_y = x + dx * speed, y + dy * speed

        if 0 <= new_x < self.grid_size and 0 <= new_y < self.grid_size:
            if self.track[new_x][new_y] in (0, 3):
                self.player_positions[self.current_player] = (new_x, new_y)
            elif self.track[new_x][new_y] == 1:
                self.reset_position()
            elif self.track[new_x][new_y] == 4:
                self.winner_label.setText(f'Победила {"красная" if self.current_player == 0 else "синяя"} машинка!')
                self.reset_game()
                return
        else:
            self.reset_position()

        self.update_grid()
        self.speed_labels[self.current_player].setText(f'Speed: {self.speeds[self.current_player]}')
        self.current_player = 1 - self.current_player
        self.turn_label.setText('Ход красной машинки' if self.current_player == 0 else 'Ход синей машинки')
        self.turn_label.setStyleSheet("color: red;font-size: 25px" if self.current_player == 0 else "color: blue;font-size: 25px")
        self.speed_changed = False

        if self.first_turn and self.player_positions[self.current_player] == self.start_positions[self.current_player]:
            self.increase_speed_button.setEnabled(False)
        else:
            self.increase_speed_button.setEnabled(True)

    def reset_position(self):
        self.player_positions[self.current_player] = self.start_positions[self.current_player]
        self.speeds[self.current_player] = 1

    def reset_game(self):
        self.player_positions = self.start_positions.copy()
        self.speeds = [1, 1]
        self.current_player = 0
        self.winner_label.setText('')
        self.update_grid()
        self.speed_labels[0].setText(f'Speed: {self.speeds[0]}')
        self.speed_labels[1].setText(f'Speed: {self.speeds[1]}')
        self.turn_label.setText('Победа')
        self.first_turn = True
        self.increase_speed_button.setEnabled(False)

    def increase_speed(self):
        if not self.speed_changed and not (self.first_turn and self.player_positions[self.current_player] == self.start_positions[self.current_player]):
            self.speeds[self.current_player] += 1
            self.speed_labels[self.current_player].setText(f'Speed: {self.speeds[self.current_player]}')
            self.speed_changed = True

    def decrease_speed(self):
        if self.speeds[self.current_player] > 1 and not self.speed_changed:
            self.speeds[self.current_player] -= 1
            self.speed_labels[self.current_player].setText(f'Speed: {self.speeds[self.current_player]}')
            self.speed_changed = True


from PyQt6.QtWidgets import QWidget, QVBoxLayout, QGridLayout, QLabel, QPushButton, QApplication, QHBoxLayout
from PyQt6.QtCore import Qt


class Track1Window(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.speed_changed = False
        self.first_turn = True

    def initUI(self):
        self.setStyleSheet("background-color: #ADD8E6;")
        self.setWindowTitle('Трасса 1')
        self.setGeometry(0, 0, 800, 600)
        self.center()

        self.grid_size = 20
        self.track = self.create_track()
        self.start_positions = [(self.grid_size - 2, 4), (self.grid_size - 2, 2)]
        self.player_positions = self.start_positions.copy()
        self.speeds = [1, 1]
        self.current_player = 0

        self.layout = QVBoxLayout()
        self.grid_layout = QGridLayout()
        self.grid_labels = [[QLabel() for _ in range(self.grid_size)] for _ in range(self.grid_size)]
        self.update_grid()

        self.button_layout = QHBoxLayout()
        self.create_buttons()

        self.speed_labels = [QLabel(f'Speed: {self.speeds[0]}'), QLabel(f'Speed: {self.speeds[1]}')]
        self.speed_labels[0].setStyleSheet("color: red; font-size: 25px")
        self.speed_labels[1].setStyleSheet("color: blue; font-size: 25px")

        self.turn_label = QLabel('Ход красной машинки')
        self.turn_label.setStyleSheet("color: red; font-size: 25px;")

        self.winner_label = QLabel('')
        self.winner_label.setStyleSheet("color: green; font-size: 24px;")
        self.winner_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.layout.addLayout(self.grid_layout)
        self.layout.addLayout(self.button_layout)
        self.layout.addWidget(self.turn_label, alignment=Qt.AlignmentFlag.AlignCenter)
        self.layout.addWidget(self.speed_labels[0], alignment=Qt.AlignmentFlag.AlignLeft)
        self.layout.addWidget(self.speed_labels[1], alignment=Qt.AlignmentFlag.AlignRight)
        self.layout.addWidget(self.winner_label, alignment=Qt.AlignmentFlag.AlignCenter)

        back_btn = QPushButton('В меню', self)
        back_btn.setFixedSize(150, 40)
        back_btn.setStyleSheet("background-color: #808080; color: white;font-size: 25px")
        back_btn.clicked.connect(self.back_to_menu)
        self.layout.addWidget(back_btn, alignment=Qt.AlignmentFlag.AlignCenter)

        self.setLayout(self.layout)

    def create_buttons(self):
        directions = [("←", 0, -1), ("↑", -1, 0), ("↓", 1, 0), ("→", 0, 1),
                      ("⭩", 1, -1), ("⭨", 1, 1), ("⭦", -1, -1), ("⭧", -1, 1)]
        for text, dx, dy in directions:
            button = QPushButton(text)
            button.setFixedSize(40, 40)
            button.setStyleSheet("background-color: yellow; font-size: 40px;")
            button.clicked.connect(lambda _, dx=dx, dy=dy: self.move_car(dx, dy))
            self.button_layout.addWidget(button)

        self.increase_speed_button = QPushButton('➕')
        self.increase_speed_button.setFixedSize(50, 30)
        self.increase_speed_button.setStyleSheet("background-color: green ; font-size: 25px")
        self.increase_speed_button.clicked.connect(self.increase_speed)
        self.increase_speed_button.setEnabled(False)

        self.decrease_speed_button = QPushButton('➖')
        self.decrease_speed_button.setFixedSize(50, 30)
        self.decrease_speed_button.setStyleSheet("background-color: red; font-size: 25px")
        self.decrease_speed_button.clicked.connect(self.decrease_speed)

        self.button_layout.addWidget(self.increase_speed_button)
        self.button_layout.addWidget(self.decrease_speed_button)

    def back_to_menu(self):
        self.close()
        global game_menu
        game_menu.show()

    def center(self):
        frameGm = self.frameGeometry()
        centerPoint = QApplication.primaryScreen().availableGeometry().center()
        frameGm.moveCenter(centerPoint)
        self.move(frameGm.topLeft())

    def create_track(self):
        track = [[0 for _ in range(self.grid_size)] for _ in range(self.grid_size)]
        for i in range(self.grid_size):
            track[0][i] = 1
            track[self.grid_size - 1][i] = 1
            track[i][0] = 1
            track[i][self.grid_size - 1] = 1

        for i in range(3, self.grid_size - 3):
            track[i][3] = 3
            track[i][self.grid_size - 3] = 3

        for j in range(2, self.grid_size - 3):
            track[2][j] = 3
            track[self.grid_size - 3][j] = 3

        for i in range(6, self.grid_size - 6):
            track[6][i] = 1
            track[7][i] = 1
            track[8][i] = 1
            track[9][i] = 1
            track[10][i] = 1
            track[11][i] = 1
            track[12][i] = 1
            track[13][i] = 1
            track[14][i] = 1
            track[15][i] = 1
            track[16][i] = 1
            track[17][i] = 1
            track[18][i] = 1

        for i in range(6, self.grid_size - 6):
            track[7][j] = 1
            track[9][j] = 1
            track[8][j] = 1
            track[10][j] = 1
            track[11][j] = 1
            track[12][j] = 1
            track[6][j] = 1
            track[5][j] = 1
            track[1][j] = 1
            track[4][j] = 1
            track[2][j] = 1
            track[3][j] = 1
            track[15][j] = 1
            track[16][j] = 1
            track[17][j] = 1
            track[18][j] = 1

            track[self.grid_size - 7][i] = 1

            track[i][self.grid_size - 7] = 1

        for j in range(1, 2):
            track[i][self.grid_size - 21] = 4

        return track

    def update_grid(self):
        for i in range(self.grid_size):
            for j in range(self.grid_size):
                if self.track[i][j] == 1:
                    self.grid_labels[i][j].setStyleSheet("background-color: black;")
                elif self.track[i][j] == 4:
                    self.grid_labels[i][j].setStyleSheet("background-color: green;")
                elif (i, j) in self.player_positions:
                    index = self.player_positions.index((i, j))
                    self.grid_labels[i][j].setStyleSheet(
                        "background-color: red;" if index == 0 else "background-color: blue;")
                else:
                    self.grid_labels[i][j].setStyleSheet("background-color: white;")
                self.grid_layout.addWidget(self.grid_labels[i][j], i, j)

    def move_car(self, dx, dy):
        x, y = self.player_positions[self.current_player]
        speed = self.speeds[self.current_player]
        new_x, new_y = x + dx * speed, y + dy * speed

        if 0 <= new_x < self.grid_size and 0 <= new_y < self.grid_size:
            if self.track[new_x][new_y] in (0, 3):
                self.player_positions[self.current_player] = (new_x, new_y)
            elif self.track[new_x][new_y] == 1:
                self.reset_position()
            elif self.track[new_x][new_y] == 4:
                self.winner_label.setText(f'Победила {"красная" if self.current_player == 0 else "синяя"} машинка!')
                self.reset_game()
                return
        else:
            self.reset_position()

        self.update_grid()
        self.speed_labels[self.current_player].setText(f'Speed: {self.speeds[self.current_player]}')
        self.current_player = 1 - self.current_player
        self.turn_label.setText('Ход красной машинки' if self.current_player == 0 else 'Ход синей машинки')
        self.turn_label.setStyleSheet(
            "color: red; font-size: 25px;" if self.current_player == 0 else "color: blue; font-size: 25px;")
        self.speed_changed = False

        if self.first_turn and self.player_positions[self.current_player] == self.start_positions[self.current_player]:
            self.increase_speed_button.setEnabled(False)
        else:
            self.increase_speed_button.setEnabled(True)

        if not self.first_turn:
            self.increase_speed_button.setEnabled(True)

    def reset_position(self):
        self.player_positions[self.current_player] = self.start_positions[self.current_player]
        self.speeds[self.current_player] = 1

    def reset_game(self):
        self.player_positions = self.start_positions.copy()
        self.speeds = [1, 1]
        self.current_player = 0
        self.winner_label.setText('')
        self.update_grid()
        self.speed_labels[0].setText(f'Speed: {self.speeds[0]}')
        self.speed_labels[1].setText(f'Speed: {self.speeds[1]}')
        self.turn_label.setText('Победа')

        self.first_turn = True
        self.increase_speed_button.setEnabled(False)

    def increase_speed(self):
        if not self.speed_changed and not (
                self.first_turn and self.player_positions[self.current_player] == self.start_positions[
            self.current_player]):
            self.speeds[self.current_player] += 1
            self.speed_labels[self.current_player].setText(f'Speed: {self.speeds[self.current_player]}')
            self.speed_changed = True

    def decrease_speed(self):
        if self.speeds[self.current_player] > 1 and not self.speed_changed:
            self.speeds[self.current_player] -= 1
            self.speed_labels[self.current_player].setText(f'Speed: {self.speeds[self.current_player]}')
            self.speed_changed = True


class RulesWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setStyleSheet("background-color: #87CEEB;")
        self.setWindowTitle('Правила')
        self.setGeometry(0, 0, 800, 600)
        self.center()

        rules_label = QLabel("Правила игры", self)
        rules_label.setStyleSheet("font-size: 18px; color: black;")
        rules_label.move(350, 30)

        rules1_label = QLabel("⦿Главная цель игры: приехать первым на финиш (финиш- это зеленая клетка на трассе).", self)
        rules1_label.setStyleSheet("font-size: 15px; color: black;")
        rules1_label.move(30, 100)

        rules2_label = QLabel("⦿Машинки передвигаются по очереди с помощью кнопок управления, которые выделены желтым цветом.", self)
        rules2_label.setStyleSheet("font-size: 15px; color: black;")
        rules2_label.move(30, 170)

        rules2_label = QLabel("⦿В первом ходу машинки начинают движение со скоростью 1 клетка.", self)
        rules2_label.setStyleSheet("font-size: 15px; color: black;")
        rules2_label.move(30, 240)

        rules2_label = QLabel("⦿Если машинка врезается в ограждение (ограждение- черная клетка на трассе), то возвращается на старт.", self)
        rules2_label.setStyleSheet("font-size: 15px; color: black;")
        rules2_label.move(30, 310)

        rules2_label = QLabel("⦿Увелечение скорости просходит при нажатии на зеленую кнопку, а уменьшение на красную.", self)
        rules2_label.setStyleSheet("font-size: 15px; color: black;")
        rules2_label.move(30, 380)

        back_btn = QPushButton('Назад', self)
        back_btn.move(320, 500)
        back_btn.setFixedSize(170, 40)
        back_btn.setStyleSheet("background-color: #FF0000; color: white;font-size: 40px;")
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
        word_label.setStyleSheet("font-size: 40px; color: black;")

        play_btn = QPushButton('Играть', self)
        play_btn.setFixedSize(200, 40)
        play_btn.setStyleSheet("background-color: #32CD32; color: white;  font-size: 35px ")


        rules_btn = QPushButton('Правила', self)
        rules_btn.setFixedSize(200, 40)
        rules_btn.setStyleSheet("background-color: #ff9763; color: white;font-size: 35px")

        exit_btn = QPushButton('Выход', self)
        exit_btn.setFixedSize(200, 40)
        exit_btn.setStyleSheet("background-color: #FF0000; color: white;font-size: 35px")

        play_btn.move(300, 225)
        word_label.move(235, 45)
        rules_btn.move(300, 280)
        exit_btn.move(300, 330)

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

