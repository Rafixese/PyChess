import json
import threading
import logging

# LOGGING CONFIG
logging.basicConfig(format='%(asctime)s :: %(levelname)s :: %(message)s', level=logging.DEBUG)

class Client:
    def __init__(self, client_socket):
        self.__client_socket = client_socket
        self.__client_database_record = None
        self.__client_lock = threading.Lock()

    def lock_acquire(self):
        self.__client_lock.acquire()

    def lock_release(self):
        self.__client_lock.release()

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
