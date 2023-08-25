'''1. Задание на закрепление знаний по модулю CSV. Написать скрипт, осуществляющий выборку
определенных данных из файлов info_1.txt, info_2.txt, info_3.txt 
и формирующий новый «отчетный» файл в формате CSV. Для этого:
    a. Создать функцию get_data(), в которой в цикле осуществляется перебор файлов с
    данными, их открытие и считывание данных. В этой функции из считанных данных
    необходимо с помощью регулярных выражений извлечь значения параметров
    «Изготовитель системы», «Название ОС», «Код продукта», «Тип системы». Значения
    каждого параметра поместить в соответствующий список. Должно получиться четыре
    списка — например, os_prod_list, os_name_list, os_code_list, os_type_list. В этой же
    функции создать главный список для хранения данных отчета — например, main_data
    — и поместить в него названия столбцов отчета в виде списка: «Изготовитель
    системы», «Название ОС», «Код продукта», «Тип системы». Значения для этих
    столбцов также оформить в виде списка и поместить в файл main_data (также для
    каждого файла);
    b. Создать функцию write_to_csv(), в которую передавать ссылку на CSV-файл. В этой
    функции реализовать получение данных через вызов функции get_data(), а также
    сохранение подготовленных данных в соответствующий CSV-файл;
    c. Проверить работу программы через вызов функции write_to_csv().'''

import csv
import chardet

files = ['info_1.txt', 'info_2.txt', 'info_3.txt']
words = ['Изготовитель системы', 'Название ОС', 'Код продукта', 'Тип системы']


def get_data(arr, wds):
    file_data = {}
    for file in arr:
        with open(file, 'rb') as f:
            res = f.read()
            enc = chardet.detect(res)['encoding']
            dec = res.decode(enc)
        dec = dec.replace('\n', ': ').split(': ')
        lst = list(map(str.strip, dec))
        if len(lst) % 2:
            lst.append("")
        file_data[file] = dict(zip(*[iter(lst)]*2))

    for d in list(file_data.keys()):
        for key in list(file_data[d].keys()):
            if key not in wds:
                file_data[d].pop(key)

    with open('main_data.csv', 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=wds)
        writer.writeheader()
        for i in files:
            # for w in wds:
            writer.writerow(file_data[i])


get_data(files, words)
