from socket import *
import sys
import json


def get_client_msg_and_answer(msg):
    dcded_msg = json.loads(msg.decode('utf-8'))
    client_name = dcded_msg['user']['account_name']
    msg_to_client = f"Hellow {client_name}, welcome! The connection is fine!"
    return json.dumps(msg_to_client).encode('utf-8')


def main():
    client_ip = ''
    tcp_port = ''
    try:
        for i, arg in enumerate(sys.argv):
            if arg == '-a':
                client_ip = sys.argv[i+1]
            if arg == '-p':
                tcp_port = int(sys.argv[i+1])
        if not client_ip:
            print('IP не был указан, по умолчанию "localhost"')
            client_ip = 'localhost'
        if not tcp_port:
            print('Порт не был указан, по умолчанию "7777"')
            tcp_port = 7777
        if tcp_port < 1024 or tcp_port > 65535:
            raise ValueError
    except:
        sys.exit(1)
    print(f'Listening to client {client_ip}:{tcp_port}')

    s = socket(AF_INET, SOCK_STREAM)
    s.bind((client_ip, tcp_port))
    s.listen(5)

    while True:
        client, addr = s.accept()  # Принять запрос на соединение
        print("Получен запрос на соединение от %s" % str(addr))
        msg_from_client = client.recv(1000000)
        msg_to_client = get_client_msg_and_answer(msg_from_client)
        client.send(msg_to_client)
        client.close()


if __name__ == '__main__':
    main()
