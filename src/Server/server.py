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

# LOGGING CONFIG
logging.basicConfig(format='%(asctime)s :: %(levelname)s :: %(message)s', level=logging.DEBUG)

# SERVER CONFIG
HOST = ''
PORT = 8888


class Server:
    def __init__(self):
        # SOCKET SETUP
        self.__server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.__server_socket.bind((HOST, PORT))
        self.__server_socket.listen(9999)
        self.__clients = []
        threading.Thread(target=self.__accept_loop).start()

    def __accept_loop(self):
        logging.debug('Start of __accept_loop in Server')
        while True:
            client_sock, addr = self.__server_socket.accept()
            logging.info(f'New connection from {addr}')
            threading.Thread(target=self.__client_thread, args=(client_sock,)).start()

    def __client_thread(self, client_sock):
        client = Client(client_sock)
        self.__clients.append(client)
        while True:
            client.lock_acquire()
            msg = client.read_from_socket()
            client.lock_release()
            ####################
            # Message handling #
            ####################


            time.sleep(5)


s = Server()
while True:
    pass
