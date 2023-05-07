import pystray
from tkinter import *
from PIL import Image
import subprocess as s
from pystray import MenuItem as item
from tkinter import filedialog as f

class SERVER():
    def __init__(self, base):
        self.base = base
        self.frame = Frame(base)
        self.frame.pack()
        self.frame2 = Frame(base)
        self.frame2.pack(anchor=CENTER)
        self.frame3 = Frame(base)
        self.frame3.pack()
        self.alerta = Label(self.frame3, text='')
        self.alerta.pack()
    def inicio(self):
        saudacao = Label(self.frame, text="Servidor remoto")
        saudacao.pack(pady=10)
        diretorio = Label(self.frame, text="Diretorio do servidor: ")
        diretorio.pack(pady=10)
        explorar = Button(self.frame, command=lambda: self.procurar_arquivos(diretorio), text="Selecionar diretorio")
        explorar.pack(pady=10)
    def procurar_arquivos(self, diretorio):
        self.pasta = f.askdirectory()
        diretorio['text'] = "Diretorio do servidor: "+self.pasta
        self.frame4 = Frame(self.frame)
        self.frame4.pack()
        port_t = Label(self.frame4, text='Porta: ')
        port_t.grid(column=0, row=0)
        self.port = Spinbox(self.frame4, from_=0, textvariable=8000)
        self.port.grid(column=1,row=0)
        if not hasattr(self,'iniciar_server'):
            self.iniciar_server = Button(self.frame2, command=self.iniciar_servidor, text="Iniciar Servidor")
            self.iniciar_server.pack(side="left",pady=10)
    def iniciar_servidor(self):
        if hasattr(self, 'subprocesso'):
            if self.port.get():
                if self.subprocesso.poll() == 1:
                    try:
                        info = s.STARTUPINFO()
                        info.dwFlags = s.STARTF_USESHOWWINDOW
                        info.wShowWindow = 0 #SW_HIDE para esconder a janela
                        self.subprocesso = s.Popen(f"python -m http.server {self.port.get()} -d {self.pasta}",startupinfo=info)
                        self.alerta["text"] = f'Servidor rodando na porta {self.port.get()}'
                    except:
                        self.alerta["text"] = 'Falha ao iniciar o servidor'
                else:
                    self.subprocesso.terminate()
                    self.iniciar_servidor()
            else:
                self.alerta['text'] = 'escolha uma porta'
        else:
            if self.port.get():
                try:
                    print(self.pasta)
                    info = s.STARTUPINFO()
                    info.dwFlags = s.STARTF_USESHOWWINDOW
                    info.wShowWindow = 0 #SW_HIDE para esconder a janela
                    self.subprocesso = s.Popen(f"python -m http.server {self.port.get()} -d {self.pasta}",startupinfo=info)
                    self.alerta['text'] = f"Servidor rodando na porta {self.port.get()}"
                    self.alerta.pack()
                    self.fechar_server = Button(self.frame2, text="Encerrar servidor", command=self.terminate)
                    self.fechar_server.pack(side="left", pady=10)
                except:
                    self.alerta['text']="Falha ao iniciar o servidor"
            else:
                self.alerta['text']='Escolha uma porta'
    def terminate(self):
        try:
            self.subprocesso.terminate()
            self.alerta['text'] = 'Servidor encerrado'
        except:
            self.alerta['text'] = 'Falha ao encerrar o servidor'

janela = Tk()
janela.title("Servidor python")
janela.geometry("500x300")
img = PhotoImage(file='icon.png')
janela.iconphoto(False, img)
server = SERVER(janela)
server.inicio()
def quit_window(icon, item):
    icon.stop()
    janela.destroy()

def show_window(icon, item):
    icon.stop()
    janela.after(0,janela.deiconify)

def withdraw_window():  
    janela.withdraw()
    image = Image.open("icon.png")
    menu = (item('Quit', quit_window), item('Show', show_window))
    icon = pystray.Icon("name", image, "title", menu)
    icon.run()



janela.protocol("WM_DELETE_WINDOW", withdraw_window)
janela.mainloop()
if hasattr(server, 'subprocesso'):
    server.subprocesso.terminate()