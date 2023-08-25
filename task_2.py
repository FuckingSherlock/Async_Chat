''' 2. Задание на закрепление знаний по модулю json.
Есть файл orders в формате JSON с информацией о заказах.
Написать скрипт, автоматизирующий его заполнение данными. Для этого:
Создать функцию write_order_to_json(), в которую передается 5 параметров — товар (item),
количество (quantity), цена (price), покупатель (buyer), дата (date).
Функция должна предусматривать запись данных в виде словаря в файл orders.json.
При записи данных указать величину отступа в 4 пробельных символа;
Проверить работу программы через вызов функции write_order_to_json()
с передачей в нее значений каждого параметра.'''

import json


def write_order_to_json(item, quantity, price, buyer, date):
    with open('orders.json', 'rt', encoding='utf-8') as f:
        dc = json.load(f)

    dc['orders'].append({'item': item, 'quantity': quantity,
                         'price': price, 'buyer': buyer, 'date': date})
    with open('orders.json', 'wt', encoding='utf-8') as f:
        json.dump(dc, f, indent=4, ensure_ascii=False)


write_order_to_json('футболка', '5', '500', 'sherlock', '20.11.22')
