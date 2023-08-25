from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Main(object):
    '''Основной класс GUI клиента'''

    def res_add(self, Main):
        '''Метод изменения размера окна для отображения/сокрытия списка подключенных к серверу клиентов'''
        Main.setFixedSize(1100, 450)

    def res_back(self, Main):
        '''Метод изменения размера окна для отображения/сокрытия списка подключенных к серверу клиентов'''
        Main.setFixedSize(860, 450)

    def setupUi(self, Main):
        '''Метод настройки GUI клиента'''
        Main.setObjectName("Main")
        Main.setFixedSize(860, 450)
        self.gotMsg = QtWidgets.QTextBrowser(Main)
        self.gotMsg.setGeometry(QtCore.QRect(20, 20, 581, 291))
        self.gotMsg.setObjectName("gotMsg")

        self.sendButton = QtWidgets.QPushButton(Main)
        self.sendButton.setGeometry(QtCore.QRect(510, 330, 93, 41))
        self.sendButton.setObjectName("sendButton")

        self.inpMsg = QtWidgets.QLineEdit(Main)
        self.inpMsg.setGeometry(QtCore.QRect(20, 330, 471, 41))
        self.inpMsg.setObjectName("inpMsg")
        self.inpMsg.setPlaceholderText("Введите сообщение")

        self.addButton = QtWidgets.QPushButton(Main)
        self.addButton.setGeometry(QtCore.QRect(620, 330, 101, 41))
        self.addButton.setObjectName("addButton")

        self.delButton = QtWidgets.QPushButton(Main)
        self.delButton.setGeometry(QtCore.QRect(740, 330, 101, 41))
        self.delButton.setObjectName("delButton")

        self.contactsList = QtWidgets.QListWidget(Main)
        self.contactsList.setGeometry(QtCore.QRect(620, 20, 221, 291))
        self.contactsList.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAsNeeded)
        self.contactsList.setObjectName("contactsList")

        self.syncContactsButton = QtWidgets.QPushButton(Main)
        self.syncContactsButton.setGeometry(QtCore.QRect(620, 390, 221, 41))
        self.syncContactsButton.setObjectName("syncContactsButton")

        self.infoMsg = QtWidgets.QTextBrowser(Main)
        self.infoMsg.setGeometry(QtCore.QRect(20, 390, 581, 41))
        self.infoMsg.setObjectName("infoMsg")

        self.ServerConnectedList = QtWidgets.QListWidget(Main)
        self.ServerConnectedList.setGeometry(QtCore.QRect(860, 20, 221, 351))
        self.ServerConnectedList.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAsNeeded)
        self.ServerConnectedList.setObjectName("ServerConnectedList")

        self.addButton_2 = QtWidgets.QPushButton(Main)
        self.addButton_2.setGeometry(QtCore.QRect(860, 390, 221, 41))
        self.addButton_2.setObjectName("addButton_2")

        self.retranslateUi(Main)
        QtCore.QMetaObject.connectSlotsByName(Main)

    def retranslateUi(self, Main):
        _translate = QtCore.QCoreApplication.translate
        Main.setWindowTitle(_translate("Main", "Dialog"))
        self.sendButton.setText(_translate("Main", "SEND"))
        self.addButton.setText(_translate("Main", "ADD CONTACT"))
        self.delButton.setText(_translate("Main", "DEL CONTACT"))
        self.syncContactsButton.setText(_translate("Main", "syncСontacts"))
        self.addButton_2.setText(_translate("Main", "ADD SELECTED CONTACTS"))
