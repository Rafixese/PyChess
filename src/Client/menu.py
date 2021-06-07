from PyQt5.QtGui import QFont
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QMessageBox, QPushButton, QLineEdit, QMainWindow, QGroupBox, \
    QGridLayout, QVBoxLayout, QDialog, QHBoxLayout
import sys
class Window(QDialog):
    def __init__(self):
        super().__init__()
        self.title = "PyChess"
        self.top = 0
        self.left = 200
        self.width = 1400
        self.height = 1000
        self.login = True
        self.Init_window()


    def Init_window(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.top, self.left, self.width, self.height)
        self.Grid()
        self.show()

    def Grid(self):
        layout = QGridLayout()
        # layout.setSpacing(50)
        self.setLayout(layout)
        groupbox = QGroupBox("GroupBox Example")
        layout.addWidget(groupbox,0,10,)
        layout.addWidget(QPushButton("1"), 0, 0,9,10)
        layout.addWidget(QPushButton("1"), 1, 0,9,10)
        vbox = QVBoxLayout()
        groupbox.setLayout(vbox)
        vbox.addWidget(QPushButton('1'))



if __name__ == "__main__":
    App = QApplication(sys.argv)
    window = Window()
    sys.exit(App.exec())