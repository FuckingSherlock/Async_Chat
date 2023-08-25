from socket import *
import sys
import time
import json
from datetime import datetime
import logging as lg
from log.client_log_config import *


def presence(username='Sherlock'):
    d = datetime.now()
    unixtime = time.mktime(d.timetuple())
    dct = {
        "action": "presence",
        "time": unixtime,
        "type": "connection check",
        "user": {
            "account_name": username,
            "status": "I am here!"
        }
    }
    return json.dumps(dct).encode('utf-8')


def get_server_msg(msg):
    return json.loads(msg.decode('utf-8'))


def main():
    lg.info('Запуск клиента')
    try:
        if len(sys.argv) == 3:
            serv_ip = sys.argv[1]
            if sys.argv[2] and type(sys.argv[2]) == list:
                tcp_port = int(sys.argv[2][0])
                if tcp_port < 1024 or tcp_port > 65535:
                    raise ValueError
        elif len(sys.argv) == 2:
            serv_ip = sys.argv[1]
            tcp_port = 7777
            lg.info('Порт не был указан, по умолчанию "7777"')
        else:
            lg.info('IP не был указан, по умолчанию "localhost"')
            lg.info('Порт не был указан, по умолчанию "7777"')
            serv_ip = 'localhost'
            tcp_port = 7777
    except:
        lg.critical('Чет пошло не так при запуске')
        sys.exit(1)

    s = socket(AF_INET, SOCK_STREAM)
    s.connect((serv_ip, tcp_port))

    s.send(presence())
    server_msg = get_server_msg(s.recv(1000000))
    lg.info(server_msg)

    s.close()


if __name__ == '__main__':
    main()
