from socket import *
import json
from subprocess import Popen, CREATE_NEW_CONSOLE
import sys
import os
import time
from meta import WriterClientVerifier

path = os.path.dirname(os.path.abspath(__file__))
os.chdir(path)


def set_username(usr):
    if not usr:
        usr = input('Введите ваш ник: ')
    print('Ваше имя: ', usr)
    return usr


def send_message(msg, sock):
    message = json.dumps(msg)
    sock.send(message.encode('utf-8'))


class ClientWrite(metaclass=WriterClientVerifier):
    # class ClientWrite():

    def __init__(self, user, sock):
        self.username = user
        self.sock = sock

    def hello(self):
        self.sock.send(f'{self.username}.writer'.encode('utf-8'))
        # time.sleep(1)

    def run(self):
        self.hello()
        # time.sleep(2)
        # self.sock.send(f'{self.username}.writer'.encode('utf-8'))
        # Popen(f'python client_read.py {username}', creationflags=CREATE_NEW_CONSOLE)
        while True:
            inp = input("Лс: /pm, Общий чат: /all, Выход: q\n").upper()
            # <recipient's name> message
            if inp == 'Q':
                break
            elif inp.startswith('/PM'):
                recep = input("Введите имя получателя: ")
            elif inp.startswith('/ALL'):
                recep = 'all'
            text = input("Введите сообщение: ")
            req = {'recip': recep,
                   'sender': self.username,
                   'text': text}
            send_message(req, self.sock)


if __name__ == '__main__':
    os.system('mode con:cols=70 lines=15')
    try:
        user = sys.argv[1]
    except IndexError:
        user = ''
    finally:
        username = set_username(user)
        s = socket(AF_INET, SOCK_STREAM)
        s.connect(('localhost', 7777))
        client_w = ClientWrite(username, s)
        client_w.run()
