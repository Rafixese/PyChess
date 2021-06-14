import pathlib
import platform
import random

from stockfish.models import Stockfish


class Game_with_Player:
    def __init__(self, client, parent):
        self.__client = client
        self.__client2 = None
        self.moves = []
        self.parent = parent

    def get_client(self):
        return self.__client

    def get_client2(self):
        return self.__client2

    def set_clinet2(self, client2):
        self.__client2 = client2
        self.start_game()

    def check_logout(self, client):
        msg = {
            'request_type': 'win'
        }
        if client == self.__client and self.__client2 != None:
            self.__client2.send_to_socket(msg)
            return True
        if client == self.__client2 and self.__client != None:
            self.__client.send_to_socket(msg)
            return True
        return False

    def check_if_player_in(self, client, mess):
        msg = {
            'request_type': 'message',
            'text': mess,
            'user': client.get_username()
        }
        if client == self.__client:
            self.__client2.send_to_socket(msg)
        elif client == self.__client2:
            self.__client.send_to_socket(msg)

    def check_move(self, move: str):
        move = move.lower()
        return self.stockfish.is_move_correct(move)

    def make_move(self, move: str):
        move = move.lower()
        self.moves.append(move)
        self.stockfish.set_position(self.moves)
        print(self.stockfish.get_board_visual())
        eval = self.stockfish.get_evaluation()
        print(eval)
        top_moves = self.stockfish.get_top_moves(3)
        print(top_moves)
        fen_color = self.stockfish.get_fen_position().split(' ')[1]
        print(fen_color)
        if eval['type'] == 'cp' and eval['value'] == 0 and len(top_moves) == 0:
            print('PAT')
            msg = {
                'request_type': 'stealmate'
            }
            self.__client.send_to_socket(msg)
            self.__client2.send_to_socket(msg)
            self.parent.games.remove(self)
        elif eval['type'] == 'mate' and eval['value'] == 0:
            if fen_color == 'b':
                print('WHITE WINS')
                if self.client_1_color == 'white':
                    self.__client.send_to_socket({'request_type': 'win'})
                    self.__client2.send_to_socket({'request_type': 'lose'})
                else:
                    self.__client.send_to_socket({'request_type': 'lose'})
                    self.__client2.send_to_socket({'request_type': 'win'})
            elif fen_color == 'w':
                print('BLACK WINS')
                if self.client_1_color == 'white':
                    self.__client.send_to_socket({'request_type': 'lose'})
                    self.__client2.send_to_socket({'request_type': 'win'})
                else:
                    self.__client.send_to_socket({'request_type': 'win'})
                    self.__client2.send_to_socket({'request_type': 'lose'})
            self.parent.games.remove(self)

    def start_game(self):
        color = random.randint(0, 1)
        self.client_1_color = 'white' if color else 'black'
        self.client_2_color = 'black' if color else 'white'
        msg = {
            'request_type': 'start_game',
            'opponent': self.__client2.get_username(),
            'color': self.client_1_color
        }
        msg2 = {
            'request_type': 'start_game',
            'opponent': self.__client.get_username(),
            'color': self.client_2_color
        }
        self.moves = []

        system = platform.system()
        if system == 'Linux':
            path = pathlib.Path(os.getcwd()).joinpath('stockfish_13_linux_x64_bmi2/stockfish_13_linux_x64_bmi2')
        else:
            path = pathlib.Path(os.getcwd()).joinpath('stockfish_13_win_x64_bmi2/stockfish_13_win_x64_bmi2.exe')
        self.stockfish = Stockfish(str(path))

        print(self.stockfish.get_board_visual())
        self.__client.send_to_socket(msg)
        self.__client2.send_to_socket(msg2)

        print("started")
