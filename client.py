from socket import *
import time
from threading import Thread
import json

addr = ('localhost', 7777)
sock = socket(AF_INET, SOCK_STREAM)
sock.connect(addr)


class InputThread(Thread):
    def run(self):
        while True:
            port = input('Recepient: ')
            text = input('Message: ')
            msg = json.dumps({port: text})
            if not port:
                msg = text
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
