from src.Server.server_client import Client


class Game_with_Player:
    def __init__(self, client):
        self.__client = client
        self.__client2 = None

    def set_clinet2(self, client2):
        self.__client2 = client2
        self.start_game()

    def check_logout(self):
        # TODO dodać jak ktoś wyjdzie żeby skończyło grę
        pass

    def check_if_player_in(self,client,mess):
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
        msg = {
            'request_type': 'start_game',
            'opponent': self.__client2.get_username(),
        }
        msg2 = {
            'request_type': 'start_game',
            'opponent': self.__client.get_username(),
        }
        self.__client.send_to_socket(msg)
        self.__client2.send_to_socket(msg2)
        print("started")
