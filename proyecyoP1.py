from datetime import date, datetime
from Crypto.PublicKey import RSA
from Crypto.Cipher import AES, PKCS1_OAEP
import binascii
import json
import base64

class ObjetoSeguro:

    # Atributos
    def __init__(self, nombre):
        self.nombre = nombre # Este parametro se recibe
        self.llavePublica, self.llavePrivada = self.gen_llaves() # Esto se crea de manera interna

        diccionarioVacio = {}
        tf = open("registro.json", "w")
        json.dump(diccionarioVacio,tf)
        tf.close()

    def gen_llaves(self):
        keyPair = RSA.generate(2048) # Esta es la PRIVADA que se retorna
        pubKey = keyPair.publickey() # Esta es la PUBLICA que se retorna
        pubKeyHEX = f"Public key: (n={hex(pubKey.n)}, e={hex(pubKey.e)})"
        pubKeyPEM = pubKey.exportKey().decode('ascii')
        privKeyHEX = f"Private key: (n={hex(pubKey.n)}, d={hex(keyPair.d)})"
        privKeyPEM = keyPair.exportKey().decode('ascii')
        
        with open("llaves.txt","w") as pk:
            pk.write(">>> La llave publica en formato hexadecimal es:\n")
            pk.write(pubKeyHEX)
            pk.write("\n\n>>>La llave publica en formato PEM es:\n")
            pk.write(pubKeyPEM)
            pk.write("\n\n>>> La llave privada en formato hexadecimal es:\n")
            pk.write(privKeyHEX)
            pk.write("\n\n>>> La llave privada en formato PEM es:\n")
            pk.write(privKeyPEM)
        return pubKey,keyPair

    def saludar(self,emisorName, mensajeCifrado):
        if emisorName == "Alice": llaveDestinatario = Bob.llave_publica()
        else: llaveDestinatario = Alice.llave_publica()

        print(f"Este es el mensaje de {emisorName}: {mensajeCifrado}")
        textoRecibidoEnClaro = mensajeCifrado
        # llaveDestinatario = Bob.llave_publica()
        print(">> Llave Destinatario: ",llaveDestinatario)
        textoCodificado = self.codificar64(textoRecibidoEnClaro)
        print(">> Mensaje codificado: ",textoCodificado)
        textoEncriptado = self.cifrar_msj(llaveDestinatario,textoCodificado)
        print(">> Mensaje Encriptado: ",textoEncriptado)
        self.esperar_respuesta(textoEncriptado)

        

    def responder(self, textoEnClaro):
        respuesta = textoEnClaro + "MensajeRespuesta"
        return respuesta
    
    def llave_publica(self):
        return self.llavePublica
    
    def cifrar_msj(self,llavePublicaDesinatario, mensaje):
        pubKey = llavePublicaDesinatario
        textoPlano = mensaje.encode("utf-8")

        encryptor = PKCS1_OAEP.new(pubKey)
        encrypted = encryptor.encrypt(textoPlano)
        # print("Mensaje encriptado: ", binascii.hexlify(encrypted))
        return encrypted

    def descifrar_msj(self,mensajeCifrado):
        privKey = self.llavePrivada
        textoCifrado = mensajeCifrado
        print(type(textoCifrado))

        decryptor = PKCS1_OAEP.new(privKey)
        decrypted = decryptor.decrypt(textoCifrado)
        # print("Mensaje desencriptado: ", decrypted.decode())
        return decrypted

    def codificar64(self,mensajeSinCodificar):
        message_bytes = mensajeSinCodificar.encode("ascii")
        base64_bytes = base64.b64encode(message_bytes)
        base64_message = base64_bytes.decode("ascii")
        return(base64_message)

    def decodificar64(sefl,mensajeCodificado):
        base64_message = mensajeCodificado.decode("utf-8")
        base64_bytes = base64_message.encode('ascii')
        message_bytes = base64.b64decode(base64_bytes)
        message = message_bytes.decode('ascii')
        return message

    def almacenar_msj(self, textoPlano):
        # Contar el numero de registros en el .json para asignar el ID
        tf = open("registro.json","r")
        paraContarRegistros = json.load(tf)
        numeroRegistros = len(paraContarRegistros.keys())

        # Campos que lleva el diccionario
        ID = numeroRegistros+1
        text = textoPlano
        fecha = date.today()
        hora = datetime.now().time()
        listaRegistro = [text,format(fecha),format(hora)] # Campos adicionales

        # Leer el diccionario anterior y actualizar
        tf = open("registro.json","r")
        previous_dict = json.load(tf)
        previous_dict[ID] = listaRegistro

        # Escribir el diccionario actualizado
        tf = open("registro.json", "w")
        json.dump(previous_dict,tf)
        tf.close()

        return ID

    def consultar_msj(self,ID):
        file = open("registro.json","r")
        diccionario = json.load(file)

        # Construimos la estructura de diccionario que debemos retornar
        dictReturn = {"ID":ID,"MSJ":diccionario[f"{ID}"][0],"FECHA":diccionario[f"{ID}"][1],"HORA":diccionario[f"{ID}"][2]}
        
        return dictReturn

    def esperar_respuesta(self,mensajeCifrado):
        textoRecibidoCifrado = mensajeCifrado
        if (self.nombre == "Alice"):
            textoRecibidoDescifrado = Bob.descifrar_msj(textoRecibidoCifrado)
            print(">> Mensaje Descifrado: ",textoRecibidoDescifrado)
            mensajeDecodificado = Bob.decodificar64(textoRecibidoDescifrado)
            print(">> Mensaje Decodificado: ",mensajeDecodificado)
            #Guardamos el mensaje que le llego a Bob
            self.almacenar_msj(mensajeDecodificado)
            respuestaBob = Bob.responder("Respuesta a Objeto de Alice")
            print(">> Respuesta de Bob: ",respuestaBob)
            Bob.saludar("Bob",respuestaBob)
        else: 
            textoRecibidoDescifrado = Alice.descifrar_msj(textoRecibidoCifrado)
            print(">> Mensaje Descifrado: ",textoRecibidoDescifrado)
            mensajeDecodificado = Bob.decodificar64(textoRecibidoDescifrado)
            print(">> Mensaje Decodificado: ",mensajeDecodificado)
            #Guardamos el mensaje que le llego a Alice
            self.almacenar_msj(mensajeDecodificado)


Alice = ObjetoSeguro("Alice") 
Bob = ObjetoSeguro("Bob")  

Alice.saludar("Alice","Este es el primer mensaje a enviar")




#----------------------------------------------------------------
# cipherText = Alice.cifrar_msj(Bob.llave_publica(),"MEnsaje  de Prueba")
# print(cipherText)
# Bob.descifrar_msj(cipherText)


# Alice.almacenar_msj("Primer mensaje a almacenar")
# Alice.almacenar_msj("Segundo mensaje a almacenar")
# Alice.consultar_msj(1)
# Alice.consultar_msj(2)
# Alice.codificar64("hola")
# Alice.decodificar64("aG9sYQ==")


# Bob.gen_llaves()

# Alice.saludar(Alice,"hola bob")

# Alice.cifrar()
# Bob.descifrar()