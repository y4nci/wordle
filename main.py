import sys
from lib import wordle
from PyQt5 import QtWidgets
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QMessageBox


class Window(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.guess_button = None
        self.word = wordle.random_word()
        self.buttons = list()
        self.output = list()
        self.num = 1
        self.init_ui()
        self.msg = QMessageBox()

    def init_ui(self):
        main_layout = QtWidgets.QVBoxLayout()
        grid = QtWidgets.QGridLayout()
        self.guess_button = QtWidgets.QPushButton("guess")
        stat_button = QtWidgets.QPushButton("show stats")
        newgame_button = QtWidgets.QPushButton("new game")

        positions = [(i, j) for i in range(6) for j in range(5)]

        for position in positions:
            button = QtWidgets.QLineEdit()
            button.setMaxLength(1)
            button.setAlignment(Qt.AlignCenter)
            button.textChanged.connect(self.next)
            grid.addWidget(button, *position)
            self.buttons.append(button)

        for i in range(self.num * 5, 30):
            self.buttons[i].setReadOnly(True)

        self.guess_button.clicked.connect(self.guess)
        stat_button.clicked.connect(self.show_stats)
        newgame_button.clicked.connect(self.new_game)
        main_layout.addLayout(grid)
        main_layout.addWidget(self.guess_button)
        main_layout.addWidget(stat_button)
        main_layout.addWidget(newgame_button)

        central = QtWidgets.QWidget(self)
        self.setCentralWidget(central)
        central.setLayout(main_layout)

        self.setGeometry(200, 150, 350, 500)
        self.setWindowTitle("Wordle")
        self.show()

    def next(self):
        self.focusNextPrevChild(True)

    def guess(self):
        letters = list()
        sum = 0

        for i in range((self.num - 1) * 5, self.num * 5):
            self.buttons[i].setReadOnly(True)
            if i < 25: self.buttons[i + 5].setReadOnly(False)
            letters.append(self.buttons[i].text() + (self.buttons[i].text() == "") * ".")

        self.output = wordle.evaluate_guess(letters, self.word)

        for i in range(5):
            sum += self.output[i]

            if self.output[i] == 2:
                self.buttons[(self.num - 1) * 5 + i].setStyleSheet("QLineEdit"
                                                                   "{"
                                                                   "background : lightgreen;"
                                                                   "}")

            elif self.output[i] == 1:
                self.buttons[(self.num - 1) * 5 + i].setStyleSheet("QLineEdit"
                                                                   "{"
                                                                   "background : lightblue;"
                                                                   "}")

            else:
                self.buttons[(self.num - 1) * 5 + i].setStyleSheet("QLineEdit"
                                                                   "{"
                                                                   "background : grey;"
                                                                   "}")

        self.num += 1

        if sum == 10:
            restart_button = QtWidgets.QPushButton("Restart")
            self.msg.setWindowTitle("Correct!")
            self.msg.setText(f"The word was {self.word}")
            self.msg.setDefaultButton(restart_button)
            self.msg.setIcon(QMessageBox.Information)
            # self.msg.buttonClicked.connect(self.restart)
            self.msg.show()
            self.restart()

        elif self.num == 7:
            restart_button = QtWidgets.QPushButton("Restart")
            self.msg.setWindowTitle("Wrong!")
            self.msg.setText(f"The word was {self.word}")
            self.msg.setDefaultButton(restart_button)
            self.msg.setIcon(QMessageBox.Critical)
            # self.msg.buttonClicked.connect(self.restart)
            self.msg.show()
            self.restart()

    def show_stats(self):
        self.buttons = list()
        self.num = 1
        self.word = wordle.random_word()
        stats = QtWidgets.QLabel(wordle.fetch_data())
        back_button = QtWidgets.QPushButton("back")
        stat_layout = QtWidgets.QVBoxLayout()
        back_button.clicked.connect(self.init_ui)
        stat_layout.addWidget(stats)
        stat_layout.addWidget(back_button)

        central = QtWidgets.QWidget(self)
        self.setCentralWidget(central)
        central.setLayout(stat_layout)

        self.show()

    def new_game(self):
        self.num = 1
        self.word = wordle.random_word()

        for i in range(30):
            button = self.buttons[i]

            if i < 5:
                button.setReadOnly(False)

            else:
                button.setReadOnly(True)

            button.clear()
            button.setStyleSheet("QLineEdit"
                                 "{"
                                 "background : white;"
                                 "}")

        self.guess_button.setEnabled(True)

        #{"total guesses": 42, "total games": 8, "total successful": 3, "total unsuccessful": 5, "success rate": "%37.5", "correct in": [0, 0, 2, 0, 0, 1]}

    def restart(self):
        if self.num == 7:
            if self.output == [2, 2, 2, 2, 2]:
                wordle.update_data(self.num - 1, True)

            else:
                wordle.update_data(-1, False)

        else:
            wordle.update_data(self.num - 1, True)

        self.guess_button.setEnabled(False)


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)

    window = Window()

    sys.exit(app.exec())
