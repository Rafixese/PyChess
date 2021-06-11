from stockfish.models import Stockfish
import platform
import pathlib
import os
from time import sleep

class BotGame:
    def __init__(self, client, client_color, elo):
        self.client = client
        self.client_color = client_color
        self.elo = int(elo)
        print('dupa')
        msg = {
            'request_type': 'start_bot_game',
            'opponent': f'BOT({self.elo})',
        }
        self.client.send_to_socket(msg)
        self.moves = []

        system = platform.system()
        if system == 'Linux':
            path = pathlib.Path(os.getcwd()).joinpath('stockfish_13_linux_x64_bmi2/stockfish_13_linux_x64_bmi2')
        else:
            path = pathlib.Path(os.getcwd()).joinpath('stockfish_13_win_x64_bmi2/stockfish_13_win_x64_bmi2.exe')
        self.stockfish = Stockfish(str(path))
        self.stockfish.set_elo_rating(self.elo)

        print(self.stockfish.get_board_visual())
        if self.client_color == "black":
            sleep(2)
            self.make_bot_move()


    def is_client_in_game(self, client):
        return self.client == client

    def check_move(self, move: str):
        move = move.lower()
        return self.stockfish.is_move_correct(move)

    def make_move(self, move: str):
        move = move.lower()
        self.moves.append(move)
        self.stockfish.set_position(self.moves)
        print(self.stockfish.get_board_visual())
        self.make_bot_move()

    def make_bot_move(self):
        self.stockfish.set_position(self.moves)
        self.stockfish.set_elo_rating(self.elo)
        self.stockfish.set_depth(int(self.elo/150))
        best_move = self.stockfish.get_best_move_time(self.elo)
        print(best_move)
        self.moves.append(best_move)
        self.stockfish.set_position(self.moves)
        print(self.stockfish.get_board_visual())
        self.client.send_to_socket({'request_type': 'player_move', 'move': best_move.upper()})
