from socket import *
import json
from subprocess import Popen, CREATE_NEW_CONSOLE
import sys
import os
import time

path = os.path.dirname(os.path.abspath(__file__))
os.chdir(path)

addr = ('localhost', 7777)
sock = socket(AF_INET, SOCK_STREAM)


def start_write(username=''):
    os.system('mode con:cols=70 lines=15')
    if not username:
        username = input('Введите ваш ник: ')
    print('Ваше имя: ', username)
    sock.connect(addr)
    sock.send(f'{username}.writer'.encode('utf-8'))
    time.sleep(1)
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
               'sender': username,
               'text': text}
        msg = json.dumps(req)
        sock.send(msg.encode('utf-8'))


if __name__ == '__main__':
    try:
        user = sys.argv[1]
        start_write(user)
    except IndexError:
        start_write()
