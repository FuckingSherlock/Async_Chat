from sqlalchemy import Table, Column, Integer, String, MetaData, ForeignKey, DateTime, create_engine
from sqlalchemy.orm import registry, sessionmaker
import path
import os
import datetime
mapper_registry = registry()

os.chdir(path.Path(__file__).abspath().parent)

SERVER_DATABASE = 'sqlite:///server.db'

'''База данных сервера'''


class Storage:
    class Clients:
        def __init__(self, name_and_type, username, password_hash):
            '''Таблица клиентов, принимает: имя и тип клиента, имя пользователя, хэшированный пароль'''
            self.id = None
            self.name_and_type = name_and_type
            self.name = username
            self.password_hash = password_hash

    class ClientsInfo:
        def __init__(self, username, user_id, type_of_client, ip_address, port, last_login):
            '''Таблица подробной информации о клиентах.Принимает имя, id, имя+тип клиента, ip-адрес, порт клиента, время подключения'''
            self.id = None
            self.name = username
            self.user_id = user_id
            self.type_of_client = type_of_client
            self.ip_address = ip_address
            self.port = port
            self.last_login = last_login

    class ClientsContacts:
        def __init__(self, username, user_id, contact_name, contact_id):
            '''Таблица контактов, принимает имя пользователя, id пользователя, имя контакта, id контакта'''
            self.id = None
            self.username = username
            self.user_id = user_id
            self.contact_name = contact_name
            self.contact_id = contact_id

    def __init__(self):
        self.database_engine = create_engine(SERVER_DATABASE, echo=False, pool_recycle=7200)
        self.metadata = MetaData()

        users_table = Table(
            'All_Users', self.metadata,
            Column('id', Integer, primary_key=True),
            Column('name_and_type', String, unique=True),
            Column('name', String),
            Column('password_hash', String),
        )

        users_info_table = Table(
            'Users_Info', self.metadata,
            Column('id', Integer, primary_key=True),
            Column('name', String),
            Column('user_id', ForeignKey('All_Users.id'), unique=True),
            Column('type_of_client', String),
            Column('ip_address', String),
            Column('port', Integer),
            Column('last_login', DateTime),
        )

        contacts_table = Table(
            'Contacts', self.metadata,
            Column('id', Integer, primary_key=True),
            Column('username', ForeignKey('Users_Info.name')),
            Column('user_id', ForeignKey('All_Users.id')),
            Column('contact_name', String),
            Column('contact_id', ForeignKey('Users_Info.user_id')),
        )

        self.metadata.create_all(self.database_engine)

        mapper_registry.map_imperatively(self.Clients, users_table)
        mapper_registry.map_imperatively(self.ClientsInfo, users_info_table)
        mapper_registry.map_imperatively(self.ClientsContacts, contacts_table)
        Session = sessionmaker(bind=self.database_engine)
        self.session = Session()

        self.session.query(self.ClientsInfo).delete()
        self.session.commit()

    def client_login(self, username, type_of_client, ip_address, port, pwd):
        '''Метод добавления подключенных клиентов в БД.
        Принимает имя клиента, имя и тип клиента, ip-адрес клиента, порт клиента, хэшированный пароль'''
        print(username, type_of_client, ip_address, port)
        rez = self.session.query(self.Clients).filter_by(name_and_type=username+type_of_client)
        last_login_time = datetime.datetime.now()
        if rez.count():
            user = rez.first()
        else:
            user = self.Clients(username+type_of_client, username, pwd)
            self.session.add(user)
            self.session.commit()

        update_user_story = self.ClientsInfo(
            username, user.id, type_of_client, ip_address, port, last_login_time)
        self.session.add(update_user_story)
        self.session.commit()

    def add_contact(self, username, contact_name):
        '''Метод добавления контактов. Принимает имя пользователя и имя контакта.'''
        rez = self.session.query(self.ClientsContacts).filter_by(
            username=username, contact_name=contact_name)
        if not rez.count():
            user_id = self.session.query(
                self.ClientsInfo.user_id).filter_by(name=username).first()[0]
            try:
                contact_id = self.session.query(self.ClientsInfo.user_id).filter_by(
                    name=contact_name, type_of_client='reader').first()[0]
            except:
                return [f'Пользователя с именем {contact_name} не существует', contact_name]

            update_contacts = self.ClientsContacts(username, user_id, contact_name, contact_id)
            self.session.add(update_contacts)
            self.session.commit()
            return [f'Контакт {contact_name} успешно добавлен', contact_name]
        else:
            return [f'Пользователь {contact_name} вас уже есть в контактах', contact_name]

    def get_contacts(self, username):
        '''Метод получения контактов из таблицы.'''
        query = self.session.query(self.ClientsContacts.contact_name).filter_by(username=username)
        if query.count():
            return query.all()
        else:
            return 'У вас нет контактов'

    def del_contact(self, username, contact_name):
        '''Метод удаления контакта. Принимает имя клиента и имя контакта'''
        rez = self.session.query(self.ClientsContacts.id).filter_by(
            username=username, contact_name=contact_name)
        if rez.count():
            rez.delete()
            return [f'Контакт {contact_name} успешно удален', contact_name]
        else:
            return [f'Пользователя с именем {contact_name}  нет в вашем списке', contact_name]

    def client_logout(self, username):
        '''Метод удаления отключившегося клиента'''
        user = self.session.query(self.Clients.name).filter_by(name=username).first()
        self.session.query(self.ClientsInfo).filter_by(name=username).delete()
        self.session.commit()
        return user

    def clients_list(self):
        '''Метод получения всех клиентов подключавшихся к серверу'''
        query = self.session.query(
            self.Clients.name_and_type,
        )
        if query.count():
            return query.all()
        else:
            return ''

    def get_client_pwd(self, name_and_type):
        '''Метод получения сохраненного в БД пароля клиента, принимает имя и тип клиента'''
        query = self.session.query(self.Clients.password_hash).filter_by(
            name_and_type=name_and_type)
        if query.count():
            return query.first()

    def get_connected(self):
        '''Метод получения подключенных клиентов'''
        query = self.session.query(
            self.ClientsInfo.name,
        )
        return query.all()

    def client_info(self, username=None):
        '''Метод получения информации о клиенте, принимает имя клиента'''
        query = self.session.query(self.Clients.name,
                                   self.ClientsInfo.last_login,
                                   self.ClientsInfo.ip_address,
                                   self.ClientsInfo.port
                                   ).join(self.Clients)
        if username:
            query = query.filter(self.Clients.name == username)
        return query.all()


# if __name__ == '__main__':
#     test_db = Storage()
#     test_db.client_login('user_11', 'writer', '192.168.1.4', 8888, '11')
#     test_db.client_login('client_2', 'reader', '192.168.1.5', 7777)
#     print(test_db.clients_list())
#     # test_db.client_logout('client_1')
#     print(test_db.clients_list())
#     test_db.client_info('client_1')
#     test_db.add_contact('client_1', 'client_2')
#     test_db.get_contacts('client_1')
