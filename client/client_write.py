from PyQt5.QtWidgets import QApplication, QWidget
from socket import *
import json
from subprocess import Popen, CREATE_NEW_CONSOLE
import sys
import os
import time
import path
from meta import WriterClientVerifier

directory = path.Path(__file__).abspath().parent.parent
# sys.path.append(directory+'\\database')
# os.chdir(directory+'\\client')


def set_username(usr):
    if not usr:
        usr = int(input('Введите ваш ник: '))
    print('Ваше имя: ', usr)
    return usr


def conn():
    sock = socket(AF_INET, SOCK_STREAM)
    sock.connect(('localhost', 7777))
    return sock


def send_message():
    pass


class ClientWrite(metaclass=WriterClientVerifier):

    def __init__(self, user, password):
        self.username = user
        self.pwd = password
        self.sock = conn()

    def hello(self):
        self.sock.send(f'{self.username}.writer.{self.pwd}'.encode('utf-8'))
        print('Ожидание сервера')

    def send_message(self, act, recip, text):
        send_message()
        req = {'act': act,
               'recip': recip,
               'sender': self.username,
               'text': text}
        message = json.dumps(req)
        self.sock.send(message.encode('utf-8'))
