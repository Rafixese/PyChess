import select
import socket
import logging
import time
import uuid
import datetime
import threading
import json
from time import sleep
from src.Server.server_client import Client
from src.Server.database import create_client, auth_client
from src.Server.Game_with_Player import Game_with_Player
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
        self.__games = []
        threading.Thread(target=self.__accept_loop).start()

    def __accept_loop(self):
        logging.debug('Start of __accept_loop in Server')
        while True:
            client_sock, addr = self.__server_socket.accept()
            logging.info(f'New connection from {addr}')
            threading.Thread(target=self.__client_thread, args=(client_sock,)).start()

    def __client_thread(self, client_sock):
        sleep_time = 0.1
        client = Client(client_sock)
        self.__clients.append(client)
        while True:
            try:
                client.ping()
                msg = client.read_from_socket()
            except ConnectionResetError:
                logging.warning(f'Connection reset for client {client}, deleting client')
                self.__clients.remove(client)
                return
            except BrokenPipeError:
                logging.warning(f'Broken pipe for client {client}, deleting client')
                self.__clients.remove(client)
                return
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
                try:
                    usr = auth_client(msg['username'], msg['password_hash'])
                    client.set_client_usr_name(usr)
                    client.send_to_socket({'request_type': 'response_to_request', 'type': 'OK', 'username': usr})
                except Exception as e:
                    logging.error(e)
                    client.send_to_socket({'request_type': 'response_to_request', 'type': 'ERROR', 'msg': str(e)})
            elif msg['request_type'] == 'find_opponent':
                try:
                    if self.__is_someone_waiting:
                        self.__is_someone_waiting = False
                        self.__games[-1].set_clent2(Client)

                    else:
                        g = Game_with_Player(Client)
                        self.__is_someone_waiting = True
                        self.__games.append(g)
                except:
                    pass

            time.sleep(sleep_time)


s = Server()
while True:
    pass
