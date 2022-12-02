from PyQt5 import QtWidgets, uic , QtCore, QtGui
import sys
import socket
from PyQt5.QtTest import QTest

#Configurações Janela Principal
class Ui_MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(Ui_MainWindow, self).__init__()
        uic.loadUi('InterfaceGrafica.ui', self)  # Carrega a janela principal

        # Botões Página Inicial
        self.button1 = self.findChild(QtWidgets.QPushButton, 'botao_Conexao')
        self.button2 = self.findChild(QtWidgets.QPushButton, 'botao_MoverBraco')
        self.button1.clicked.connect(self.botaoConexao)
        self.button2.clicked.connect(self.botaoMoverBraco)
        self.show()

        #Abrir página para conexão
    def botaoConexao(self):
        window.close()
        w2.show()

        # Abrir página para braço robótico
    def botaoMoverBraco(self):
        window.close()
        w3.show()

#Configurações Janela Conexão
class Ui_ConectWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(Ui_ConectWindow, self).__init__()

        uic.loadUi('InterfaceConectar.ui', self) #Abre pagina para conexão

        #Define botoes e entradas
        self.entrada1 = self.findChild(QtWidgets.QLineEdit, 'IP')
        self.entrada2 = self.findChild(QtWidgets.QLineEdit, 'Entrada')
        self.entrada3 = self.findChild(QtWidgets.QLineEdit, 'Envio')

        self.button1 = self.findChild(QtWidgets.QPushButton, 'botao_Conectar')
        self.button1.clicked.connect(self.realizarConexao)

        self.button2 = self.findChild(QtWidgets.QPushButton, 'botao_voltar')
        self.button2.clicked.connect(self.voltar)
    #Realiza conexao com Ip e porta definidos
    def realizarConexao(self):
        try:
            ip = self.entrada1.text() #coleta o ip digitado
            envio = int(self.entrada2.text()) #coleta a porta de envio digitada
            entrada = int(self.entrada3.text()) #coleta a porta de entrada digitada
            conexao.connect((ip, envio)) #estabelece a conexão
            print(f"Conectado ao IP: {ip}, Porta Envio: {envio}, Porta Entrada: {entrada}")
            window.show()

        except:
            print("Algo deu errado, tente novamente")

    def voltar(self):
        w2.close()
        window.show()

