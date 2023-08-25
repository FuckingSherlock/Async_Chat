from sqlalchemy import Table, Column, Integer, String, MetaData, ForeignKey, DateTime, create_engine
from sqlalchemy.orm import registry, sessionmaker
import path
import os
import datetime
mapper_registry = registry()

os.chdir(path.Path(__file__).abspath().parent)

SERVER_DATABASE = 'sqlite:///clients.db'


class Storage:
    class Clients:
        def __init__(self, username):
            self.id = None
            self.name = username

    class ClientsInfo:
        def __init__(self, user_id, type_of_client, ip_address, port, last_login):
            self.id = None
            self.user = user_id
            self.type_of_client = type_of_client
            self.ip_address = ip_address
            self.port = port
            self.last_login = last_login

    def __init__(self):
        self.database_engine = create_engine(SERVER_DATABASE, echo=False, pool_recycle=7200)
        self.metadata = MetaData()

        users_table = Table(
            'All_Users', self.metadata,
            Column('id', Integer, primary_key=True),
            Column('name', String, unique=True),
        )

        users_info_table = Table(
            'Users_Info', self.metadata,
            Column('id', Integer, primary_key=True),
            Column('user', ForeignKey('All_Users.id'), unique=True),
            Column('type_of_client', String),
            Column('ip_address', String),
            Column('port', Integer),
            Column('last_login', DateTime),
        )

        self.metadata.create_all(self.database_engine)

        mapper_registry.map_imperatively(self.Clients, users_table)
        mapper_registry.map_imperatively(self.ClientsInfo, users_info_table)
        Session = sessionmaker(bind=self.database_engine)
        self.session = Session()

        self.session.query(self.ClientsInfo).delete()
        self.session.commit()

    def client_login(self, username, type_of_client, ip_address, port):
        print(username, type_of_client, ip_address, port)
        rez = self.session.query(self.Clients).filter_by(name=username)
        last_login_time = datetime.datetime.now()
        if rez.count():
            user = rez.first()
        else:
            user = self.Clients(username)
            self.session.add(user)
            self.session.commit()

        update_user_story = self.ClientsInfo(
            user.id, type_of_client, ip_address, port, last_login_time)
        self.session.add(update_user_story)
        self.session.commit()

    def client_logout(self, username):
        user = self.session.query(self.Clients).filter_by(name=username).first()
        self.session.query(self.ClientsInfo).filter_by(user=user.id).delete()
        self.session.commit()

    def clients_list(self):
        query = self.session.query(
            self.Clients.name,
            self.ClientsInfo.last_login,
        )
        return query.all()

    def client_info(self, username=None):
        query = self.session.query(self.Clients.name,
                                   self.ClientsInfo.last_login,
                                   self.ClientsInfo.ip_address,
                                   self.ClientsInfo.port
                                   ).join(self.Clients)
        if username:
            query = query.filter(self.Clients.name == username)
        return query.all()


if __name__ == '__main__':
    test_db = Storage()
    test_db.client_login('client_1', 'writer', '192.168.1.4', 8888)
    test_db.client_login('client_2', 'reader', '192.168.1.5', 7777)
    print(test_db.clients_list())
    test_db.client_logout('client_1')
    print(test_db.clients_list())
    test_db.client_info('client_1')
