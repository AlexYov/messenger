import sys
from PyQt5 import QtWidgets, QtCore
from ui_app_qui import *
from PyQt5.QtGui import QColor
import socket
import threading
import sqlite3
from time import sleep
import pickle
from rsa import Encrypt
from rsa import Decrypt
from rsa import Save_keys

# ссылка для настройки QTextEdit https://doc.qt.io/qt-5/stylesheet-reference.html

class Window_App(QtWidgets.QWidget):  
    
    mysignal1 = QtCore.pyqtSignal(QtCore.QVariant)
    mysignal2 = QtCore.pyqtSignal(QtCore.QVariant)
    
    def __init__(self, parent=None):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.server = ('192.168.0.102',1488)      
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client.connect(self.server)
        self.ui.textEdit.setStyleSheet("QTextEdit {color:black;font-size:12pt}")
        self.ui.pushButton.clicked.connect(self.get_message)
        self.mysignal1.connect(self.send)
        self.mysignal2.connect(self.show_new_message)
        threading.Thread(target=self.recieve).start()
        
    def show_new_message(self,mes):
        self.ui.textEdit.append(f'Собеседник: {mes}')
 
    def recieve(self):
        while True:
            data = self.client.recv(4096)
            sleep(0.1)
            self.mysignal2.emit(pickle.loads(Decrypt(data))) 
            
    def get_message(self):
        message = self.ui.plainTextEdit.toPlainText()
        sleep(0.1)
        self.mysignal1.emit(message)
        self.ui.textEdit.append(f'Вы: {message}')
        self.ui.plainTextEdit.clear()
        
    def send(self,message):  
        self.client.send(Encrypt(pickle.dumps(('user name', message))))
    
app = QtWidgets.QApplication(sys.argv)
window = Window_App()
window.setWindowFlags(QtCore.Qt.MSWindowsFixedSizeDialogHint)
Save_keys()
window.show()
sys.exit(app.exec_())

