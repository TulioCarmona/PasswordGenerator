"""
Author: Marco Tulio Carmona Bellido
This programs simulates a client GUI which connects to a server, the GUI allow the user to request the latest password generated
17-06-2023
"""
import socket
import sys
import os
from datetime import datetime
from PyQt5.QtCore import QSize
from PyQt5.QtWidgets import (
    QApplication,
    QMainWindow,
    QVBoxLayout,
    QGridLayout,
    QLabel,
    QWidget,
    QPushButton,
    QMessageBox
)

host = 'localhost'
port = 12345

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)#socket config
sock.connect((host, port))
print(sock.recv(1024).decode())

#window configuration
class mainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Guardar contraseñas')
        main_layout = QVBoxLayout()
        control_layout = QGridLayout()

        btn_request = QPushButton('Solicitar Contraseña')
        btn_request.setFixedSize(QSize(200,60))
        btn_request.pressed.connect(self.pass_request)
        control_layout.addWidget(btn_request,0 ,0 )

        self.lbl_pwsd = QLabel("")
        control_layout.addWidget(self.lbl_pwsd, 1, 0)

        self.btn_save = QPushButton('Guardar')
        self.btn_save.pressed.connect(self.save_pswd)
        control_layout.addWidget(self.btn_save, 2, 0)

        main_layout.addLayout(control_layout)
        widget = QWidget()
        widget.setLayout(main_layout)
        self.setCentralWidget(widget)
        self.setFixedSize(250, 130)
        self.lbl_pwsd.hide()
        self.btn_save.hide()
        self.pswd = ''

    def pass_request(self): #request password function
        r = 'pp'
        sock.send(r.encode())
        try:
            ans = sock.recv(1024)
            self.pswd = ans.decode()
            self.lbl_pwsd.show()
            self.lbl_pwsd.setText(self.pswd)
            self.btn_save.show()
        except:
            print('Error al recibir datos')

    def save_pswd(self): #save to file function
        now = datetime.now()
        file = open('pswdHistoy.txt', 'a+') #leer y ageregar
        file.write('\n'+ str(now.date()) + '\t' + str(now.time()) + '\t' + self.pswd)
        file.close()
        loc = os.getcwd()
        loc += 'pswdhistory.txt'

        ok_board = QMessageBox()
        ok_board.setWindowTitle("Hecho!")
        msg = "La contraseña se guardo en:"
        ok_board.setText(msg)
        ok_board.setInformativeText(loc)
        ok_board.setStandardButtons(QMessageBox.Ok)
        ok_board.setIcon(QMessageBox.Information)
        ok_board.exec_()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = mainWindow()
    window.show()
    app.exec()
    sock.close()
    print('Conexion finalizada')