from PyQt5.QtGui import QFont, QPixmap
from PyQt5 import QtWidgets
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QMessageBox, QPushButton, QLineEdit, QMainWindow, QGroupBox, \
    QGridLayout, QVBoxLayout, QDialog, QHBoxLayout, QListWidget, QScrollBar, QSlider

import pathlib

BOARD_SIZE = 800
FIELD_SIZE = int(BOARD_SIZE / 8)

FIELD_LETTERS = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H']


class BoardField(QLabel):
    def __init__(self, parent, row, col, color, not_reversed):
        super().__init__(parent)
        self.__label = f'{FIELD_LETTERS[-col-1]}{row+1}' if not not_reversed else f'{FIELD_LETTERS[col]}{8-row}'
        self.__parent = parent
        self.__row = row
        self.__col = col
        self.__color = color
        self.__not_reversed = not_reversed
        self.__x_pos = FIELD_SIZE * col
        self.__y_pos = FIELD_SIZE * row
        self.__piece = None
        self.setGeometry(self.__x_pos, self.__y_pos, FIELD_SIZE, FIELD_SIZE)
        if self.__color:
            self.setStyleSheet("background-color: #A2916B")
        else:
            self.setStyleSheet("background-color: #FFFFFF")

        self.show()

    @property
    def label(self):
        return self.__label

    @property
    def x_pos(self):
        return self.__x_pos

    @property
    def y_pos(self):
        return self.__y_pos

    @property
    def color(self):
        return self.__color

    @property
    def row(self):
        return self.__row

    @property
    def col(self):
        return self.__col

    @property
    def piece(self):
        return self.__piece

    def has_checker(self):
        return self.__piece is not None

    def add_piece(self, piece: 'Piece'):
        if self.__piece is None and self.__color:
            self.__piece = piece
            piece.set_field(self)
            return True
        return False

    def remove_piece(self):
        self.__piece = None

    def do_pos_belongs_to_field(self, x, y):
        return self.__x_pos <= x < self.__x_pos + FIELD_SIZE and self.__y_pos <= y < self.__y_pos + FIELD_SIZE

    def __str__(self):
        return f'Field: [{self.__row}, {self.__col}] color {"black" if self.__color else "white"}'


class Piece(QLabel):
    def __init__(self, parent, is_white: bool, type: str):
        super().__init__(parent)
        self.__fen = type.upper() if is_white else type
        self.__parent = parent
        self.__field = None
        self.__is_white = is_white
        self.__type = type
        path = pathlib.Path(f'Pieces/Chess_{type}{"lt" if is_white else "dt"}60.png')
        pixmap = QPixmap(str(path)).scaledToWidth(100)
        self.setPixmap(pixmap)
        self.show()

    @property
    def is_white(self):
        return self.__is_white

    @property
    def type(self):
        return self.__type

    def set_field(self, field):
        if self.__field is not None:
            self.__field.remove_piece()
        self.__field = field
        self.setGeometry(int(field.x_pos + FIELD_SIZE * 0.1),
                         int(field.y_pos + FIELD_SIZE * 0.1),
                         int(FIELD_SIZE * 0.8),
                         int(FIELD_SIZE * 0.8))
        self.show()

    def release_field(self):
        self.__field = None

    def mouseMoveEvent(self, event):
        if self.__parent.is_white_move == self.is_white:
            pos_x, pos_y = int(event.windowPos().x() - FIELD_SIZE * 0.6), int(
                event.windowPos().y() - FIELD_SIZE)
            self.raise_()
            self.move(pos_x, pos_y)

    def mouseReleaseEvent(self, event):
        if self.__parent.is_white_move == self.is_white:
            pos_x, pos_y = int(event.windowPos().x()), int(event.windowPos().y())
            fields = self.__parent.fields


class Chessboard(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.__white_bottom_black_top = True
        self.setup()
        self.__fields = self.set_fields()
        self.set_pieces()
        self.is_white_move = True

    @property
    def fields(self):
        return self.__fields

    def change_sides(self, white_bottom_black_top):
        self.__white_bottom_black_top = white_bottom_black_top
        self.set_fields()

    def find_field(self, row_n, col_n):
        for row in self.__fields:
            for f in row:
                if f.row == row_n and f.col == col_n:
                    return f

    def setup(self):
        self.setGeometry(500, 500, BOARD_SIZE, BOARD_SIZE)
        self.show()

    def set_fields(self):
        fields = []
        for row in range(8):
            rows = []
            for col in range(8):
                rows.append(BoardField(self, row, col, ((col + row) % 2 == 1), self.__white_bottom_black_top))
            fields.append(rows)
        return fields

    def set_pieces(self):
        self.__fields[0][0].add_piece(Piece(self, True, 'p'))