#Configurações Janela Envio dados para manopla
class Ui_MachineWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(Ui_MachineWindow, self).__init__()

        uic.loadUi('InterfaceBraco.ui', self) #Abre janela

        #Define botoes e entradas
        self.flork = self.findChild(QtWidgets.QLabel, 'flork')
        self.flork.setVisible(False)
        self.florkt = self.findChild(QtWidgets.QLabel, 'florkt')
        self.florkt.setVisible(False)
        self.slider1 = self.findChild(QtWidgets.QSlider, 'x_slider')
        self.slider2 = self.findChild(QtWidgets.QSlider, 'y_slider')
        self.slider3 = self.findChild(QtWidgets.QSlider, 'z_slider')

        self.saida1 = self.findChild(QtWidgets.QLabel, 'visor_x')
        self.saida2 = self.findChild(QtWidgets.QLabel, 'visor_y')
        self.saida3 = self.findChild(QtWidgets.QLabel, 'visor_z')


        #Configurações dos botões de Slider
        self.slider1.setMaximum(180)
        self.slider1.valueChanged.connect(self.visorx)

        self.slider2.setMaximum(180)
        self.slider2.valueChanged.connect(self.visory)

        self.slider3.setMaximum(180)
        self.slider3.valueChanged.connect(self.visorz)

        self.button1 = self.findChild(QtWidgets.QPushButton, 'botao_enviar')
        self.button1.clicked.connect(self.movimentarBraco)

        self.button2 = self.findChild(QtWidgets.QPushButton, 'botao_voltar')
        self.button2.clicked.connect(self.voltar)

        self.visor1 = self.findChild(QtWidgets.QLabel, 'visor_x_2')
        self.visor2 = self.findChild(QtWidgets.QLabel, 'visor_y_2')
        self.visor3 = self.findChild(QtWidgets.QLabel, 'visor_z_2')

        self.cb1 = self.findChild(QtWidgets.QCheckBox, "cb_x")
        self.cb2 = self.findChild(QtWidgets.QCheckBox, "cb_y")
        self.cb3 = self.findChild(QtWidgets.QCheckBox, "cb_z")

        self.msgc = self.findChild(QtWidgets.QLabel, "confirmar_msg")


    #Manda socket para braço se movimentar
    def movimentarBraco(self):
        try:
            posicao_x = str(self.saida1.text())
            posicao_y = str(self.saida2.text())
            posicao_z = str(self.saida3.text())

            # Gera uma string com as três informações de estado e a envia via Socket
            string = "{} {} {}".format(posicao_x, posicao_y, posicao_z)
            conexao.send(string.encode())

            msg = conexao.recv(1024) #Mensagem recebida
            msg_recebida = msg.decode()  # Lê a mensagem recebida
            split_msg = msg_recebida.split(" ", 2)  # Separa as informações recebidas

            msg_t[0] = split_msg[0]
            msg_t[1] = split_msg[1]
            msg_t[2] = split_msg[2]

            #Cria BackUp de Mensagens
            bkup[0].append(split_msg[0])
            bkup[1].append(split_msg[1])
            bkup[2].append(split_msg[2])

            # Estabelece critérios para caso o recebimento do sinal seja confirmado ou não
            if msg_t[0] != "":
                if bkup[0][-1] != bkup[0][-2]:
                    QTest.qWait(1000)
                    self.cb1.setChecked(True)
                    self.visor1.setText(msg_t[0])
                    self.visor1.setStyleSheet("background-color: green; color: white;")

            else:
                self.cb1.setChecked(False)
                self.visor1.setStyleSheet("background-color: red;")

            if msg_t[1] != "":
                if bkup[1][-1] != bkup[1][-2]:
                    QTest.qWait(1000)
                    self.cb2.setChecked(True)
                    self.visor2.setText(msg_t[1])
                    self.visor2.setStyleSheet("background-color: green; color: white;")
            else:
                self.cb2.setChecked(False)
                self.visor2.setStyleSheet("background-color: red;")

            if msg_t[2] != "":
                if bkup[2][-1] != bkup[2][-2]:
                    QTest.qWait(1000)
                    self.cb3.setChecked(True)
                    self.visor3.setText(msg_t[2])
                    self.visor3.setStyleSheet("background-color: green; color: white;")
            else:
                self.cb3.setChecked(False)
                self.visor3.setStyleSheet("background-color: red;")

            if msg_t[0] == "" and msg_t[1] == "" and msg_t[2] == "":
                self.msgc.setStyleSheet("color: red;")
                self.msgc.setText("Nenhum sinal recebido")
                self.florkt.setVisible(True)
                self.flork.setVisible(False)
            else:
                self.msgc.setStyleSheet("color: green;")
                self.msgc.setText("Sinal recebido!")
                self.flork.setVisible(True)

        except:
            self.msgc.setStyleSheet("color: red;")
            self.msgc.setText("Erro ao receber sinal")
            self.florkt.setVisible(True)
            self.flork.setVisible(False)
    def voltar(self):
        w3.close()
        window.show()

    def visorx(self, value):
        self.saida1.setText(str(value))
    def visory(self, value):
        self.saida2.setText(str(value))
    def visorz(self, value):
        self.saida3.setText(str(value))


if __name__ == "__main__":

    #Estancia as janelas do GUI e define as variáveis que serão utilizadas
    conexao = socket.socket() # Abre o servidor para conexão TCP
    app = QtWidgets.QApplication(sys.argv)
    window = Ui_MainWindow()
    w2 = Ui_ConectWindow()
    w3 = Ui_MachineWindow()
    msg_t = ["", "", ""]
    bkup = [[0, 1], [0, 1], [0, 1]]
    window.show()
    app.exec_()
