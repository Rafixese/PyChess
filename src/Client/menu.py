from PyQt5.QtGui import QFont
from PyQt5 import QtWidgets
from PyQt5.QtCore import Qt, pyqtSlot
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QMessageBox, QPushButton, QLineEdit, QMainWindow, QGroupBox, \
    QGridLayout, QVBoxLayout, QDialog, QHBoxLayout, QListWidget, QScrollBar, QSlider
import sys
from src.Client.game_components import Chessboard
from src.Client.server_client import Client


class Menu(QDialog):
    def __init__(self, client):
        super().__init__()
        self.title = "PyChess"
        self.width = 1200
        self.height = 920
        self.login = True
        self.white = True
        self.client = client
        self.in_game = False
        self.Init_window()

    def Init_window(self):
        self.setWindowTitle(self.title)
        self.setFixedSize(self.width, self.height)
        self.Grid()
        self.show()

    def Grid(self):
        # Umiejscownienie boxów i miejsce na szachownice
        layout = QGridLayout()
        self.setLayout(layout)
        bot = QGroupBox("Play with bot")
        online = QGroupBox("Play online")
        chat = QGroupBox("Chat")
        layout.addWidget(bot, 0, 10, 3, 4)
        layout.addWidget(online, 3, 10, 1, 4)
        layout.addWidget(chat, 4, 10, 5, 4)
        # Miejsce na szachownice starczy podmnieć obiekt guzika Ważne żeby zachować numerki ewentualnie zmienićna 1, 1 9,9 żeby było równo
        self.oponnent_user_name = QLabel('Player spaceholder')
        layout.addWidget(self.oponnent_user_name, 0, 0, 1, 10, alignment=Qt.AlignRight)
        self.chessboard = Chessboard()
        layout.addWidget(self.chessboard, 1, 0, 9, 10)
        self.user_name = QLabel(self.client.get_username())
        layout.addWidget(self.user_name, 10, 0, 1, 10, alignment=Qt.AlignRight)
        layout.setRowStretch(0, 1)
        layout.setRowStretch(2, 10)
        layout.setRowStretch(10, 1)

        # Gra z botem
        vbox = QGridLayout()
        bot.setLayout(vbox)

        self.slider = QSlider(Qt.Horizontal)
        self.slider.setFocusPolicy(Qt.StrongFocus)
        self.slider.setTickPosition(QSlider.TicksBothSides)
        self.slider.setMinimum(300)
        self.slider.setMaximum(3000)
        self.slider.setTickInterval(100)
        self.slider.setValue(1000)
        self.slider.valueChanged.connect(self.Change_elo)

        self.dif = QLabel("Select difficulty")
        self.dif.setFont(QFont('Arial', 20))
        vbox.addWidget(self.dif, 0, 0, 1, 2)
        vbox.addWidget(self.slider, 1, 0, 1, 2)
        self.elo = QLabel("1000 ")
        self.elo.setFont(QFont('Arial', 20))
        vbox.addWidget(self.elo, 1, 3, 1, 1)
        label = QLabel("Select color of pieces")
        label.setFont(QFont('Arial', 20))
        vbox.addWidget(label, 2, 0, 1, 2)
        self.w = QPushButton("White")
        self.w.setStyleSheet("Background-color: grey")
        self.w.clicked.connect(self.Switch_color_b_w)
        self.b = QPushButton("Black")
        self.b.clicked.connect(self.Switch_color_w_b)
        self.b.setStyleSheet("Background-color: lightgrey")
        vbox.addWidget(self.w, 3, 0)
        vbox.addWidget(self.b, 3, 1)
        self.play = QPushButton("Play")
        self.play.clicked.connect(self.Play_with_bot)
        vbox.addWidget(QLabel(), 4, 0, 1, 1)
        vbox.addWidget(self.play, 5, 3, 1, 1)
        # Gra online
        vbox1 = QVBoxLayout()
        online.setLayout(vbox1)

        self.find_button = QPushButton('Find opponet')
        self.find_button.clicked.connect(self.Find_opponent)
        vbox1.addWidget(self.find_button)

        # Donly box z miejscem przygotownym pod chat
        vbox2 = QGridLayout()
        chat.setLayout(vbox2)

        self.list_widget = QListWidget(self)
        self.list_widget.setGeometry(25, 25, 950, 650)
        scroll_bar = QScrollBar(self)
        scroll_bar.setStyleSheet("background : Grey;")
        self.list_widget.setVerticalScrollBar(scroll_bar)

        vbox2.addWidget(self.list_widget, 0, 0, 1, 0)
        self.text_messenge = QLineEdit()
        vbox2.addWidget(self.text_messenge, 1, 0)
        self.send_messenge = QPushButton("Send")
        self.send_messenge.clicked.connect(self.Send_message)
        vbox2.addWidget(self.send_messenge, 1, 1)

        # przykladowe wiadomosci dodane

    def Change_elo(self):
        if self.slider.value() >= 1000:
            self.elo.setText("" + str(self.slider.value()) + " ")
        else:
            self.elo.setText(" " + str(self.slider.value()) + " ")

    def Switch_color_w_b(self):
        if self.white:
            self.w.setStyleSheet("background-color: lightgrey")
            self.b.setStyleSheet("background-color: grey")
            self.white = not self.white

    def Switch_color_b_w(self):
        if not self.white:
            self.b.setStyleSheet("background-color: lightgrey")
            self.w.setStyleSheet("background-color: grey")
            self.white = not self.white

    def Find_opponent(self):
        if self.in_game == False:
            self.client.find_opponent()
            self.in_game = True
            self.list_widget.addItem("SYSTEM: Looking for game")

    def Play_with_bot(self):
        if self.white:
            self.client.play_with_bot("white", self.elo.text())
        else:
            self.client.play_with_bot("black", self.elo.text())

    def Send_message(self):
        if self.text_messenge.text().strip() == "":
            pass
        else:
            self.list_widget.addItem("Ja: " + self.text_messenge.text())
            self.client.send_messenge(self.text_messenge.text())
            self.text_messenge.setText("")

    @pyqtSlot()
    def Win(self):
        self.in_game = False
        QMessageBox.warning(self, "Win", "Congratulation you won game", QMessageBox.Ok)

    def closeEvent(self, event):
        close = QMessageBox()
        close.setText("You wanna close game?")
        close.setStandardButtons(QMessageBox.Yes | QMessageBox.Cancel)
        close = close.exec()

        if close == QMessageBox.Yes:
            event.accept()
            self.client.shut_down()
            self.destroy()
            sys.exit()
        else:
            event.ignore()
