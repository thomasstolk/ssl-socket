import socket
import ssl

from threading import Thread

from utils import PROJECT_ROOT


def read_keys():
    letter = 'a'
    while ord(letter) <= ord('z'):
        __import__('time').sleep(0.1)
        yield letter.encode()
        letter = chr(ord(letter) + 1)


def record_sound():
    sound = b'la'*2048
    for i in range(1, 10):
        __import__('time').sleep(0.2)
        yield sound


SERVER_HOSTNAME = 'test.nl'
SERVER_ADDRESS = '127.0.0.1'
SERVER_PORT = 12345
SERVER_CERT = f'{PROJECT_ROOT}/keys/server.crt'
CLIENT_CERT = f'{PROJECT_ROOT}/keys/client.crt'
PRIVATE_KEY = f'{PROJECT_ROOT}/keys/client.key'

DATA_TYPES = [
    {'name': 'keylogger', 'id': b'9bbbbd52-a8c7-4e2a-a7e2-82d74c0694e2', 'data_collector': read_keys},
    {'name': 'sound recorder', 'id': b'24176171-0c93-4d8f-b328-4ce93bf91c35', 'data_collector': record_sound}
]
STOP_ID = b'8e97edbb-7624-4279-9c1f-553576b0e53a'

context = ssl.create_default_context(ssl.Purpose.SERVER_AUTH, cafile=SERVER_CERT)
context.load_cert_chain(certfile=CLIENT_CERT, keyfile=PRIVATE_KEY)


class Connection(Thread):
    def __init__(self, _socket, _data_type):
        Thread.__init__(self)
        self.conn = context.wrap_socket(_socket, server_side=False, server_hostname=SERVER_HOSTNAME)
        self.name = _data_type['name']
        self.id = _data_type['id']
        self.data_collector = _data_type['data_collector']
        self.start()

    def run(self):
        try:
            self.conn.connect((SERVER_ADDRESS, SERVER_PORT))
            print('Connection started')
            self.conn.send(self.id)
            for data in self.data_collector():
                self.conn.send(data)
                if self.conn.recv(36) == STOP_ID:
                    break
        finally:
            print('Connection closed')
            self.conn.shutdown(socket.SHUT_RDWR)
            self.conn.close()


for data_type in DATA_TYPES:
    Connection(socket.socket(socket.AF_INET, socket.SOCK_STREAM), data_type)

