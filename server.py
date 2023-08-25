from client.meta import ServerVerifier
import time
import json
import hashlib
import socket
from select import select
from descr import Port
from server_database.server_db import Storage


class Server(metaclass=ServerVerifier):
    # class Server():
    port = Port()

    def __init__(self, address, database):
        self.database = database
        self.address = address
        self.port = address[1]  # КАКОГО ЭТО ВООБЩЕ РАБОТАЕТ????
        self.addr = address[0]
        self.inputs = []
        self.outputs = []
        self.readers = {}
        self.writers = {}
        self.requests = False
        self.s = 0
        all_clients = self.database.clients_list()
        self.all_clients = [i[0] for i in all_clients]

    def listening_socket(self):
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.bind(self.address)
        self.s.settimeout(0.2)
        self.inputs.append(self.s)
        self.s.listen(5)
        print(f'Serv addr {self.address}')
        return self.s

    @staticmethod
    def print_stage():
        print('Сервер запущен')

    def hello_send_contacts(self, username, s):
        answer = self.database.get_contacts(username)
        if type(answer) != str:
            answer = [i[0] for i in answer]
        msg = {'recip': username,
               'sender': 'server',
               'text': answer}
        msg_enc = json.dumps(msg).encode('utf-8')
        s.send(msg_enc)

    def check_pwd(self, user, pwd):
        server_hash = ''
        server_hash = self.database.get_client_pwd(user)[0]
        print(server_hash)
        if server_hash:
            if pwd == server_hash:  # докрутить проверку
                return True
        return False

    def accept_conn(self, connect):
        sock, addr = connect.accept()
        pwd = 0
        try:
            name = sock.recv(1024).decode('utf-8').split('.')
            print(f"Получен запрос на соединение от {name[0]}({name[1]}) {name[2]}")
            sock.setblocking(False)
            msg = {'recip': name[0],
                   'sender': 'server',
                   'text': None,
                   'act': 'INFO'}
            print()
            if self.all_clients:
                print(self.all_clients)
                if name[0]+name[1] in self.all_clients:
                    pwd = self.check_pwd(name[0]+name[1], name[2])
                    if pwd == False:
                        print('Проверка пароля неудачно')
                        msg['text'] = 'Вы ввели неверный пароль'
                        msg_enc = json.dumps(msg).encode('utf-8')
                        sock.send(msg_enc)
                        sock.close()
                        return 0, '000', 0, 0
            else:
                pwd = name[2]
                msg['text'] = 'Регистрация прошла успешно'
                msg_enc = json.dumps(msg).encode('utf-8')
                sock.send(msg_enc)
        except:
            print('\nNAME ERROR\n')
        return sock, name, addr, pwd

    def read_requests(self, sock):
        inp, w_clients = self.inputs, self.writers
        responses = {}
        data = False
        for name in w_clients:
            if w_clients[name] == sock:
                sender_name = name
        try:
            data = json.loads(sock.recv(1024).decode('utf-8'))
            print(data)
            if data:
                responses[data['recip']] = [sender_name, data['text'], data['act']]
            else:
                print(f"Клиент {sender_name} отключился...")
                inp.remove(sock)
                del w_clients[sender_name]
                sock.close()
        except:
            pass
        return responses, inp, w_clients

    def write_responses(self, r_clients):
        for recip in list(self.requests.keys()):
            sender = self.requests[recip][0]
            message = self.requests[recip][1]
            act = self.requests[recip][2]
            if act != 'msg' and recip == 'server':
                answ_contact = ''
                req_contact = message
                if act == 'add_contact':
                    answer = self.database.add_contact(sender, req_contact)
                    answ_contact = answer[1]
                    answer = answer[0]
                elif act == 'del_contact':
                    answer = self.database.del_contact(sender, req_contact)
                    answ_contact = answer[1]
                    answer = answer[0]
                elif act == 'get_contacts':
                    print('get_contacts')
                    answer = self.database.get_contacts(sender)
                    if isinstance(answer, list):
                        answer = [i[0] for i in answer]
                    print(answer)

                elif act == 'get_connected':
                    print('get_connected')
                    answer = self.database.get_connected()
                    if isinstance(answer, list):
                        answer = [i[0] for i in answer]
                    print(answer)
                elif act == 'sync_contacts':
                    self.database.add_contact(sender, req_contact)
                    answer = 'Контакты синхронизированы'
                msg = {'recip': sender,
                       'sender': 'server',
                       'text': answer,
                       'act': act}
                if answ_contact:
                    msg['contact'] = answ_contact
                print(msg)
                msg_enc = json.dumps(msg).encode('utf-8')
                sock = self.readers[sender]
                sock.send(msg_enc)
                del self.requests['server']
                time.sleep(0.2)

            elif recip == 'all':
                msg = {'recip': 'all',
                       'sender': sender,
                       'text': message}
                msg_enc = json.dumps(msg).encode('utf-8')
                del self.requests['all']
                for sock in r_clients:
                    sock.send(msg_enc)
                    time.sleep(0.2)
            else:
                if recip in list(self.readers.keys()):
                    sock = self.readers[recip]
                    if sock in r_clients:
                        msg = {'recip': recip,
                               'sender': sender,
                               'text': message}
                        msg_enc = json.dumps(msg).encode('utf-8')
                        sock.send(msg_enc)
                        del self.requests[recip]
                        time.sleep(0.2)
                    else:
                        for name in list(self.readers.keys()):
                            if name == sender:
                                msg = {'recip': sender,
                                       'sender': 'server',
                                       'text': 'Получатель оффлайн'}
                                msg_enc = json.dumps(msg).encode('utf-8')
                                self.readers[name].send(msg_enc)

    def mainloop(self):
        self.listening_socket()
        self.print_stage()
        while True:
            read, write, err = select(self.inputs, self.outputs, [], 1)
            for conn in read:
                if conn != self.s:
                    self.requests, self.inputs, self.writers = self.read_requests(conn)
                else:
                    sock, name, addr, pwd = self.accept_conn(conn)
                    if name[1] == 'writer':
                        self.writers[name[0]] = sock
                        self.inputs.append(sock)
                        self.database.client_login(
                            name[0], name[1], addr[0], addr[1], pwd)
                    elif name[1] == 'reader':
                        self.readers[name[0]] = sock
                        self.outputs.append(sock)
                        self.database.client_login(
                            name[0], name[1], addr[0], addr[1], pwd)
                    all_clients = self.database.clients_list()
                    self.all_clients = [i[0] for i in all_clients]

            if self.requests:
                self.write_responses(write)


def run_server():
    database = Storage()
    srv = Server(('', 7777), database)
    srv.mainloop()


if __name__ == '__main__':
    run_server()
