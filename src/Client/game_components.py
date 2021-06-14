import logging
import pathlib

from PyQt5.QtCore import pyqtSlot
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QWidget, QLabel

from src.Client.prmotion_window import Promotion

# LOGGING CONFIG
logging.basicConfig(format='%(asctime)s :: %(levelname)s :: %(message)s', level=logging.DEBUG)

BOARD_SIZE = 800
FIELD_SIZE = int(BOARD_SIZE / 8)

FIELD_LETTERS = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H']


class BoardField(QLabel):
    def __init__(self, parent, row, col, color, not_reversed):
        super().__init__(parent)
        self.__label = f'{FIELD_LETTERS[-col - 1]}{row + 1}' if not not_reversed else f'{FIELD_LETTERS[col]}{8 - row}'
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

    def reversed(self, white_bottom_black_top):
        self.__not_reversed = white_bottom_black_top
        self.__label = f'{FIELD_LETTERS[-self.__col - 1]}{self.__row + 1}' if not self.__not_reversed else f'{FIELD_LETTERS[self.__col]}{8 - self.__row}'

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

    def has_piece(self):
        return self.__piece is not None

    def add_piece(self, piece: 'Piece'):
        if self.__piece is None:
            self.__piece = piece
            piece.set_field(self)
            return True
        return False

    def remove_piece(self):
        self.__piece.hide()
        self.__piece = None

    def do_pos_belongs_to_field(self, x, y):
        return self.__x_pos <= x < self.__x_pos + FIELD_SIZE and self.__y_pos <= y < self.__y_pos + FIELD_SIZE

    def __str__(self):
        return f'Field: [{self.__row}, {self.__col}] color {"black" if self.__color else "white"}'


class Piece(QLabel):
    def __init__(self, parent: 'Chessboard', is_white: bool, type: str):
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

    def change_type(self, promotion):
        self.__type = promotion
        path = pathlib.Path(f'Pieces/Chess_{self.__type}{"lt" if self.__is_white else "dt"}60.png')
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
        if self.__field is not None and self.__field.has_piece():
            self.__field.remove_piece()
        self.__field = field
        self.setGeometry(int(field.x_pos),
                         int(field.y_pos),
                         int(FIELD_SIZE),
                         int(FIELD_SIZE))
        self.show()

    def release_field(self):
        self.__field = None

    def mouseMoveEvent(self, event):
        if self.__parent.white_bottom_black_top == self.is_white and self.__parent.is_player_turn:
            pos_x, pos_y = int(event.windowPos().x() - FIELD_SIZE * 0.6), int(
                event.windowPos().y() - FIELD_SIZE)
            self.raise_()
            self.move(pos_x, pos_y)

    def mouseReleaseEvent(self, event):
        if self.__parent.white_bottom_black_top == self.is_white and self.__parent.is_player_turn:
            pos_x, pos_y = int(event.windowPos().x()), int(event.windowPos().y() - FIELD_SIZE / 2)
            fields = self.__parent.fields
            moved = False
            if self.__parent.get_parent().in_game:
                for row in fields:
                    if moved:
                        break
                    for field in row:
                        if moved:
                            break
                        if field.do_pos_belongs_to_field(pos_x, pos_y):
                            if field == self.__field:
                                break
                            logging.debug(f'Move {self.__field.label} -> {field.label}')
                            move_src = self.__field.label
                            move_dst = field.label
                            move_src_field = self.__field
                            move_dst_field = field
                            is_promotion = False
                            if self.__type == 'p' and (move_dst[1] == '8' or move_dst[1] == '1'):
                                promotion = Promotion("white" if self.is_white else "black")
                                promotion.exec_()
                                while promotion.piece == "X":
                                    if promotion.isHidden():
                                        promotion.piece = "Q"
                                    if not self.__parent.get_parent().in_game:
                                        promotion.close()
                                        return
                                promotion_to_piece = promotion.piece
                                promotion.close()
                                is_promotion = True
                                msg = {'request_type': 'player_move',
                                       'move': f'{self.__field.label}{field.label}{promotion_to_piece}'}
                            else:
                                msg = {'request_type': 'player_move', 'move': f'{self.__field.label}{field.label}'}

                            self.__parent.parent.client.send_to_socket(msg)
                            self.__parent.parent.client.move_lock.acquire()
                            while self.__parent.parent.client.move_lock.locked():
                                pass
                            if not self.__parent.parent.client.last_move_valid:
                                self.setGeometry(int(self.__field.x_pos),
                                                 int(self.__field.y_pos),
                                                 int(FIELD_SIZE),
                                                 int(FIELD_SIZE))
                                return
                            moved = True

                            if is_promotion:
                                self.change_type(promotion=promotion_to_piece.lower())
                            if self.__type == "p" and move_dst_field.piece is None and move_src_field.col - move_dst_field.col != 0:
                                self.__parent.fields[move_dst_field.row + 1][move_dst_field.col].remove_piece()
                            self.__parent.is_white_move = not self.__parent.is_white_move
                            self.__parent.is_player_turn = False
                            self.__parent.castle(move_src, move_dst)
                            if field.has_piece():
                                field.remove_piece()
                            field.add_piece(self)

            if not moved:
                self.setGeometry(int(self.__field.x_pos),
                                 int(self.__field.y_pos),
                                 int(FIELD_SIZE),
                                 int(FIELD_SIZE))


