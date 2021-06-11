from src.Server.server_client import Client
import random
from stockfish.models import Stockfish
import platform
import pathlib
import os
from time import sleep

class Game_with_Player:
    def __init__(self, client):
        self.__client = client
        self.__client2 = None
        self.moves = []

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


    def start_game(self):
        print(1)
        color = random.randint(0, 1)
        msg = {
            'request_type': 'start_game',
            'opponent': self.__client2.get_username(),
            'color': 'white' if color else 'black'
        }
        msg2 = {
            'request_type': 'start_game',
            'opponent': self.__client.get_username(),
            'color': 'black' if color else 'white'
        }
        print(2)
        self.moves = []

        system = platform.system()
        print(3)
        if system == 'Linux':
            path = pathlib.Path(os.getcwd()).joinpath('stockfish_13_linux_x64_bmi2/stockfish_13_linux_x64_bmi2')
        else:
            path = pathlib.Path(os.getcwd()).joinpath('stockfish_13_win_x64_bmi2/stockfish_13_win_x64_bmi2.exe')
        self.stockfish = Stockfish(str(path))
        print(4)

        print(self.stockfish.get_board_visual())
        self.__client.send_to_socket(msg)
        self.__client2.send_to_socket(msg2)

        print(5)
        print("started")
