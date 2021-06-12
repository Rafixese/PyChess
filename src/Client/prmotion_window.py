import threading

from PyQt5.QtGui import QFont, QIcon
from PyQt5 import QtWidgets
from PyQt5.QtCore import Qt, pyqtSlot, QSize
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QMessageBox, QPushButton, QLineEdit, QMainWindow, QGroupBox, \
    QGridLayout, QVBoxLayout, QDialog, QHBoxLayout, QListWidget, QScrollBar, QSlider
import sys
from src.Client.server_client import Client


class Promotion(QDialog):
    def __init__(self, color):
        super().__init__()
        self.title = "Promotion"
        self.width = 420
        self.height = 200
        self.color = color
        self.queen = QPushButton(self)
        self.rook = QPushButton(self)
        self.bishop = QPushButton(self)
        self.knight = QPushButton(self)
        self.text = QLabel(self)
        self.piece = "X"
        self.Init_window()

    def Init_window(self):
        self.setWindowTitle(self.title)
        self.setFixedSize(self.width, self.height)

        self.text.setText("Choose what you want to be promote into")
        self.text.setGeometry(25, 0, 5000, 100)
        self.text.setFont(QFont('Arial', 15))

        if self.color == "black":
            self.queen.setIcon(QIcon('Pieces/Chess_qdt60.png'))
            self.rook.setIcon(QIcon('Pieces/Chess_rdt60.png'))
            self.knight.setIcon(QIcon('Pieces/Chess_ndt60.png'))
            self.bishop.setIcon(QIcon('Pieces/Chess_bdt60.png'))
        else:
            self.queen.setIcon(QIcon('Pieces/Chess_qlt60.png'))
            self.rook.setIcon(QIcon('Pieces/Chess_rlt60.png'))
            self.knight.setIcon(QIcon('Pieces/Chess_nlt60.png'))
            self.bishop.setIcon(QIcon('Pieces/Chess_blt60.png'))

        self.queen.setGeometry(20, 105, 80, 80)
        self.queen.setIconSize(self.queen.size())
        self.queen.clicked.connect(self.queen_click)

        self.rook.setGeometry(120, 105, 80, 80)
        self.rook.setIconSize(self.rook.size())
        self.rook.clicked.connect(self.rook_click)

        self.knight.setGeometry(220, 105, 80, 80)
        self.knight.setIconSize(self.knight.size())
        self.knight.clicked.connect(self.knight_click)

        self.bishop.setGeometry(320, 105, 80, 80)
        self.bishop.setIconSize(self.bishop.size())
        self.bishop.clicked.connect(self.bishop_click)

        self.show()

    def queen_click(self):
        self.piece = "Q"
        self.close()
    def rook_click(self):
        self.piece = "R"
        self.close()
    def bishop_click(self):
        self.piece = "B"
        self.close()
    def knight_click(self):
        self.piece = "N"
        self.close()

if __name__ == "__main__":
    App = QApplication(sys.argv)
    window = Promotion("white")
    sys.exit(App.exec())