class Chessboard(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.__parent = parent
        self.__white_bottom_black_top = True
        self.__is_player_turn = self.__white_bottom_black_top
        self.setup()
        self.__fields = self.__set_fields()
        self.__set_fields()
        self.is_white_move = True
        self.reset_pieces()

    def get_parent(self):
        return self.__parent

    @property
    def fields(self):
        return self.__fields

    @property
    def parent(self):
        return self.__parent

    @property
    def white_bottom_black_top(self):
        return self.__white_bottom_black_top

    @property
    def is_player_turn(self):
        return self.__is_player_turn

    @is_player_turn.setter
    def is_player_turn(self, val):
        self.__is_player_turn = val

    def castle(self, move_src: str, move_dst: str):
        dst_field = self.find_field(move_src)
        dst_piece = dst_field.piece
        if dst_piece.type != 'k':
            return
        castling_moves = [('E1', 'G1'), ('E1', 'C1'), ('E8', 'G8'), ('E8', 'C8')]
        rook_moves = [('H1', 'F1'), ('A1', 'D1'), ('H8', 'F8'), ('A8', 'D8')]
        if (move_src, move_dst) in castling_moves:
            index = castling_moves.index((move_src, move_dst))
            rook_move = rook_moves[index]
            rook_src = self.find_field(rook_move[0])
            rook_dst = self.find_field(rook_move[1])
            rook = rook_src.piece
            rook_src.remove_piece()
            rook_dst.add_piece(rook)

    def change_sides(self, white_bottom_black_top):
        self.__white_bottom_black_top = white_bottom_black_top
        for row in range(8):
            for col in range(8):
                self.__fields[row][col].reversed(white_bottom_black_top)

    def find_field(self, label: str):
        field_letter, field_num = label
        col = FIELD_LETTERS.index(field_letter) if self.__white_bottom_black_top else 7 - FIELD_LETTERS.index(
            field_letter)
        row = 7 - (int(field_num) - 1) if self.__white_bottom_black_top else int(field_num) - 1

        return self.__fields[row][col]

    def setup(self):
        self.setGeometry(500, 500, BOARD_SIZE, BOARD_SIZE)
        self.show()

    def play_move(self, src: str, dst: str, promotion=None):
        src_field = self.find_field(src)
        dst_field = self.find_field(dst)
        self.castle(src, dst)
        if src_field.piece.type == "p" and dst_field.piece is None and src_field.col - dst_field.col != 0:
            self.__fields[dst_field.row - 1][dst_field.col].remove_piece()
        if dst_field.has_piece():
            dst_field.remove_piece()
        dst_field.add_piece(src_field.piece)
        self.__is_player_turn = True
        self.is_white_move = not self.is_white_move
        if promotion is not None:
            dst_field.piece.change_type(promotion.lower())

    def __set_fields(self):
        fields = []
        for row in range(8):
            rows = []
            for col in range(8):
                rows.append(BoardField(self, row, col, ((col + row) % 2 == 1), self.__white_bottom_black_top))
            fields.append(rows)

        return fields

    @pyqtSlot()
    def reset_pieces(self):
        for i in range(8):
            for j in range(8):
                if self.__fields[i][j].has_piece():
                    self.__fields[i][j].remove_piece()
        pieces = ['rnbqkbnr', 'pppppppp']
        if not self.__white_bottom_black_top:
            pieces[0] = pieces[0][::-1]
        for row_num, row in zip(range(0, 2), pieces):
            for col_num, type in zip(range(8), row):
                self.__fields[row_num][col_num].add_piece(Piece(self, not self.__white_bottom_black_top, type))
        pieces.reverse()
        for row_num, row in zip(range(6, 8), pieces):
            for col_num, type in zip(range(8), row):
                self.__fields[row_num][col_num].add_piece(Piece(self, self.__white_bottom_black_top, type))

        self.__is_player_turn = self.__white_bottom_black_top
        self.is_white_move = True
