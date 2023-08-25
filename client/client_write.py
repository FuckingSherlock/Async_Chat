from socket import *
import json
import path
from client_meta import WriterClientVerifier

directory = path.Path(__file__).abspath().parent.parent


def conn():
    '''Функция создания сокета клиента и подключения к серверу'''
    sock = socket(AF_INET, SOCK_STREAM)
    sock.connect(('localhost', 7777))
    return sock


def send_message():
    pass


class ClientWrite(metaclass=WriterClientVerifier):

    def __init__(self, user, password):
        '''
        Класс клиента для отправки сообщений, 
        принимает имя пользователя и пароль.
        Основан на проверочном метаклассе WriterClientVerifier.
        '''
        self.username = user
        self.pwd = password
        self.sock = conn()

    def hello(self):
        '''Метод отправки первого сообщения 
        содержащего имя и пароль серверу'''
        self.sock.send(f'{self.username}.writer.{self.pwd}'.encode('utf-8'))
        print('Ожидание сервера')

    def send_message(self, act, recip, text):
        '''Метод отправки сообщений другим клиентам сервера'''
        send_message()
        req = {'act': act,
               'recip': recip,
               'sender': self.username,
               'text': text}
        message = json.dumps(req)
        self.sock.send(message.encode('utf-8'))
