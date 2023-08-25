from socket import *
import json
from subprocess import Popen, CREATE_NEW_CONSOLE
import sys
import os

path = os.path.dirname(os.path.abspath(__file__))
os.chdir(path)

addr = ('localhost', 7777)
sock = socket(AF_INET, SOCK_STREAM)


def start_read(username):
    os.system('mode con:cols=70 lines=15')
    print('Ваше имя: ', username)
    sock.connect(addr)
    sock.send(f'{username}.reader'.encode('utf-8'))

    while True:
        msg_from_server = sock.recv(1024).decode('utf-8')
        dcded_msg = json.loads(msg_from_server)
        where = ''
        # {'recip': recip,
        # 'sender': sender,
        #  'text': text})
        sender = dcded_msg['sender']
        msg = dcded_msg['text']
        if 'recip' in list(dcded_msg.keys()):
            if dcded_msg['recip'] == 'all':
                where = f'Сообщение в общий чат от {sender}: '
        # elif dcded_msg['recip'] == username:
        else:
            where = f'Личное сообщение от {sender}: '
        print(where, msg)


if __name__ == '__main__':
    # try:
    #     user = sys.argv[1]
    # except IndexError:
    #     print('это приложение нельзя запустить самостоятельно')
    #     exit(1)
    # start_read(user)
    start_read(sys.argv[1])
