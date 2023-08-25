from sqlalchemy import Table, Column, Integer, String, MetaData, ForeignKey, DateTime, create_engine
from sqlalchemy.orm import registry, sessionmaker
import path
import os
import datetime
mapper_registry = registry()

os.chdir(path.Path(__file__).abspath().parent)

SERVER_DATABASE = 'sqlite:///client.db'


class Storage:
    class Contacts:
        def __init__(self, contact_name):
            self.id = None
            self.contact_name = contact_name

    class Messages:
        def __init__(self, sender, recip, message, time):
            self.id = None
            self.sender = sender
            self.recip = recip
            self.message = message
            self.time = time

    def __init__(self):
        self.database_engine = create_engine(SERVER_DATABASE, echo=False, pool_recycle=7200)
        self.metadata = MetaData()

        contacts_table = Table(
            'Contacts', self.metadata,
            Column('id', Integer, primary_key=True),
            Column('name', String, unique=True),
        )

        messages_table = Table(
            'Story_of_messages', self.metadata,
            Column('id', Integer, primary_key=True),
            Column('sender', String),
            Column('recipient', String),
            Column('message', String),
            Column('time', DateTime),
        )

        self.metadata.create_all(self.database_engine)

        mapper_registry.map_imperatively(self.Contacts, contacts_table)
        mapper_registry.map_imperatively(self.Messages, messages_table)
        Session = sessionmaker(bind=self.database_engine)
        self.session = Session()

        self.session.query(self.Messages).delete()
        self.session.commit()

    def save_message(self, sender, msg, recip):
        time = datetime.datetime.now()
        message = self.Messages(sender, recip, msg, time)
        self.session.add(message)
        self.session.commit()

    def add_contact(self, contact_name):
        rez = self.session.query(self.Contacts).filter_by(contact_name=contact_name)
        if not rez.count():
            self.session.add(self.Contacts(contact_name))
            self.session.commit()
            return f'Контакт {contact_name} успешно добавлен'
        else:
            return 'У вас уже есть этот контакт'

    # def get_contacts(self):
    #     query = self.session.query(self.Contacts.contact_name)
    #     if query:
    #         return query.all()
    #     else:
    #         return 'У вас нет контактов'

    def del_contact(self, contact_name):
        rez = self.session.query(self.Contacts.id).filter_by(contact_name=contact_name)
        if rez.count():
            rez.delete()
            return f'Контакт {contact_name} успешно удален'
        else:
            return 'Такого контакта нет в вашем списке'


# if __name__ == '__main__':
#     test_db = Storage()
