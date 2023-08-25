"""
Задание 5.

Выполнить пинг веб-ресурсов yandex.ru, youtube.com и
преобразовать результаты из байтовового в строковый тип на кириллице.

Подсказки:
--- используйте модуль chardet, иначе задание не засчитается!!!
"""
import chardet

import os


def ping(host, count):
    resp = os.popen(f'ping -n {count} {host}').read().encode('cp1251')
    enc = chardet.detect(resp)

    resp = resp.decode(enc['encoding'])
    print(resp)


ping('yandex.ru', 2)
ping('youtube.com', 3)
