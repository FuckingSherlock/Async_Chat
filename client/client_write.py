
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
sys.path.append(directory+'\\database')
os.chdir(directory+'\\client')


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
        print('Ожидание сервера')
        time.sleep(2)

    def run(self):
        self.hello()
        # time.sleep(2)
        # self.sock.send(f'{self.username}.writer'.encode('utf-8'))
        # Popen(f'python client_read.py {username}', creationflags=CREATE_NEW_CONSOLE)
        while True:
            inp = input("Лс: /pm, Общий чат: /all, Выход: /q,\nНастройки: /s\n ").upper()
            # <recipient's name> message
            if inp == '/Q':
                break
            if inp == '/S':
                inp2 = input(
                    'Добавить контакт: /add, Удалить контакт: /del,\nПоказать контакты: /get, Назад: /c\n ').upper()
                recip = 'server'

                if inp2.startswith('/ADD'):
                    act = 'add_contact'
                    text = input('Введите имя нового контакта: ')
                elif inp2.startswith('/DEL'):
                    act = 'del_contact'
                    text = input('Введите имя удаляемого контакта: ')
                elif inp2.startswith('/GET'):
                    act = 'get_contacts'
                    text = None
                elif inp2.startswith('/C'):
                    continue
                else:
                    continue

            elif inp.startswith('/PM'):
                act = 'msg'
                recip = input("Введите имя получателя: ")
                text = input("Введите сообщение: ")
            elif inp.startswith('/ALL'):
                act = 'msg'
                recip = 'all'
                text = input("Введите сообщение: ")
            else:
                continue
            req = {'act': act,
                   'recip': recip,
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


# if __name__ == '__main__':
#     app = QApplication(sys.argv)  # [2]
#     w = QWidget()  # [3]
#     w.resize(850, 750)  # [4]
#     w.setWindowTitle('Simple')  # [6]
#     w.show()  # [7]
#     sys.exit(app.exec_())
