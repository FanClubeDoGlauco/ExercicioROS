import customtkinter
from ctypes import *
from PIL import Image, ImageTk
import os

# Classe com toda as definições dentro do aplicativo e suas funções
class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        # configure window
        self.title("EPOS CONNECTION")
        self.geometry(f"{1000}x{580}")

        # configure grid layout (4x4)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure((2, 3), weight=0)
        self.grid_rowconfigure((0, 1, 2), weight=1)

        # create sidebar frame with widgets
        # Options Bar
        self.sidebar_frame = customtkinter.CTkFrame(self, width=140, height=800, corner_radius=10)
        self.sidebar_frame.grid(row=0, column=0, rowspan=10, sticky="nsew")
        self.sidebar_frame.grid_rowconfigure(4, weight=1)
        self.logo_label = customtkinter.CTkLabel(self.sidebar_frame, text="Options",
                                                 font=customtkinter.CTkFont(size=20, weight="bold"))
        self.logo_label.grid(row=0, column=0, padx=20, pady=(20, 10))
        # Buttons

        self.sidebar_button_2 = customtkinter.CTkButton(self.sidebar_frame,
                                                        text="Enviar Comando Step", command=self.movimentar)
        self.sidebar_button_2.grid(row=2, column=0, padx=20, pady=10)

        self.sidebar_button_3 = customtkinter.CTkButton(self.sidebar_frame,
                                                        text="Enviar Comando Velocidade", command=self.velocidade)

        self.sidebar_button_3.grid(row=3, column=0, padx=20, pady=10)

        self.sidebar_button_4 = customtkinter.CTkButton(self.sidebar_frame,
                                                        text="Parar Motor", command=self.stop)
        self.sidebar_button_4.grid(row=4, column=0, padx=20, pady=10)

        self.florkimg1 = ImageTk.PhotoImage(Image.open("flork.jpg").resize((150, 150)))
        self.florkimg2 = ImageTk.PhotoImage(Image.open("florkt.png").resize((150, 150)))
        self.sidebar_img = customtkinter.CTkLabel(self.sidebar_frame, width=80, text="")
        self.sidebar_img.grid(row=5, column=0, padx=20, pady=10)

        # Scaling menu
        self.scaling_label = customtkinter.CTkLabel(self.sidebar_frame, text="UI Scaling:", anchor="w")
        self.scaling_label.grid(row=7, column=0, padx=20, pady=10)
        self.scaling_optionemenu = customtkinter.CTkOptionMenu(self.sidebar_frame,
                                                               values=["80%", "90%", "100%", "110%", "120%"],
                                                               command=self.change_scaling_event)
        self.scaling_optionemenu.grid(row=8, column=0, padx=20, pady=10)

        # create textbox
        self.commandframe = customtkinter.CTkFrame(self, width=200, height=100)
        self.commandframe.grid(row=1, column=1, columnspan=1, padx=(20, 0), pady=(20, 0), sticky="nsew")
        self.commandframe.grid_columnconfigure(0, weight=1)
        self.commandframe.grid_rowconfigure(4, weight=1)
        self.textbox = customtkinter.CTkTextbox(self.commandframe, width=200, height=150)
        self.textbox.grid(row=0, column=0, padx=(20, 0), pady=(20, 0), sticky="nsew")
        self.labelterminal = customtkinter.CTkLabel(self.commandframe, text="History", width=30, height=10)
        self.labelterminal.grid(row=1, column=0, padx=(20, 0), pady=(20, 0), sticky="nsew")
        self.terminal = customtkinter.CTkTextbox(self.commandframe, width=200, height=450)
        self.terminal.grid(row=2, column=0, padx=(20, 0), pady=(20, 0), sticky="nsew")

        # create tabview
        self.connection = customtkinter.CTkFrame(self,  width=200, height=100)
        self.connection.grid(row=1, column=2, columnspan=2, rowspan=3, padx=(20, 0), pady=(20, 0), sticky="nsew")
        self.devicelabel = customtkinter.CTkLabel(self.connection, width=200, text="Device Name")
        self.devicelabel.grid(row=1, column=0, padx=20, pady=10)
        self.devicename = customtkinter.CTkOptionMenu(self.connection,
                                                      values=["EPOS", "EPOS1", "EPOS2", "EPOS3", "EPOS4"], width=200)
        self.devicename.grid(row=2, column=0, padx=20, pady=10)
        self.protocollabel = customtkinter.CTkLabel(self.connection, width=200, text="Protocol")
        self.protocollabel.grid(row=3, column=0, padx=20, pady=10)
        self.protocol = customtkinter.CTkOptionMenu(self.connection,
                                                    values=["MAXON_RS232", "MAXON SERIAL V2", "CANopen"], width=200)
        self.protocol.grid(row=4, column=0, padx=20, pady=10)
        self.interfacenamelabel = customtkinter.CTkLabel(self.connection, width=200, text="Interface Name")
        self.interfacenamelabel.grid(row=5, column=0, padx=20, pady=10)
        self.interfacename = customtkinter.CTkOptionMenu(self.connection,
                                                         values=["RS232", "USB"],
                                                         width=200,
                                                         command=self.change_port_name)
        self.interfacename.grid(row=6, column=0, padx=20, pady=10)
        self.portnamelabel = customtkinter.CTkLabel(self.connection, width=200, text="Port")
        self.portnamelabel.grid(row=7, column=0, padx=20, pady=10)
        self.portname = customtkinter.CTkOptionMenu(self.connection,
                                                         values=["COM0", "COM1", "COM2", "COM4", "COM5"], width=200)
        self.portname.grid(row=8, column=0, padx=20, pady=10)

        # create slider and progressbar frame
        self.slider_progressbar_frame = customtkinter.CTkFrame(self,  width=120)
        self.slider_progressbar_frame.grid(row=4, column=1, columnspan=3, padx=(20, 0), pady=(20, 0), sticky="nsew")
        self.slider_progressbar_frame.grid_columnconfigure(0, weight=1)
        self.slider_progressbar_frame.grid_rowconfigure(4, weight=1)
        self.progressbar_1 = customtkinter.CTkProgressBar(self.slider_progressbar_frame, width=1000)
        self.progressbar_1.grid(row=1, column=0, padx=(20, 10), pady=(10, 10), sticky="ew")
        self.slider_1 = customtkinter.CTkSlider(self.slider_progressbar_frame, from_=0, to=50000, number_of_steps=50000,
                                                command=self.change_x)
        self.slider_1.grid(row=3, column=0, padx=(20, 10), pady=(10, 10), sticky="ew")
        self.slider_2 = customtkinter.CTkSlider(self.slider_progressbar_frame, from_=0, to=1000, number_of_steps=1000,
                                                command=self.change_x2)
        self.slider_2.grid(row=4, column=0, padx=(20, 10), pady=(10, 10), sticky="ew")
        self.slider_label1 = customtkinter.CTkLabel(self.slider_progressbar_frame, text="Steps:", anchor="w")
        self.slider_label1.grid(row=3, column=1, padx=20, pady=10)
        self.xtext = customtkinter.CTkTextbox(self.slider_progressbar_frame, height=20, width=90)
        self.xtext.grid(row=3, column=2, padx=10, pady=10)
        self.xtext.insert("0.0", "0")

        self.slider_label2 = customtkinter.CTkLabel(self.slider_progressbar_frame, text="Velocity:", anchor="w")
        self.slider_label2.grid(row=4, column=1, padx=20, pady=10)
        self.xtext2 = customtkinter.CTkTextbox(self.slider_progressbar_frame, height=20, width=90)
        self.xtext2.grid(row=4, column=2, padx=10, pady=10)
        self.xtext2.insert("0.0", "0")

        # set default values
        self.scaling_optionemenu.set("100%")

        self.progressbar_1.configure(mode="indeterminnate")
        self.progressbar_1.start()

        self.textbox.insert("0.0", "Este aplicativo foi criado para o projeto de Sistemas Embarcados do Professor Glauco\n\n"
                            + "Para utilizá-lo no perfil de posição: selecione as especificações da conexão. Estas podem ser encontradas pelo software EPOS Studio" +
                            "Após definir a conexão, marque a quantidade de steps que deseja enviar e clique no botão" +
                            "'Enviar Comando Step' para enviar o comando desejado para o sistema" +
                            "Para utilizá-lo no perfil de velocidade:" +
                            "marque a quantidade de steps que deseja enviar e clique no botão" +
                            "'Enviar Comando Velocidade' para enviar o comando desejado para o sistema"
                            )
        self.textbox.configure(state='disabled')
        self.terminal.configure(bg_color="white", text_color="yellow", state='disabled')
        self.xtext.configure(state='disabled')

        self.progressbar_1.configure(progress_color="red")

    # Mudando Scale do Aplicativo
    def change_scaling_event(self, new_scaling: str):
        new_scaling_float = int(new_scaling.replace("%", "")) / 100
        customtkinter.set_widget_scaling(new_scaling_float)
        self.terminal.configure(state='normal')
        self.terminal.insert("0.0", f"Aplicativo redimensionado para {new_scaling}\n\n")
        self.terminal.configure(state='disabled')

    # Função para mandar coordenadas ao sistema embarcado. O Mesmo descrito neste bloco serve para 'velocidade' e 'stop'
    def movimentar(self):

                #Define, em bytes os parâmetros para conexão serial com a controladora e a quantidade de steps que
                #Será mandada. Todos os dados são definidos no app
                Steps = int(self.xtext.get("0.0", '100.0')[0:-3])
                DeviceName = bytes(self.devicename.get().lstrip(), "utf-8")
                Protocol = bytes(self.protocol.get().lstrip(), "utf-8")
                Interface = bytes(self.interfacename.get().lstrip(), "utf-8")
                Port = bytes(self.portname.get().lstrip(), "utf-8")

                #Node de conexão. Pode ser obtido no EPOS Studio
                NodeID = 2
                keyhandle = 0
                # return variable from Library Functions
                ret = 0
                pErrorCode = c_uint()
                pDeviceErrorCode = c_uint()

                #Conecta ao controlador e retorna 0 ou != 0
                keyhandle = epos.VCS_OpenDevice(DeviceName, Protocol, Interface, Port, byref(pErrorCode))

                if keyhandle != 0:

                    # Device Error Evaluation
                    if pDeviceErrorCode.value == 0:

                        #Coloca o motor no perfil de Posição e envia a posição desejada
                        ret = epos.VCS_ActivateProfilePositionMode(keyhandle, NodeID, byref(pErrorCode))
                        ret = epos.VCS_MoveToPosition(keyhandle, NodeID, Steps, 0, 0, byref(pErrorCode))
                        ret = 1

                        self.terminal.configure(state='normal')
                        self.terminal.insert("0.0", "Cyclic movemenent finished \n")
                        self.terminal.insert("0.0", f"Steps: {Steps} \n")
                        self.progressbar_1.configure(progress_color="green")
                        self.sidebar_img.configure(image=self.florkimg1)

                    else:
                        print(pErrorCode.value)
                        self.terminal.insert("0.0", f"{pErrorCode.value} \n")
                        self.terminal.insert("0.0",
                                             f"EPOS Error Description can be found in the EPOS Fimware Specification \n")
                        self.progressbar_1.configure(progress_color="red")
                        self.sidebar_img.configure(image=self.florkimg2)
                else:
                    self.terminal.insert("0.0", f"Error Openening Port: %#5.8x{pErrorCode.value} \n")
                    self.progressbar_1.configure(progress_color="red")
                    self.sidebar_img.configure(image=self.florkimg2)

                self.terminal.configure(state='normal')
                self.terminal.insert("0.0", f"\n")

    # Função para mandar velocidade ao sistema embarcado
    def velocidade(self):
        Velocity = int(self.xtext2.get("0.0", '100.0')[0:-3])
        DeviceName = bytes(self.devicename.get().lstrip(), "utf-8")
        Protocol = bytes(self.protocol.get().lstrip(), "utf-8")
        Interface = bytes(self.interfacename.get().lstrip(), "utf-8")
        Port = bytes(self.portname.get().lstrip(), "utf-8")

        NodeID = 2
        keyhandle = 0
        # return variable from Library Functions
        ret = 0
        pErrorCode = c_uint()
        pDeviceErrorCode = c_uint()

        keyhandle = epos.VCS_OpenDevice(DeviceName, Protocol, Interface, Port, byref(pErrorCode))

        if keyhandle != 0:

            # Device Error Evaluation
            if pDeviceErrorCode.value == 0:

                ret = epos.VCS_ActivateProfileVelocityMode(keyhandle, NodeID, byref(pErrorCode))
                ret = epos.VCS_MoveWithVelocity(keyhandle, NodeID, Velocity, byref(pErrorCode))
                ret = 1

                self.terminal.configure(state='normal')
                self.terminal.insert("0.0", f"Velocity: {Velocity} \n")
                self.progressbar_1.configure(progress_color="green")
                self.sidebar_img.configure(image=self.florkimg1)

            else:
                print(pErrorCode.value)
                self.terminal.insert("0.0", f"{pErrorCode.value} \n")
                self.terminal.insert("0.0",
                                     f"EPOS Error Description can be found in the EPOS Fimware Specification \n")
                self.progressbar_1.configure(progress_color="red")
                self.sidebar_img.configure(image=self.florkimg2)
        else:
            self.terminal.insert("0.0", f"Error Openening Port: %#5.8x{pErrorCode.value} \n")
            self.progressbar_1.configure(progress_color="red")
            self.sidebar_img.configure(image=self.florkimg2)

        self.terminal.configure(state='normal')
        self.terminal.insert("0.0", f"\n")

    # Função para parar o motor do sistema embarcado
    def stop(self):
        Velocity = 0
        DeviceName = bytes(self.devicename.get().lstrip(), "utf-8")
        Protocol = bytes(self.protocol.get().lstrip(), "utf-8")
        Interface = bytes(self.interfacename.get().lstrip(), "utf-8")
        Port = bytes(self.portname.get().lstrip(), "utf-8")

        NodeID = 2
        keyhandle = 0
        # return variable from Library Functions
        ret = 0
        pErrorCode = c_uint()
        pDeviceErrorCode = c_uint()

        keyhandle = epos.VCS_OpenDevice(DeviceName, Protocol, Interface, Port, byref(pErrorCode))

        if keyhandle != 0:

            # Device Error Evaluation
            if pDeviceErrorCode.value == 0:

                ret = epos.VCS_ActivateProfileVelocityMode(keyhandle, NodeID, byref(pErrorCode))
                ret = epos.VCS_MoveWithVelocity(keyhandle, NodeID, Velocity, byref(pErrorCode))
                ret = 1

                self.terminal.configure(state='normal')
                self.terminal.insert("0.0", f"Velocity: {Velocity} \n")
                self.progressbar_1.configure(progress_color="green")
                self.sidebar_img.configure(image=self.florkimg1)

            else:
                print(pErrorCode.value)
                self.terminal.insert("0.0", f"{pErrorCode.value} \n")
                self.terminal.insert("0.0",
                                     f"EPOS Error Description can be found in the EPOS Fimware Specification \n")
                self.progressbar_1.configure(progress_color="red")
                self.sidebar_img.configure(image=self.florkimg2)
        else:
            self.terminal.insert("0.0", f"Error Openening Port: %#5.8x{pErrorCode.value} \n")
            self.progressbar_1.configure(progress_color="red")
            self.sidebar_img.configure(image=self.florkimg2)

        self.terminal.configure(state='normal')
        self.terminal.insert("0.0", f"\n")

    # Seleciona a coordenada X
    def change_x(self, x_value):
        self.xtext.configure(state='normal')
        self.xtext.delete('0.0', '100.0')
        self.xtext.insert('0.0', str(x_value))
        self.xtext.configure(state='disabled')

    def change_x2(self, x_value):
        self.xtext2.configure(state='normal')
        self.xtext2.delete('0.0', '100.0')
        self.xtext2.insert('0.0', str(x_value))
        self.xtext2.configure(state='disabled')

    def change_port_name(self, new: str):
        if self.interfacename.get().lstrip() == "USB":
            self.portname.configure(values=["USB0", "USB1", "USB2", "USB4", "USB5"])
        if self.interfacename.get().lstrip() == "RS232":
            self.portname.configure(values=["COM0", "COM1", "COM2", "COM4", "COM5"])

# Iniciando o Aplicativo
if __name__ == "__main__":

    customtkinter.set_appearance_mode("dark")  # Modes: "System" (standard), "Dark", "Light"
    customtkinter.set_default_color_theme("blue")  # Themes: "blue" (standard), "green", "dark-blue"
    path = r'.\EposCmd64.dll'
    cdll.LoadLibrary(path)
    epos = CDLL(path)
    app = App()
    app.mainloop()
