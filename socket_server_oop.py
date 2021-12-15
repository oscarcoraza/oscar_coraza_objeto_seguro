import socket
from proyectoP2 import ObjetoSeguro


class SocketServer:
    def __init__(self):
        self.socketServidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # Generamos el socket
        self.direccionServidor = "localhost"
        self.puertoServidor = 12345 # Puerto donde escucha
        self.socketServidor.bind((self.direccionServidor,self.puertoServidor)) # Enlace
        self.socketServidor.listen(5) # Ponemos a escuchar al sevidor
        self.socketConexion, addr = self.socketServidor.accept() # Establecemos la conexion
        self.Bob = ObjetoSeguro("Bob")
        self.BobPK = self.Bob.llave_publica()

        # Espera la llave de Alice
        self.AlicePK = self.socketConexion.recv(1024).decode()
        print("La llave publica recibida de Alice es: ",self.AlicePK)
       
        # Bob manda su llave
        self.socketConexion.send(self.BobPK.encode())

    def miLlave(self):
        return self.llaveBob

    def receiver(self):
        msg = ""
        while msg != "exit":
            # Recibimos el mensaje del cliente
            msg = self.socketConexion.recv(1024)#.decode()
            tex_desci = self.Bob.descifrar_msj(msg)
            tex_decod = self.Bob.decodificar64(tex_desci)
            print(f"<<< {tex_decod}")
            

            # Mandamos mensaje al cliente
            self.socketConexion.send(input().encode())

if __name__ == '__main__':

    Bob = ObjetoSeguro("Bob")  
    
    server = SocketServer()
    server.receiver()
