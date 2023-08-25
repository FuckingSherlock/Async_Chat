'''Проверка валидности порта сервера'''


class Port:
    def __set__(self, instance, value):
        if not 1023 < value < 65536:
            print(
                f'Port error. Port {value} is not valid. Valid addresses from 1024 to 65535.')
            exit(1)
        else:
            print('GOOD')
        instance.__dict__[self.name] = value

    def __set_name__(self, owner, name):
        self.name = name
