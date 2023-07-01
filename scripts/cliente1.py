"""
Author: Marco Tulio Carmona Bellido
This programs simulates a client GUI which connects to a server, the GUI gives the user the option to modify the desired password parameters
17-06-2023
"""
import sys
import socket
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (
    QApplication,
    QMainWindow,
    QVBoxLayout,
    QGridLayout,
    QLabel,
    QWidget,
    QSpinBox,
    QDoubleSpinBox,
    QComboBox,
    QPushButton,
    QMessageBox,
    QFileDialog,
    QLineEdit,
    QGroupBox,
    QRadioButton,
    QCheckBox,
    QSlider
)

android = "⠄⠄⠄⠄⢠⣿⣿⣿⣿⣿⢻⣿⣿⣿⣿⣿⣿⣿⣿⣯⢻⣿⣿⣿⣿⣆⠄⠄⠄\n⠄⠄⣼⢀⣿⣿⣿⣿⣏⡏⠄⠹⣿⣿⣿⣿⣿⣿⣿⣿⣧⢻⣿⣿⣿⣿⡆⠄⠄\n⠄⠄⡟⣼⣿⣿⣿⣿⣿⠄⠄⠄⠈⠻⣿⣿⣿⣿⣿⣿⣿⣇⢻⣿⣿⣿⣿⠄⠄\n⠄⢰⠃⣿⣿⠿⣿⣿⣿⠄⠄⠄⠄⠄⠄⠙⠿⣿⣿⣿⣿⣿⠄⢿⣿⣿⣿⡄⠄\n⠄⢸⢠⣿⣿⣧⡙⣿⣿⡆⠄⠄⠄⠄⠄⠄⠄⠈⠛⢿⣿⣿⡇⠸⣿⡿⣸⡇⠄\n⠄⠈⡆⣿⣿⣿⣿⣦⡙⠳⠄⠄⠄⠄⠄⠄⢀⣠⣤⣀⣈⠙⠃⠄⠿⢇⣿⡇⠄\n⠄⠄⡇⢿⣿⣿⣿⣿⡇⠄⠄⠄⠄⠄⣠⣶⣿⣿⣿⣿⣿⣿⣷⣆⡀⣼⣿⡇⠄\n⠄⠄⢹⡘⣿⣿⣿⢿⣷⡀⠄⢀⣴⣾⣟⠉⠉⠉⠉⣽⣿⣿⣿⣿⠇⢹⣿⠃⠄\n⠄⠄⠄⢷⡘⢿⣿⣎⢻⣷⠰⣿⣿⣿⣿⣦⣀⣀⣴⣿⣿⣿⠟⢫⡾⢸⡟⠄.\n⠄⠄⠄⠄⠻⣦⡙⠿⣧⠙⢷⠙⠻⠿⢿⡿⠿⠿⠛⠋⠉⠄⠂⠘⠁⠞⠄⠄⠄\n⠄⠄⠄⠄⠄⠈⠙⠑⣠⣤⣴⡖⠄⠿⣋⣉⣉⡁⠄⢾⣦⠄⠄⠄⠄⠄⠄⠄⠄"

