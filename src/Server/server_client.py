import json
import logging
import select
import threading

# LOGGING CONFIG
logging.basicConfig(format='%(asctime)s :: %(levelname)s :: %(message)s', level=logging.DEBUG)


class Client:
    def __init__(self, client_socket):
        self.__client_socket = client_socket
        self.__client_database_usr_name = None
        self.__username = None
        self.__client_lock = threading.Lock()

    def set_name(self, n):
        self.__username = n

    def get_username(self):
        return self.__username

    def set_client_usr_name(self, value):
        self.__client_database_usr_name = value

    def __lock_acquire(self):
        self.__client_lock.acquire()

    def __lock_release(self):
        self.__client_lock.release()

    def ping(self):
        self.send_to_socket({'request_type': 'ping'})

    def read_from_socket(self):
        self.__lock_acquire()
        ready = select.select([self.__client_socket], [], [], 0.00001)
        if ready[0]:
            msg = self.__client_socket.recv(1024).decode()
        else:
            msg = ''
        self.__lock_release()
        if msg == '':
            return None
        msg_dec = json.loads(msg)
        logging.debug(f'{self} got message: {msg_dec}')
        return msg_dec

    def send_to_socket(self, msg_dict):
        response = json.dumps(msg_dict)
        self.__lock_acquire()
        self.__client_socket.send(response.encode())
        if msg_dict['request_type'] != 'ping':
            logging.debug(f'{self} sent message: {msg_dict}')
        self.__lock_release()
