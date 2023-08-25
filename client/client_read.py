from socket import *
import json
from subprocess import Popen, CREATE_NEW_CONSOLE
import sys
import os
import time
from meta import ReaderClientVerifier
import path
directory = path.Path(__file__).abspath().parent.parent
sys.path.append(directory+'\\database')
os.chdir(directory+'\\client')


def ipt():  # Потомушо автоформат, отключать не хочу, а как обойти - хз
    from client_db import Storage
    return Storage()


database = ipt()


def add_local_data(msg):
    text = msg['text']
    if 'contact' in msg:
        contact = msg['contact']
        if text == f'Контакт {contact} успешно добавлен' or text == 'У вас уже есть этот контакт':
            database.add_contact(contact)
        elif text == f'Контакт {contact} успешно удален':
            database.del_contact(contact)
    else:
        database.save_message(msg['sender'], msg['recip'], text)


def get_message(message):
    dcded_msg = json.loads(message)
    add_local_data(dcded_msg)
    where = ''
    sender = dcded_msg['sender']
    msg = dcded_msg['text']
    string = ''
    if type(msg) == list:
        print('Ваши контакты:')
        for i in msg:
            print(i)
    else:
        if dcded_msg['recip'] == 'all':
            where = f'Сообщение в общий чат от {sender}: '
        else:
            where = f'Личное сообщение от {sender}: '
        print(where, msg)


class ClientRead(metaclass=ReaderClientVerifier):

    def __init__(self, user, sock):
        self.username = user
        self.sock = sock

    def hello(self):
        # self.s = socket(AF_INET, SOCK_STREAM)
        # self.s.connect(self.sock)
        self.sock.send(f'{self.username}.reader'.encode('utf-8'))
        # return self.sock

    def run(self):
        self.hello()
        print('Ваше имя: ', self.username)
        while True:
            msg_from_server = s.recv(1024).decode('utf-8')
            if msg_from_server:
                get_message(msg_from_server)


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
