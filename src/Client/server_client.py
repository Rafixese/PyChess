import select
import socket
import logging
import time
import uuid
import datetime
import threading
import json
from time import sleep

# LOGGING CONFIG
logging.basicConfig(format='%(asctime)s :: %(levelname)s :: %(message)s', level=logging.DEBUG)

# SERVER CONFIG
HOST = ''
PORT = 8888


class Client:
    def __init__(self):
        self.__client_socket = None
        self.__connect_to_server()

    def __connect_to_server(self):
        logging.debug(f'Connecting to server')
        self.__client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            self.__client_socket.connect((HOST, PORT))
        except ConnectionRefusedError as error:
            logging.error(error)

    def read_from_socket(self):
        msg = self.__client_socket.recv(1024).decode()
        if msg == '':
            return None
        msg_dec = json.loads(msg)
        logging.debug(f'{self} got message: {msg_dec}')
        return msg_dec

    def send_to_socket(self, msg_dict):
        response = json.dumps(msg_dict)
        logging.debug(f'{self} sending message: {msg_dict}')
        self.__client_socket.send(response.encode())


c = Client()
c.send_to_socket({'abc': 'abc'})
#fan legi