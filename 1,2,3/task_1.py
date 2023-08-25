'''1. Написать функцию host_ping(), в которой с помощью утилиты ping будет проверяться доступность сетевых узлов. Аргументом функции является список, в котором каждый сетевой узел должен быть представлен именем хоста или ip-адресом. В функции необходимо перебирать ip-адреса и проверять их доступность с выводом соответствующего сообщения («Узел доступен», «Узел недоступен»). При этом ip-адрес сетевого узла должен создаваться с помощью функции ip_address().'''


from ipaddress import ip_address
from subprocess import Popen, PIPE
import socket


def host_ping(addrs):
    result = {'Доступные узлы': "", 'Недоступные узлы': ""}
    for host in addrs:
        host_name = host
        try:
            host = ip_address(host)
        except:
            host = socket.gethostbyname(host)
        resp = Popen(f"ping {host} -w 1500 -n 1", shell=False, stdout=PIPE)
        resp.wait()
        if resp.returncode == 0:
            result['Доступные узлы'] += f'{host_name}\n'
            res_string = f'{host_name} - Узел доступен'
        else:
            result['Недоступные узлы'] += f'{host_name}\n'
            res_string = f'{host_name} - Узел недоступен'
        print(res_string)
    return result


if __name__ == "__main__":
    host_ping(['google.com', '192.168.0.101'])
