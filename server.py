from select import select
from socket import *
# import sys
import json
import time

print('Сервер запущен')


def listening_socket(address):
    s = socket(AF_INET, SOCK_STREAM)
    s.bind(address)
    s.listen(5)
    s.settimeout(0.2)
    return s


def read_requests(sock, inp, w_clients):
    responses = {}
    data = False
    for name in w_clients:
        if w_clients[name] == sock:
            sender_name = name
    try:
        data = json.loads(sock.recv(1024).decode('utf-8'))
        print(data)
        if data:
            responses[data['recip']] = [sender_name, data['text']]
        else:
            print(f"Клиент {sender_name} отключился...")
            inp.remove(sock)
            del w_clients[sender_name]
            sock.close()
    except:
        pass
    return responses, inp, w_clients


def write_responses(requests, r_clients, all_readers):
    for recip in list(requests.keys()):
        sender = requests[recip][0]
        message = requests[recip][1]
        if recip == 'all':
            msg = {'recip': 'all',
                   'sender': sender,
                   'text': message}
            msg_enc = json.dumps(msg).encode('utf-8')
            del requests['all']
            for sock in r_clients:
                sock.send(msg_enc)
                time.sleep(0.2)
            # for name in list(r_clients.keys()):
                # r_clients[name].send(msg_enc)
        else:
            if recip in list(all_readers.keys()):
                sock = all_readers[recip]
                if sock in r_clients:
                    # try:
                    msg = {'sender': sender,
                           'text': message}
                    msg_enc = json.dumps(msg).encode('utf-8')
                    sock.send(msg_enc)
                    del requests[recip]
                    time.sleep(0.2)
                    # except:
                    #     print(f'\nSEND ERR\n')
                else:
                    for name in list(all_readers.keys()):
                        if name == sender:
                            msg = {'recip': sender,
                                   'sender': 'System',
                                   'text': 'Получатель оффлайн'}
                            msg_enc = json.dumps(msg).encode('utf-8')
                            all_readers[name].send(msg_enc)


def accept_conn(connect):
    sock, addr = connect.accept()
    # print("Получен запрос на соединение от %s" % str(addr))
    sock.setblocking(False)
    try:
        name = sock.recv(1024).decode('utf-8').split('.')
        print(f"Получен запрос на соединение от {name[0]}({name[1]})")
    except:
        print('\nNAME ERROR\n')
    return sock, name


def mainloop():
    wait = 1
    address = ('', 7777)
    s = listening_socket(address)
    inputs = [s]
    outputs = []
    readers = {}
    writers = {}
    requests = False
    while True:
        read, write, err = select(inputs, outputs, [], wait)
        # try:

        for conn in read:
            if conn != s:
                requests, inputs, writers = read_requests(conn, inputs, writers)
            else:
                sock, name = accept_conn(conn)
                if name[1] == 'writer':
                    writers[name[0]] = sock
                    inputs.append(sock)
                elif name[1] == 'reader':
                    readers[name[0]] = sock
                    outputs.append(sock)
        if requests:
            write_responses(requests, write, readers)
        # for conn in write:
        #     requests, inputs, writers = read_requests(conn, inputs, writers)

        #     if requests:
        #         write_responses(requests, outputs, readers)
        # except:
        #     pass


if __name__ == '__main__':
    mainloop()
