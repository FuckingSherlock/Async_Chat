from PyQt5 import QtCore, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(863, 457)

        self.gotMsg = QtWidgets.QTextBrowser(Dialog)
        self.gotMsg.setGeometry(QtCore.QRect(20, 20, 581, 291))
        self.gotMsg.setObjectName("gotMsg")

        self.sendButton = QtWidgets.QPushButton(Dialog)
        self.sendButton.setGeometry(QtCore.QRect(510, 330, 93, 41))
        self.sendButton.setObjectName("sendButton")

        self.inpMsg = QtWidgets.QLineEdit(Dialog)
        self.inpMsg.setGeometry(QtCore.QRect(20, 330, 471, 41))
        self.inpMsg.setObjectName("inpMsg")
        self.inpMsg.setPlaceholderText("Введите сообщение")

        self.addButton = QtWidgets.QPushButton(Dialog)
        self.addButton.setGeometry(QtCore.QRect(620, 330, 101, 41))
        self.addButton.setObjectName("addButton")

        self.delButton = QtWidgets.QPushButton(Dialog)
        self.delButton.setGeometry(QtCore.QRect(740, 330, 101, 41))
        self.delButton.setObjectName("delButton")

        self.contactsList = QtWidgets.QListWidget(Dialog)
        self.contactsList.setGeometry(QtCore.QRect(620, 20, 221, 291))
        self.contactsList.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAsNeeded)
        self.contactsList.setObjectName("contactsList")

        self.syncContactsButton = QtWidgets.QPushButton(Dialog)
        self.syncContactsButton.setGeometry(QtCore.QRect(620, 390, 221, 41))
        self.syncContactsButton.setObjectName("syncContactsButton")

        self.infoMsg = QtWidgets.QTextBrowser(Dialog)
        self.infoMsg.setGeometry(QtCore.QRect(20, 390, 581, 41))
        self.infoMsg.setObjectName("infoMsg")

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.sendButton.setText(_translate("Dialog", "SEND"))
        self.addButton.setText(_translate("Dialog", "ADD CONTACT"))
        self.delButton.setText(_translate("Dialog", "DEL CONTACT"))
        self.syncContactsButton.setText(_translate("Dialog", "SYNC CONTACTS"))
