from socket import *
from subprocess import Popen, CREATE_NEW_CONSOLE
import os
import time

path = os.path.dirname(os.path.abspath(__file__))
os.chdir(path)
p_list = []

usernames = ['user_11', 'user_22', 'user_33', 'user_44', ]


def start_clients(c):
    for i in range(int(c)):
        p_list.append(
            Popen(f'python client_write.py {usernames[i]}', creationflags=CREATE_NEW_CONSOLE))
        # time.sleep(1)
        p_list.append(
            Popen(f'python client_read.py {usernames[i]}', creationflags=CREATE_NEW_CONSOLE))
        time.sleep(1)


while True:
    # command = input(
    #     'Запустить 4 гостя (G) / Закрыть клиенты (c) / Выйти(q): ').upper()
    command = input(
        'Запустить "S" клиентов: (s) / Закрыть клиенты (c) / Выйти(q) / Запустить 4 гостя (G): ').upper()
    if command == 'G':
        count = 4
        start_clients(count)

    elif command == 'S':
        count = input('Сколько клиентов запустить? (max 4)')

        try:
            count = int(count)
        except:
            print('Это не число')
        if count <= 4:
            start_clients(count)
        else:
            print('MAX 4!!')
    elif command == 'C':
        for p in p_list:
            p.kill()
        p_list.clear()
    elif command == 'Q':
        break
