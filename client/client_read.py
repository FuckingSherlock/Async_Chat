from socket import *
import json
from subprocess import Popen, CREATE_NEW_CONSOLE
import sys
import os
import time
from meta import ReaderClientVerifier

path = os.path.dirname(os.path.abspath(__file__))
os.chdir(path)


def get_message(s):
    msg_from_server = s.recv(1024).decode('utf-8')
    dcded_msg = json.loads(msg_from_server)
    where = ''
    sender = dcded_msg['sender']
    msg = dcded_msg['text']
    if 'recip' in list(dcded_msg.keys()):
        if dcded_msg['recip'] == 'all':
            where = f'Сообщение в общий чат от {sender}: '
    else:
        where = f'Личное сообщение от {sender}: '
    print(where, msg)


class ClientRead(metaclass=ReaderClientVerifier):

    def __init__(self, user, sock):
        self.username = user
        self.sock = sock
        # self.s = addr

    def hello(self):
        # self.s = socket(AF_INET, SOCK_STREAM)
        # self.s.connect(self.sock)
        # time.sleep(1)
        self.sock.send(f'{self.username}.reader'.encode('utf-8'))
        # return self.sock

    def run(self):
        self.hello()
        print('Ваше имя: ', self.username)
        while True:
            get_message(self.sock)


if __name__ == '__main__':
    os.system('mode con:cols=70 lines=15')
    # try:
    #     user = sys.argv[1]
    # except IndexError:
    #     print('это приложение нельзя запустить самостоятельно')
    #     exit(1)
    # start_read(user)
    name = sys.argv[1]
    s = socket(AF_INET, SOCK_STREAM)
    s.connect(('localhost', 7777))
    client_w = ClientRead(name, s)
    client_w.run()
