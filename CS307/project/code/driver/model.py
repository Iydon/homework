import threading
import socket

from config import default_host, default_port, default_encoding, default_bufsize


class BlockingListener(threading.Thread):
    def __init__(self, port=default_port):
        threading.Thread.__init__(self)
        self.port = port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.bind((default_host, port))
        self.sock.listen(0)

    def run(self):
        print('listener started')
        while True:
            client, cltadd = self.sock.accept()
            help(self.sock.accept)
            while True:
                data = client.recv(default_bufsize)
                if not data:
                    break
                print(data.decode(default_encoding), '')
            print('accept a connect')


if __name__ == '__main__':
    lst = BlockingListener()
    lst.start()
