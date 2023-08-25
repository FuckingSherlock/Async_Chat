from socket import *
import json
import os
from client_meta import ReaderClientVerifier
import path
from client_database.client_db import Storage

directory = path.Path(__file__).abspath().parent.parent
os.chdir(directory+'\\client')


def set_db(username):
    '''Функция подключения к базе данных клиента'''
    db = Storage(username)
    return db


def conn():
    '''Функция создания сокета клиента и подключения к серверу'''
    sock = socket(AF_INET, SOCK_STREAM)
    sock.connect(('localhost', 7777))
    return sock


def add_local_data(msg, data):
    '''Функция записи данных в бд клиента'''
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
        data.save_message(msg['sender'], text)
        return 0


def get_message(message, database):
    '''Функция разбора сообщения, 
    принимает сообщение и базу данных клиента'''
    dcded_msg = json.loads(message)
    sender = dcded_msg['sender']
    text = dcded_msg['text']
    try:
        act = dcded_msg['act']
    except:
        act = ''
    info = 'msg'
    if dcded_msg['sender'] == 'server':
        if isinstance(text, list):
            print('Ваши контакты:')
            for i in text:
                print(i)
        else:
            info = add_local_data(dcded_msg, database)
    print(__name__, [info, sender, text])
    if act:
        return [info, sender, text, act]
    return [info, sender, text]


class ClientRead(metaclass=ReaderClientVerifier):

    def __init__(self, user, password):
        '''
        Класс клиента для чтения, 
        принимает имя пользователя и пароль.
        Основан на проверочном метаклассе ReaderClientVerifier.
        '''
        self.username = user
        self.db = set_db(user)
        self.pwd = password
        self.sock = conn()

    def hello(self):
        '''Метод отправки первого сообщения 
        содержащего имя и пароль серверу'''
        print(self.pwd)
        self.sock.send(f'{self.username}.reader.{self.pwd}'.encode('utf-8'))

    def run(self):
        '''Метод запуска чтения сообщений от сервера'''
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
