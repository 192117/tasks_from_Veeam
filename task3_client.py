# Клиент
import socket


class Client:

    def __init__(self, host):
        self.host = host

    def connect_to_8000(self, message_send):
        """ Метод для конекта с 8000 портом."""
        with socket.create_connection((self.host, 8000)) as sock:
            try:
                sock.sendall(message_send.encode("utf-8"))
                answer = sock.recv(1024).decode("utf-8")
            except Exception:
                print("Something's wrong!")
            return answer

    def connect_to_8001(self, message_send):
        """ Метод для конекта с 8001 портом."""
        with socket.create_connection((self.host, 8001)) as sock:
            try:
                sock.sendall(message_send.encode("utf-8"))
                answer = sock.recv(1024).decode("utf-8")
            except Exception:
                print("Something's wrong!")
            return answer

    def send_user(self, user):
        """ Метод для отправки на 8000 порт идентификатора. И получения своего ключа."""
        data = "{}".format(str(user))
        answer = self.connect_to_8000(data)
        print("Your key: {}".format(answer))

    def send_text(self, text, user, user_value):
        """ Метод для отправки на 8000 порт текста, идентификатора и ключа."""
        data = "{}-{}-{}".format(text, str(user), str(user_value))
        answer = self.connect_to_8001(data)
        print(answer)