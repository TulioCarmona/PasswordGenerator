"""
Author: Marco Tulio Carmona Bellido
This programs simulates a server with the capability of generate pseudorandom passwords using predefined characters
17-06-2023
"""
import socket
import random
import threading

def pass_generate(n1, n2, n3, n4):
    minus = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'v',
             'w', 'x', 'y', 'z']  # 25 char
    mayus = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'V',
             'W', 'X', 'Y', 'Z'] # 25 char
    num = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']  # 10 char
    sChar = ['#', '$', '%', '!', '^', '&', '*', '<', '>', '?', '¿', '+', '-','@']  # 13 char
    n5 = n1 - n2 - n3 - n4
    c1 = random.choices(minus, k=n5) #choose k random elements from a given list
    c2 = random.choices(mayus, k=n2)
    c3 = random.choices(sChar, k=n3)
    c4 = random.choices(num, k=n4)
    #concatenates all random elements into one list
    primitivePass = c1
    for i in c2:
        primitivePass.append(i)
    for i in c3:
        primitivePass.append(i)
    for i in c4:
        primitivePass.append(i)
    # creates the final password from the selected elements
    p = ''
    while len(primitivePass) > 0:
        x = len(primitivePass)
        if x == 1:
            p+= primitivePass.pop(0)
        else:
            p+=primitivePass.pop(random.randint(0, x-1))
    return p #returns the generated password

pswd = 'Batman |m|.' #default password if you get it as a result of a request something went wrong
#server configuration
host = 'localhost' #server IP
port = 12345

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #socket config

sock.bind((host, port))

sock.listen(5)
print('Servidor escuchando en {}:{}'.format(host, port))

#client handler
def NweClientSocketHandler(client, addr):
    global pswd
    print('Socket Id del cliente:',client)
    while True:
        try:
            data = client.recv(1024).decode()
            try:
                lon, mayus, sc, num = data[:].split(sep=',')
                pswd = pass_generate(int(lon), int(mayus), int(sc), int(num))
                client.send(pswd.encode())
                print(pswd)
            except:
                if data:
                    if data == 'pp':
                        client.send(pswd.encode())
                    else:
                        pswd = data
                        #print(pswd)
        except:
            print('Conexxion perdida con', addr)
            break

#Wait for multiple conecctions
print('Esperando por conexiones')
while True:
    client, addr = sock.accept()
    msg = 'Conexion aceptada'
    client.send(msg.encode())

    threading._start_new_thread(NweClientSocketHandler , (client, addr))
