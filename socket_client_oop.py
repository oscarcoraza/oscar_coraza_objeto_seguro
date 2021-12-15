from proyectoP2 import ObjetoSeguro
from socket_server_oop import SocketServer
import socket


class SocketClient:
    def __init__(self):
        self.socketCliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.IPServidor = "localhost" # Direccion del puerto al que nos vamos a conectar
        self.puertoServidor = 12345 # Puerto
        self.socketCliente.connect((self.IPServidor,self.puertoServidor))
        self.Alice = ObjetoSeguro("Alice")
        self.llaveAlice = self.Alice.llave_publica()

        # Alice manda su llave publica
        self.socketCliente.send(self.llaveAlice.encode())

        # Recibimos la llave pública de Bob
        self.BobPK = self.socketCliente.recv(1024).decode()
        print("La llave publica recibida de Bob es: ",self.BobPK)

    def send_sms(self, SMS):
        tex_cod = self.Alice.codificar64(SMS)
        tex_cif = self.Alice.cifrar_msj(self.BobPK,tex_cod)
        self.socketCliente.send(tex_cif) # .encode()

    def sender(self):
        message = ""
        while message != "exit":
            # Comenzamos la comunicacion
            message = input(">>> ")
            # Enviamos mensaje
            self.send_sms(message)
            respuesta = self.socketCliente.recv(4096).decode()
            print(" Servidor >> ",respuesta)


if __name__ == '__main__':
    
    client = SocketClient()
    client.sender()
