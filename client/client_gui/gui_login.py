from PyQt5 import QtCore, QtWidgets


class Ui_Login(object):
    '''Класс GUI входа клиента, принимает основной класс окна клиента'''

    def __init__(self, main):
        self.main_window = main

    def setupUi(self, Login):
        '''Метод настройки GUI входа клиента'''
        self.win = Login
        Login.setObjectName("Login")
        Login.resize(321, 167)
        self.loginButton = QtWidgets.QPushButton(Login)
        self.loginButton.setGeometry(QtCore.QRect(110, 120, 93, 31))
        self.loginButton.setObjectName("loginButton")
        self.loginButton.clicked.connect(self.login)

        self.passwordForm = QtWidgets.QLineEdit(Login)
        self.passwordForm.setGeometry(QtCore.QRect(31, 70, 256, 41))
        self.passwordForm.setObjectName("passwordForm")

        self.loginForm = QtWidgets.QLineEdit(Login)
        self.loginForm.setGeometry(QtCore.QRect(31, 22, 256, 41))
        self.loginForm.setObjectName("loginForm")

        self.retranslateUi(Login)
        QtCore.QMetaObject.connectSlotsByName(Login)

    def retranslateUi(self, Login):
        _translate = QtCore.QCoreApplication.translate
        Login.setWindowTitle(_translate("Login", "Dialog"))
        self.loginButton.setText(_translate("Login", "LOGIN"))
        self.passwordForm.setPlaceholderText(_translate("Login", "Enter password"))
        self.loginForm.setPlaceholderText(_translate("Login", "Enter login"))

    def login(self):
        '''Метод проверяет ввод логина и пароля клиентом и запускает основной GUI клиента'''
        if self.loginForm.text() and self.passwordForm:
            self.main_window.name = self.loginForm.text()
            self.main_window.password = self.passwordForm.text()
            self.main_window.run()
            self.main_window.show()
            self.win.close()
