"""
Задание 4.

Преобразовать слова «разработка», «администрирование», «protocol»,
«standard» из строкового представления в байтовое и выполнить
обратное преобразование (используя методы encode и decode).

Подсказки:
--- используйте списки и циклы, не дублируйте функции
"""

str_list = ['разработка', 'администрирование', 'protocol', 'standard']
bytes_list = []
back_to_str = []

for i in str_list:
    bytes_list.append(i.encode('utf-8'))

print(bytes_list)
print([i.decode('utf-8') for i in bytes_list])
