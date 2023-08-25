''' 3. Задание на закрепление знаний по модулю yaml. 
Написать скрипт, автоматизирующий сохранение данных в файле YAML-формата. Для этого:
Подготовить данные для записи в виде словаря, в котором первому ключу соответствует список, 
второму — целое число, третьему — вложенный словарь, 
где значение каждого ключа — это целое число с юникод-символом, 
отсутствующим в кодировке ASCII (например, €);
Реализовать сохранение данных в файл формата YAML — например, 
в файл file.yaml. При этом обеспечить стилизацию файла с помощью параметра default_flow_style,
а также установить возможность работы с юникодом: allow_unicode = True;
Реализовать считывание данных из созданного файла и проверить, совпадают ли они с исходными.'''

import yaml

dct = {1: [], 2: 500, 3: {1: '5\u8381', 2: '23\u3364', 3: '876\u1846'}}

with open('file.yaml', 'w', encoding='utf-8') as f:
    yaml.dump(dct, f, allow_unicode=True, default_flow_style=False)

with open('file.yaml', 'r', encoding='utf-8') as f:
    dct2 = yaml.full_load(f)
if dct2 == dct:
    print('Данные совпадают')