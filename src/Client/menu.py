from PyQt5.QtGui import QFont
from PyQt5 import QtWidgets
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QMessageBox, QPushButton, QLineEdit, QMainWindow, QGroupBox, \
    QGridLayout, QVBoxLayout, QDialog, QHBoxLayout, QListWidget, QScrollBar, QSlider
import sys
from src.Client.server_client import Client

class Menu(QDialog):
    def __init__(self,client):
        super().__init__()
        self.title = "PyChess"
        self.top = 50
        self.left = 200
        self.width = 1400
        self.height = 1000
        self.login = True
        self.white = True
        self.Init_window()
        self.Client = client

    def Init_window(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
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
        layout.addWidget(QPushButton("Miejsce na szachownice"), 0, 0, 9, 10)

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
        vbox.addWidget(self.dif, 0, 0,1,2)
        vbox.addWidget(self.slider, 1, 0, 1, 2)
        self.elo = QLabel("1000 ")
        self.elo.setFont(QFont('Arial', 20))
        vbox.addWidget(self.elo, 1, 3, 1, 1)
        label = QLabel("Select color of pieces")
        label.setFont(QFont('Arial', 20))
        vbox.addWidget(label, 2, 0,1,2)
        self.w = QPushButton("White")
        self.w.setStyleSheet("Background-color: grey")
        self.w.clicked.connect(self.Switch_color_b_w)
        self.b = QPushButton("Black")
        self.b.clicked.connect(self.Switch_color_w_b)
        self.b.setStyleSheet("Background-color: lightgrey")
        vbox.addWidget(self.w, 3, 0)
        vbox.addWidget(self.b, 3, 1)
        self.play = QPushButton("Play")
        vbox.addWidget(QLabel(),4,0,1,1)
        vbox.addWidget(self.play,5,3,1,1)
        # Gra online
        vbox1 = QVBoxLayout()
        online.setLayout(vbox1)

        vbox1.addWidget(QPushButton('Find opponet'))

        # Donly box z miejscem przygotownym pod chat
        vbox2 = QGridLayout()
        chat.setLayout(vbox2)

        self.list_widget = QListWidget(self)
        self.list_widget.setGeometry(25, 25, 950, 650)
        scroll_bar = QScrollBar(self)
        scroll_bar.setStyleSheet("background : Grey;")
        self.list_widget.setVerticalScrollBar(scroll_bar)

        vbox2.addWidget(self.list_widget, 0, 0, 1, 0)
        vbox2.addWidget(QLineEdit(), 1, 0)
        vbox2.addWidget(QPushButton("Send"), 1, 1)

        # przykladowe wiadomosci dodane
        self.list_widget.addItem("Piesek")
        self.list_widget.addItem("fajny")
        self.list_widget.addItem("to d4 to nieświeże zagranie")
        self.list_widget.addItem("miss click sory")
        self.list_widget.addItem("miss click sory")
        self.list_widget.addItem("miss click sory")
        self.list_widget.addItem("miss click sory")
        self.list_widget.addItem("miss click sory")
        self.list_widget.addItem("miss click sory")

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

if __name__ == "__main__":
    App = QApplication(sys.argv)
    window = Menu(None)
    sys.exit(App.exec())
