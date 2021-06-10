from src.Server.server_client import Client
import random


class Game_with_Player:
    def __init__(self, client):
        self.__client = client
        self.__client2 = None

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

    def start_game(self):
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
        self.__client.send_to_socket(msg)
        self.__client2.send_to_socket(msg2)
        print("started")
