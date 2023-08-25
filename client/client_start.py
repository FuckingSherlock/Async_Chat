from socket import *
from client_write import ClientWrite
from client_read import ClientRead
import sys
import time
from PyQt5 import QtWidgets, QtCore
from client_gui.gui_main import Ui_Main
from client_gui.gui_login import Ui_Login


class ClientApp(QtWidgets.QMainWindow, Ui_Main):
    """
    Client app main Class

    Attributes
    ----------
    name : str
    password : str
    """

    def __init__(self):
        super().__init__()
        self.name = ''
        self.password = ''

    def run(self):
        """
        Запуск основного потока клиента
        """
        self.setupUi(self)
        self.secondThread = secondFlow(self.name, self.password)
        self.write = ClientWrite(self.name, self.password)
        self.write.hello()
        self.secondThread.changeChatAndInfo.connect(self.change_text)
        self.secondThread.start()
        self.db = self.secondThread.db

        self.adding = ''
        self.contacts = self.db.get_contacts()
        self.gui_contacts = []
        self.server_connected = []
        if isinstance(self.contacts, list):
            self.contacts = [i[0] for i in self.contacts]
            self.curr_recip = self.contacts[0]
            self.change_text([['INFO', 'database', self.contacts]])
        else:
            self.infoMsg.setText(f'INFO: {self.contacts}')
            self.contacts = ''
            self.curr_recip = ''
        self.sendButton.clicked.connect(lambda: self.send_msg('msg'))
        self.delButton.clicked.connect(lambda: self.send_msg('del_contact'))
        self.syncContactsButton.clicked.connect(lambda: self.send_msg('sync_contacts'))
        self.contactsList.itemDoubleClicked.connect(self.change_recip)
        self.ServerConnectedList.itemClicked.connect(self.change_add)
        self.addButton.clicked.connect(self.first_add_contact)
        self.addButton_2.clicked.connect(self.second_add_contact)

    def first_add_contact(self):
        """Начало добавления контакта"""
        self.send_msg('get_connected')
        self.res_add(self)

    def change_add(self, item):
        '''
        Выбор добавляемого контакта

            Parameters
            ----------
            item : QListWidgetItem
        '''
        self.adding = item.text()

    def second_add_contact(self):
        '''
        Добавление выбранного контакта
        '''
        if self.adding:
            if self.adding == self.name:
                self.infoMsg.setText(f'INFO: Вы не можете добавить в контакты самого себя')
            else:
                self.send_msg('add_contact', self.adding)
                self.contactsList.addItem(self.adding)
                self.res_back(self)
        self.adding = ''

    def change_recip(self, item):
        '''
        Выбор получателя сообщения

            Parameters
            ----------
            item : QListWidgetItem
        '''
        self.gotMsg.clear()
        self.curr_recip = item.text()
        self.gotMsg.append(f'Чат с {self.curr_recip}')

    def sync_contacts(self):
        '''
        Синхронизировать контакты c сервером

        '''
        if isinstance(self.contacts, list):
            for name in self.contacts:
                self.send_msg('sync_contacts', name=name)

    def send_msg(self, command, name=None):
        '''
        Отправить сообщение

        Parameters
        ----------
        command : str
        name : str
        '''
        if command == 'add_contact':
            self.write.send_message(command, 'server', name)
            return
        elif command == 'del_contact':
            self.write.send_message(command, 'server', self.curr_recip)
        elif command == 'get_connected':
            self.write.send_message(command, 'server', '')
        elif command == 'msg':
            msg = self.inpMsg.text()
            if msg:
                self.write.send_message('msg', self.curr_recip, msg)
                self.gotMsg.append(f'Вы ({self.name}): {msg}\n')
                self.inpMsg.clear()
        elif command == 'sync_contacts':
            self.write.send_message(command, 'server', name)

    def update_msg_story(self):
        pass

    def change_text(self, msg):
        '''
        Обновить текст сообщений

        Parameters
        ----------
        msg : list
        '''
        msg = msg[0]
        act = ''
        print(msg)
        msg_type, sender, text = msg[0], msg[1], msg[2]
        try:
            act = msg[3]
        except:
            pass
        if sender == 'server' or sender == 'database':
            if isinstance(text, list):
                if act == 'INFO':
                    self.infoMsg.setText(f'INFO: {text}')
                    if text == 'Вы ввели неверный пароль':  # хз как кильнуть
                        time.sleep(1)
                        sys.exit(app.exec_())
                        win.close()
                elif act == 'get_connected':
                    for i in text:
                        if i not in self.server_connected:
                            self.server_connected.append(i)
                            print(self.server_connected)
                            self.ServerConnectedList.addItem(i)
                else:
                    for i in text:
                        if i not in self.gui_contacts:
                            self.gui_contacts.append(i)
                            print(self.gui_contacts)
                            self.contactsList.addItem(i)
                            self.db.add_contact(i)
            else:
                self.infoMsg.setText(f'INFO: {text}')
        elif isinstance(text, str):
            if sender != self.name:
                self.gotMsg.append(f'{sender}: {text}\n')


class secondFlow(QtCore.QThread):
    """
    Дополнительный поток клиента для чения сообщений
    """
    changeChatAndInfo = QtCore.pyqtSignal(list)

    def __init__(self, name, pwd, parent=None):
        '''
        Parameters
        ----------
        name : str
        pwd : str
        '''
        super().__init__(parent)
        self.read = ClientRead(name, pwd)
        self.read.hello()
        self.db = self.read.db
        self.msg = ''

    def run(self):
        '''
        Запуск потока клиента
        '''
        time.sleep(2)
        while True:
            self.msg = self.read.run()
            if self.msg:
                print(2, __name__, self.msg)
                self.changeChatAndInfo.emit([self.msg])
                self.msg = ''
                self.msleep(100)


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    win = QtWidgets.QDialog()
    enter_ui = Ui_Login(ClientApp())
    enter_ui.setupUi(win)
    win.show()
    sys.exit(app.exec_())
