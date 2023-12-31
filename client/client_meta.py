import dis


class ReaderClientVerifier(type):

    def __init__(self, clsname, bases, clsdict):
        '''Метакласс проверки клиента для чтения на соответствие требованиям ТЗ'''
        methods = []
        for func in clsdict:
            try:
                ret = dis.get_instructions(clsdict[func])
            except TypeError:
                pass
            else:
                for i in ret:
                    if i.opname == 'LOAD_GLOBAL':
                        if i.argval not in methods:
                            methods.append(i.argval)

        for command in ('accept', 'listen', 'socket'):
            if command in methods:
                raise TypeError('"accept", "listen", "socket" methods are not allowed')
        if 'get_message' in methods:
            pass
        else:
            raise TypeError('There are no function calls for working with sockets')
        super().__init__(clsname, bases, clsdict)


class WriterClientVerifier(type):

    def __init__(self, clsname, bases, clsdict):
        '''Метакласс проверки клиента для отправки сообщений на соответствие требованиям ТЗ'''
        methods = []
        for func in clsdict:
            try:
                ret = dis.get_instructions(clsdict[func])
            except TypeError:
                pass
            else:
                for i in ret:
                    if i.opname == 'LOAD_GLOBAL':
                        if i.argval not in methods:
                            methods.append(i.argval)
        for command in ('accept', 'listen', 'socket'):
            if command in methods:
                raise TypeError('"accept", "listen", "socket" methods are not allowed')
        if 'send_message' in methods:
            pass
        else:
            raise TypeError('There are no function calls for working with sockets')
        super().__init__(clsname, bases, clsdict)