#window configuration
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Generador de Contraseñas")
        main_layout = QVBoxLayout()
        control_layout = QGridLayout()
        control_layout2 = QGridLayout()
        control_layout3 = QGridLayout()
        lbl1 = QLabel("-----> Configuración de parametros <-----")
        lbl1.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(lbl1)
        group_box = QGroupBox("Opciones")
        options_layout = QVBoxLayout()

        lbl_PassLen = QLabel("Numero de caracteres de la contraseña")
        control_layout.addWidget(lbl_PassLen, 0, 0) # y_pos, x_pos, ¿?, x_len

        sld_passLen = QSlider(Qt.Horizontal)
        sld_passLen.setFocusPolicy(Qt.StrongFocus)
        sld_passLen.setTickPosition(QSlider.TicksBelow)
        sld_passLen.setMaximum(50)
        sld_passLen.setTickInterval(5)
        sld_passLen.setSingleStep(1)
        sld_passLen.valueChanged.connect(self.passLen_change)
        control_layout.addWidget(sld_passLen, 1, 0)

        lbl_void2 = QLabel("     ")
        control_layout.addWidget(lbl_void2, 1, 1)

        self.lbl_sldValue = QLabel("")
        self.lbl_sldValue.setAlignment(Qt.AlignLeft)
        control_layout.addWidget(self.lbl_sldValue, 1, 2)

        self.ckb_mayus = QCheckBox("Mayusculas")
        self.ckb_mayus.stateChanged.connect(self.show_mayus_spb)
        control_layout2.addWidget(self.ckb_mayus, 0, 0)

        self.spb_mayus = QSpinBox()
        self.spb_mayus.setMinimum(0)
        self.spb_mayus.setAlignment(Qt.AlignRight)
        self.spb_mayus.valueChanged.connect(self.set_mayus_num)
        control_layout2.addWidget(self.spb_mayus, 1, 0)


        self.ckb_sc = QCheckBox("Carcateres Especiales") #sc: special character
        self.ckb_sc.stateChanged.connect(self.show_sc_spb)
        control_layout2.addWidget(self.ckb_sc, 0, 1)

        self.spb_sc = QSpinBox()
        self.spb_sc.setMinimum(0)
        self.spb_sc.setAlignment(Qt.AlignRight)
        self.spb_sc.valueChanged.connect(self.set_sc_num)
        control_layout2.addWidget(self.spb_sc, 1, 1)

        self.ckb_num = QCheckBox("Numeros")
        self.ckb_num.stateChanged.connect(self.show_num_spb)
        control_layout2.addWidget(self.ckb_num, 0, 2)

        self.spb_num = QSpinBox()
        self.spb_num.setMinimum(0)
        self.spb_num.setAlignment(Qt.AlignRight)
        self.spb_num.valueChanged.connect(self.set_num_num)
        control_layout2.addWidget(self.spb_num, 1, 2)

        btn_generate = QPushButton("Generar")
        btn_generate.setStyleSheet("background-color : Teal")
        btn_generate.pressed.connect(self.send_parameters)
        control_layout3.addWidget(btn_generate, 0, 0, 1, 2)

        self.new_pswd = QLineEdit("")
        control_layout3.addWidget(self.new_pswd, 1, 0, 1, 2)

        lbl_void = QLabel("")
        control_layout3.addWidget(lbl_void, 2, 0)

        self.btn_save = QPushButton("Guardar")
        self.btn_save.pressed.connect(self.save_pswd)
        control_layout3.addWidget(self.btn_save, 2, 1)

        options_layout.addLayout(control_layout2)
        group_box.setLayout(options_layout)
        main_layout.addLayout(control_layout)
        main_layout.addWidget(group_box)
        main_layout.addLayout(control_layout3)
        widget = QWidget()
        widget.setLayout(main_layout)
        self.setCentralWidget(widget)

        self.spb_mayus.hide()
        self.spb_sc.hide()
        self.spb_num.hide()
        self.new_pswd.hide()
        self.btn_save.hide()
        self.passLen = 0
        self.numMayus = 0
        self.scNum = 0
        self.numNum = 0
        self.pswd = ""

    def passLen_change(self, pLen):
        self.passLen = pLen
        self.lbl_sldValue.setText(str(pLen))

    def show_mayus_spb(self):
        if self.ckb_mayus.isChecked():
            self.spb_mayus.show()
        else:
            self.spb_mayus.hide()
            self.numMayus = 0
            self.spb_mayus.setValue(0)

    def set_mayus_num(self, num):
        self.numMayus = num

    def show_sc_spb(self):
        if self.ckb_sc.isChecked():
            self.spb_sc.show()
        else:
            self.spb_sc.hide()
            self.scNum = 0
            self.spb_sc.setValue(0)

    def set_sc_num(self, num):
        self.scNum = num

    def show_num_spb(self):
        if self.ckb_num.isChecked():
            self.spb_num.show()
        else:
            self.spb_num.hide()
            self.numNum = 0
            self.spb_num.setValue(0)

    def set_num_num(self, num):
        self.numNum = num

    def send_parameters(self): #send parameters
        if self.passLen > (self.numMayus + self.scNum + self.numNum):
            self.new_pswd.show()
            print(self.passLen, self.numMayus, self.scNum, self.numNum)
            #converts parameters into string to be send to the server
            self.pswd = str(self.passLen) + ',' + str(self.numMayus) + ',' + str(self.scNum) + ',' + str(self.numNum)
            sock.send(self.pswd.encode())
            ans = sock.recv(1024)
            self.new_pswd.setText(ans.decode())
            self.btn_save.show()
        else:
            er_board = QMessageBox()
            er_board.setWindowTitle("Error!")
            msg = "El numero de caracteres de la contraseña es menor"
            msg += " que el numero de caractrees especiales seleccionados"
            msg2 = "Error al generar la contraseña"
            er_board.setText(msg2)
            er_board.setInformativeText(msg)
            er_board.setStandardButtons(QMessageBox.Ok)
            er_board.setIcon(QMessageBox.Critical)
            er_board.exec_()

    def save_pswd(self): #save to file function
        data = self.new_pswd.text()
        sock.send(data.encode())

        dir = QFileDialog.getSaveFileName()
        #print(dir[0])
        file = open(dir[0], 'w', encoding='utf-8')
        file.write(data)
        file.write("\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n")
        file.write(android)  #just for fun :), look at the end of the file you saved
        file.close()

        ok_board = QMessageBox()
        ok_board.setWindowTitle("Hecho!")
        msg = "La contraseña se guardo exitosamente"
        msg2 = '>w<'
        ok_board.setText(msg)
        ok_board.setInformativeText(msg2)
        ok_board.setStandardButtons(QMessageBox.Ok)
        ok_board.setIcon(QMessageBox.Information)
        ok_board.exec_()

# Client config
host = 'localhost'  # server's ip address
port = 12345  # server port

# Create a TCP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #socket config

# connect to server
sock.connect((host, port))
print(sock.recv(1024).decode())

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    app.exec()
    sock.close()
    print('Conexion finalizada')