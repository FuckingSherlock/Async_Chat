from socket import *
import json
import sys
import os
from meta import ReaderClientVerifier
import path
from client_database.client_db import Storage

from PyQt5 import QtWidgets
import client_gui

directory = path.Path(__file__).abspath().parent.parent
os.chdir(directory+'\\client')


def set_db(username):
    db = Storage(username)
    return db


def conn():
    sock = socket(AF_INET, SOCK_STREAM)
    sock.connect(('localhost', 7777))
    return sock


def add_local_data(msg, data):
    text = msg['text']
    print(__name__, msg)
    if 'contact' in msg:
        contact = msg['contact']
        if text == f'Контакт {contact} успешно добавлен' or text == 'У вас уже есть этот контакт':
            data.add_contact(contact)
        elif text == f'Контакт {contact} успешно удален':
            data.del_contact(contact)
        return text
    else:
        data.save_message(msg['sender'], msg['recip'], text)
        return 0


def get_message(message, database):
    dcded_msg = json.loads(message)
    sender = dcded_msg['sender']
    text = dcded_msg['text']
    act = ''
    try:
        act = dcded_msg['act']
    except:
        pass
    where = ''
    info = 'msg'
    if dcded_msg['sender'] == 'server':
        if isinstance(text, list):
            print('Ваши контакты:')
            for i in text:
                print(i)
        else:
            info = add_local_data(dcded_msg, database)

    # if dcded_msg['recip'] == 'all':
    #     where = f'Сообщение в общий чат от {sender}: '
    # else:
    #     where = f'Личное сообщение от {sender}: '
    # print(__name__, where, text)
    print(__name__, [info, sender, text])
    if act:
        return [info, sender, text, act]
    return [info, sender, text]


class ClientRead(metaclass=ReaderClientVerifier):

    def __init__(self, user, password):
        self.username = user
        self.db = set_db(user)
        self.pwd = password
        self.sock = conn()

    def hello(self):
        print(self.pwd)
        self.sock.send(f'{self.username}.reader.{self.pwd}'.encode('utf-8'))

    def run(self):

        msg_from_server = self.sock.recv(1024).decode('utf-8')
        if msg_from_server:
            print(__name__, get_message(msg_from_server, self.db))
            return get_message(msg_from_server, self.db)


# if __name__ == '__main__':
#     os.system('mode con:cols=70 lines=15')
#     name = sys.argv[1]
#     s = socket(AF_INET, SOCK_STREAM)
#     s.connect(('localhost', 7777))
#     client_w = ClientRead(name, s)
#     client_w.run()
