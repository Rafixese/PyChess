


class Game_with_Player:
    def __init__(self,client):
        self.__client = client
        self.__client2 = None

    def set_clinet2(self,client2):
        self.__client2 = client2
        self.start_game()

    def check_logout(self):
        #TODO dodać jak ktoś wyjdzie żeby skończyło grę
        pass

    def start_game(self):
        msg = {
            'request_type': 'start_game',
            'opponent': self.__client2.__client_database_usr_name,
        }
        msg2 = {
            'request_type': 'start_game',
            'opponent': self.__client1.__client_database_usr_name,
        }
        self.__client.send_to_socket(msg)
        self.__client2.send_to_socket(msg2)
