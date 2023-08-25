from socket import *
import sys
import json
import logging as lg
# from log.server_log_config import *
from decorators.log_decor import *
from select import select


@func_log
def get_and_forward_msg_to_clients(msg, client):
    # dcded_msg = json.loads(msg.decode('utf-8'))
    # lg.debug(dcded_msg)
    # print(dcded_msg)
    # return json.dumps(msg_to_clients).encode('utf-8')
    client.send(msg)


def listening_socket(address):
    s = socket(AF_INET, SOCK_STREAM)
    s.bind(address)
    s.listen(5)
    s.settimeout(0.2)
    return s


def read_requests(r_clients, all_clients):
    responses = {}
    for sock in r_clients:
        try:
            data = sock.recv(1024).decode('utf-8')
            try:
                data = json.loads(data)
            except:
                pass
            print(f'Client {sock.getpeername()} send: ', data)
            responses[sock] = data
        except:
            print(f'Client {sock.fileno()} {sock.getpeername()} has disconnected')
            all_clients.remove(sock)
    return responses


def write_responses(requests, w_clients, all_clients):
    recipients = all_clients
    for sock in w_clients:
        if sock in requests:
            try:
                # resp = f'Client {sock.getpeername()} sent: {requests[sock]}'.encode('utf-8')
                resp = f'Client {sock.getpeername()[1]} sent: {requests[sock]}'.encode('utf-8')
            except:
                print(f'Client {sock.fileno()} {sock.getpeername()} has disconnected')
                info(all_clients)
                sock.close()
    # print(recipients)
    client_p = list(requests[sock].keys())[0]
    # print(client_p)
    msg = requests[sock][client_p]
    if type(requests[sock]) == type(dict()):
        # resp = f'Client {sock.getpeername()[1]} sent: {requests[sock][list(requests[sock].keys())[0]]}'.encode(
        #     'utf-8')
        resp = f'Client {sock.getpeername()[1]} sent: {msg}'.encode('utf-8')
        for s in recipients:
            if s.getpeername()[1] == int(client_p):
                s.send(resp)
            return
    else:
        for i in recipients:
            i.send(resp)


def info(all_clients):
    for i in all_clients:
        hello_msg = f'Ваше имя: {i.getpeername()[1]}\nДоступные адресаты: {[n.getpeername()[1] for n in all_clients]}'.encode(
            'utf-8')
        i.send(hello_msg)


@func_log
def mainloop():
    address = ('', 7777)
    clients = []
    s = listening_socket(address)

    while True:
        try:
            conn, addr = s.accept()
        except OSError as e:
            pass
        else:
            # lg.info("Получен запрос на соединение от %s" % str(addr))
            print("Получен запрос на соединение от %s" % str(addr))
            clients.append(conn)
            info(clients)
        finally:
            wait = 1
            w = []
            r = []
            try:
                r, w, e = select(clients, clients, [], wait)
            except Exception as e:
                pass

            requests = read_requests(r, clients)

            if requests:
                write_responses(requests, w, clients)

            # for s_client in w:
            #     try:
            #         s_client.send('text test'.encode('utf-8'))
            #     except:
            #         clients.remove(s_client)


# @func_log
# def main():
#     lg.info('Запуск сервера')
#     client_ip = ''
#     tcp_port = ''
#     try:
#         for i, arg in enumerate(sys.argv):
#             if arg == '-a':
#                 client_ip = sys.argv[i+1]
#             if arg == '-p':
#                 tcp_port = int(sys.argv[i+1])
#         if not client_ip:
#             lg.info('IP не был указан, по умолчанию "localhost"')
#             client_ip = 'localhost'
#         if not tcp_port:
#             lg.info('Порт не был указан, по умолчанию "7777"')
#             tcp_port = 7777
#         if tcp_port < 1024 or tcp_port > 65535:
#             raise ValueError
#     except:
#         lg.critical('Чет пошло не так при запуске')
#         sys.exit(1)
#     lg.info(f'Listening to client {client_ip}:{tcp_port}')

#     s = socket(AF_INET, SOCK_STREAM)
#     s.bind((client_ip, tcp_port))
#     s.listen(5)

    # while True:
    #     client, addr = s.accept()  # Принять запрос на соединение
    #     lg.info("Получен запрос на соединение от %s" % str(addr))
    #     msg_from_client = client.recv(1000000)
    #     msg_to_client = get_client_msg_and_answer(msg_from_client)
    #     client.send(msg_to_client)
    #     client.close()

if __name__ == '__main__':
    mainloop()
