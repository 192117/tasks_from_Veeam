# Сервер
import asyncio
import random


class ClientServerProtocol(asyncio.Protocol):

    user_id = dict()

    def process_data(self, message, port):
        """ Обработка сообщений от клиентов."""
        try:
            parse_message = message.split("-")
            if len(parse_message) == 1 and port == 8000:
                return self.check_id(parse_message[0])
            elif len(parse_message) == 3 and port == 8001:
                return self.check_id_from_message(parse_message[0], parse_message[1], parse_message[2])
            else:
                return "error wrong command\n"
        except Exception as err:
            return "error wrong command\n"


    def write_value(self, user, user_value, text):
        with open(".\\server.txt", "a") as file:
            file.write("{} send {} with {}\n".format(user, text, user_value))


    def check_id(self, user):
        """ Метод для проверки наличия идентификатора пользователя в базе."""
        if user not in ClientServerProtocol.user_id:
            ClientServerProtocol.user_id[user] = str(str(id(user))[:random.randint(1, len(str(id(user)-1)))])
            return ClientServerProtocol.user_id[user]


    def check_id_from_message(self, text, user, user_value):
        """ Метод для получения сообщения от пользователя, который имеет свой идентификатор в базе и ключ."""
        if user in ClientServerProtocol.user_id:
            if ClientServerProtocol.user_id[user] == user_value:
                self.write_value(user, user_value, text)
                return "ok"
            else:
                return "Incorrect user_value"
        return ("I dont't know you {}".format(user))


    def connection_made(self, transport):
        self.port = transport.get_extra_info('sockname')[1]
        self.transport = transport


    def data_received(self, data):
        resp = self.process_data(data.decode(), self.port)
        self.transport.write(resp.encode())


def run_server(host):
    loop = asyncio.get_event_loop()
    coro = loop.create_server(
        ClientServerProtocol,
        host, 8000
    )
    coro2 = loop.create_server(
        ClientServerProtocol,
        host, 8001
    )

    group = asyncio.gather(coro, coro2)

    server = loop.run_until_complete(group)

    try:
        loop.run_forever()
    except KeyboardInterrupt:
        pass

    server.close()
    loop.run_until_complete(server.wait_closed())
    loop.close()

if __name__ == "__main__":
    run_server("127.0.0.1")