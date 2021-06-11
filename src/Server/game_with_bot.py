from stockfish.models import Stockfish
import platform
import pathlib
import os
from time import sleep

class BotGame:
    def __init__(self, client, client_color, elo, parent):
        self.client = client
        self.client_color = client_color
        self.elo = int(elo)
        self.parent = parent
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
        self.check_for_end_game()
        self.make_bot_move()

    def make_bot_move(self):
        self.stockfish.set_position(self.moves)
        self.stockfish.set_skill_level(self.elo)
        self.stockfish.set_depth(self.elo)
        best_move = self.stockfish.get_best_move()
        print(best_move)
        self.moves.append(best_move)
        self.stockfish.set_position(self.moves)
        print(self.stockfish.get_board_visual())
        self.client.send_to_socket({'request_type': 'player_move', 'move': best_move.upper()})
        self.check_for_end_game()

    def check_for_end_game(self):
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
            self.client.send_to_socket(msg)
            self.parent.bot_games.remove(self)
        elif eval['type'] == 'mate' and eval['value'] == 0:
            if fen_color == 'b':
                print('WHITE WINS')
                if self.client_color == 'white':
                    msg = {
                        'request_type': 'win'
                    }
                else:
                    msg = {
                        'request_type': 'lose'
                    }
                self.client.send_to_socket(msg)
            elif fen_color == 'w':
                print('BLACK WINS')
                if self.client_color == 'black':
                    msg = {
                        'request_type': 'win'
                    }
                else:
                    msg = {
                        'request_type': 'lose'
                    }
                self.client.send_to_socket(msg)
            self.parent.bot_games.remove(self)
