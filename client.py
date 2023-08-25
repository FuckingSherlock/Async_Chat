from socket import *
import time
from threading import Thread

addr = ('localhost', 7777)
sock = socket(AF_INET, SOCK_STREAM)
sock.connect(addr)


class InputThread(Thread):
    def run(self):
        while True:
            msg = input('Message: ')
            if msg == 'exit':
                break
            sock.send(msg.encode('utf-8'))
            time.sleep(1)


class PrintThread(Thread):
    def run(self):
        while True:
            msg_from_server = sock.recv(1024).decode('utf-8')
            print(msg_from_server)


if __name__ == '__main__':
    it = InputThread().start()
    pt = PrintThread().start()
