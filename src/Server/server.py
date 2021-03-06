import logging
import socket
import threading
import time
from json import JSONDecodeError
from time import sleep

from src.Server.database import create_client, auth_client
from src.Server.game_with_bot import BotGame
from src.Server.game_with_player import Game_with_Player
from src.Server.server_client import Client

# LOGGING CONFIG
logging.basicConfig(format='%(asctime)s :: %(levelname)s :: %(message)s', level=logging.DEBUG)

# SERVER CONFIG
HOST = 'localhost'
PORT = 8888


class Server:
    def __init__(self):
        # SOCKET SETUP
        self.__server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.__server_socket.bind((HOST, PORT))
        self.__server_socket.listen(9999)
        self.__clients = []
        self.__is_someone_waiting = False
        self.games = []
        self.bot_games = []
        threading.Thread(target=self.__accept_loop).start()

    def __accept_loop(self):
        logging.debug('Start of __accept_loop in Server')
        while True:
            client_sock, addr = self.__server_socket.accept()
            logging.info(f'New connection from {addr}')
            threading.Thread(target=self.__client_thread, args=(client_sock,)).start()

    def __remove_from_games(self, client):
        for i in self.games:
            if i.check_logout(client):
                logging.debug(f'Removing game {i}')
                self.games.remove(i)
        for game in self.bot_games:
            if game.is_client_in_game(client):
                logging.debug(f'Removing game {game}')
                self.bot_games.remove(game)

    def __client_thread(self, client_sock):
        sleep_time = 0.1
        client = Client(client_sock)
        self.__clients.append(client)
        try:
            while True:
                client.ping()
                msg = client.read_from_socket()
                if msg is None or msg == '':
                    time.sleep(sleep_time)
                    continue
                ####################
                # Message handling #
                ####################
                if msg['request_type'] == 'create_client':
                    try:
                        create_client(
                            msg['username'],
                            msg['email'],
                            msg['password_hash']
                        )
                        client.set_client_usr_name(msg['username'])
                        client.send_to_socket({'request_type': 'response_to_request', 'type': 'OK'})
                    except Exception as e:
                        logging.error(e)
                        client.send_to_socket({'request_type': 'response_to_request', 'type': 'ERROR', 'msg': str(e)})
                elif msg['request_type'] == 'auth_client':
                    client_exist = False
                    for i in self.__clients:
                        if i.get_username() == msg['username']:
                            client_exist = True
                            client.send_to_socket({'request_type': 'response_to_request', 'type': 'BUSY'})
                            break
                    if not client_exist:
                        try:
                            usr = auth_client(msg['username'], msg['password_hash'])
                            client.set_client_usr_name(usr)
                            client.send_to_socket(
                                {'request_type': 'response_to_request', 'type': 'OK', 'username': usr})
                            client.set_name(msg['username'])
                        except Exception as e:
                            logging.error(e)
                            client.send_to_socket(
                                {'request_type': 'response_to_request', 'type': 'ERROR', 'msg': str(e)})
                elif msg['request_type'] == 'find_opponent':
                    # setup game
                    try:
                        if self.__is_someone_waiting:
                            self.__is_someone_waiting = False
                            self.games[-1].set_clinet2(client)
                        else:
                            g = Game_with_Player(client, self)
                            self.__is_someone_waiting = True
                            self.games.append(g)
                    except:
                        pass

                elif msg['request_type'] == 'play_with_bot':
                    game = BotGame(client, msg['color'], msg['elo'], self)
                    self.bot_games.append(game)
                elif msg['request_type'] == 'message':
                    for i in self.games:
                        i.check_if_player_in(client, msg['text'])
                elif msg['request_type'] == 'player_move':
                    for game in self.games + self.bot_games:
                        is_valid = game.check_move(msg['move'])
                        client.send_to_socket({'request_type': 'move_valid', 'valid': is_valid})
                        if is_valid:
                            if game in self.bot_games:
                                sleep(sleep_time * 2)
                                game.make_move(msg['move'])
                            else:
                                sleep(sleep_time * 2)
                                if client == game.get_client():
                                    oponnent = game.get_client2()
                                else:
                                    oponnent = game.get_client()
                                game.make_move(msg['move'])
                                oponnent.send_to_socket({'request_type': 'player_move', 'move': msg['move']})
                elif msg['request_type'] == 'resign':
                    for i in self.games:
                        if i.check_logout(client):
                            self.games.remove(i)
                    for i in self.bot_games:
                        if i.is_client_in_game(client):
                            self.bot_games.remove(i)
                    client.send_to_socket({'request_type': 'resign'})
                time.sleep(sleep_time)
        except ConnectionResetError:
            logging.warning(f'Connection reset for client {client}, deleting client')
            self.__clients.remove(client)
            self.__remove_from_games(client)
            return
        except BrokenPipeError:
            logging.warning(f'Broken pipe for client {client}, deleting client')
            self.__clients.remove(client)
            self.__remove_from_games(client)
            return
        except JSONDecodeError:
            logging.warning(f'Broken pipe for client {client}, deleting client')
            self.__clients.remove(client)
            self.__remove_from_games(client)
            return


s = Server()
while True:
    pass
