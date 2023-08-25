from socket import *
from client_write import ClientWrite, set_username
from client_read import ClientRead, get_message, set_db
import sys
from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtWidgets import QWidget
import client_gui


class ClientApp(QtWidgets.QMainWindow, client_gui.Ui_MainWindow):
    def __init__(self, name):
        super().__init__()
        self.setupUi(self)
        # self.infoMsg.setText('INFO: Отправьте ваш логин сообщением')
        self.name = name
        self.write = ClientWrite(self.name)
        self.write.hello()
        self.secondThread = secondFlow(self.name)
        self.secondThread.changeChatAndInfo.connect(self.change_text)
        self.secondThread.start()
        self.db = self.secondThread.db

        self.inpMsg.setPlaceholderText("Введите сообщение")
        self.contacts = self.db.get_contacts()
        self.gui_contacts = []
        if isinstance(self.contacts, list):
            self.contacts = [i[0] for i in self.contacts]
            self.curr_recip = self.contacts[0]
            self.change_text([['INFO', 'database', self.contacts]])
        else:
            self.infoMsg.setText(f'INFO: {self.contacts}')
            self.contacts = ''
            self.curr_recip = ''

        self.sendButton.clicked.connect(lambda: self.send_msg('msg'))
        self.addButton.clicked.connect(lambda: self.send_msg('add_contact'))
        self.delButton.clicked.connect(lambda: self.send_msg('del_contact'))
        self.syncContactsButton.clicked.connect(lambda: self.send_msg('get_contacts'))
        self.contactsList.itemDoubleClicked.connect(self.change_recip)

    def change_recip(self, item):
        self.curr_recip = item.text()

    def send_msg(self, command):
        msg = self.inpMsg.text()
        if msg:
            self.write.send_message('msg', self.curr_recip, msg)
            self.gotMsg.append(f'{self.name}: {msg}\n')
            self.inpMsg.clear()
        if command != 'msg':
            self.write.send_message(command, 'server', msg)

    def change_text(self, msg):
        msg = msg[0]
        print(msg)
        msg_type, sender, text = msg[0], msg[1], msg[2]
        if sender == 'server':
            print('sender == server')
            if isinstance(text, list):
                print('\nсписок\n')
                for i in text:
                    if i not in self.gui_contacts:
                        self.gui_contacts.append(i)
                        print(self.gui_contacts)
                        self.contactsList.addItem(i)
                        self.db.add_contact(i)
            else:
                self.infoMsg.setText(f'INFO: {text}')
        elif isinstance(text, str):
            self.gotMsg.append(f'{sender}: {text}\n')


class secondFlow(QtCore.QThread):
    changeChatAndInfo = QtCore.pyqtSignal(list)

    def __init__(self, name, parent=None):
        super().__init__(parent)
        self.read = ClientRead(name)
        self.read.hello()
        self.db = self.read.db
        self.msg = ''

    def run(self):
        while True:
            self.msg = self.read.run()
            print(2, __name__, self.msg)
            if self.msg:
                self.changeChatAndInfo.emit([self.msg])
                self.msg = ''
                self.msleep(100)


def main():
    try:
        # user = 'user'
        user = sys.argv[1]
    except IndexError:
        user = ''
    finally:
        username = set_username(user)
        app = QtWidgets.QApplication(sys.argv)
        window = ClientApp(username)
        window.show()
        sys.exit(app.exec_())


if __name__ == '__main__':
    main()
