import socket
import time
import sys
import select
from urllib.request import parse_keqv_list

from zfec.easyfec import Encoder, Decoder
import random
import zfec

print("MODE:")
x = input()
if(x == "1"):
    print("Message:")
    msgFromClient = input()
    bytesToSend = str.encode(msgFromClient)
    serverAddressPort = ("127.0.0.1", 20001)
    bufferSize = 1024

    # Create a UDP socket at client side

    UDPClientSocket = socket.socket(
        family=socket.AF_INET, type=socket.SOCK_DGRAM)

    # Send to server using created UDP socket

    UDPClientSocket.sendto(bytesToSend, serverAddressPort)

    msgFromServer = UDPClientSocket.recvfrom(bufferSize)

    msg = "Message from Server {}".format(msgFromServer[0].decode())

    print(msg)

elif (x == "2"):
    #收檔案
    UDP_IP = "127.0.0.1"
    IN_PORT = 5005
    timeout = 3

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind((UDP_IP, IN_PORT))
    print("Loading...")

    while True:
        data, addr = sock.recvfrom(1024)
        if data:
            print("File name:", data)
            file_name = data.strip()

        f = open(file_name, 'wb')

        while True:
            ready = select.select([sock], [], [], timeout)
            if ready[0]:
                data, addr = sock.recvfrom(1024)
                f.write(data)
            else:
                print("%s Finish!" % file_name)
                f.close()
                break
elif (x == "3"):
    #zfec收檔案
    UDP_IP = "127.0.0.1"
    IN_PORT = 5005
    timeout = 3

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind((UDP_IP, IN_PORT))
    print("Loading...")

    while True:
        data, addr = sock.recvfrom(1024)
        if data:
            print("File name:", data)
            file_name = data.strip()

        f = open(file_name, 'wb')
        data, addr = sock.recvfrom(1024)
        k= data.strip().decode()

        data, addr = sock.recvfrom(1024)
        m= data.strip().decode()

        while True:
            ready = select.select([sock], [], [], timeout)
            if ready[0]:
                packets=[]
                for g in range (int(k)):
                    data, addr = sock.recvfrom(1024)
                    i=data.decode()
                    data, addr = sock.recvfrom(1024)
                    d=data.strip()

                    tmp=(int(i),bytearray(d))
                    packets.append(tmp)
                print(packets)
                blocks = list(x[1] for x in packets)
                blocknums = list(x[0] for x in packets)
                decK = Decoder(int(k),int(m))
                decoded = decK.decode(blocks, sharenums=blocknums, padlen=0)
                data_dec = decoded.decode()
                print(decoded)
                f.write(decoded)
                #f.write(data)
            else:
                print("%s Finish!" % file_name)
                f.close()
                break
elif (x == "4"):
    #平行zfec收檔案
    UDP_IP = "127.0.0.1"
    IN_PORT = 5005
    timeout = 3

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind((UDP_IP, IN_PORT))
    print("Loading...")

    while True:
        data, addr = sock.recvfrom(1024)
        if data:
            print("File name:", data)
            file_name = data.strip()

        f = open(file_name, 'wb')
        data, addr = sock.recvfrom(1024)
        k= data.strip().decode()

        data, addr = sock.recvfrom(1024)
        m= data.strip().decode()

        while True:
            ready = select.select([sock], [], [], timeout)
            if ready[0]:
                packets=[]
                int_tmp=[]
                byte_tmp=[]
                for g in range (int(k)):
                    data, addr = sock.recvfrom(1024)
                    i=data.decode()
                    int_tmp.append(i)
                for h in range (int(k)):
                    data, addr = sock.recvfrom(1024)
                    d=data.strip()
                    byte_tmp.append(d)
                for j in range (int(k)):
                    tmp=(int(int_tmp[j]),bytearray(byte_tmp[j]))
                    packets.append(tmp)
                print(packets)
                blocks = list(x[1] for x in packets)
                blocknums = list(x[0] for x in packets)
                decK = Decoder(int(k),int(m))
                decoded = decK.decode(blocks, sharenums=blocknums, padlen=0)
                data_dec = decoded.decode()
                print(decoded)
                f.write(decoded)
                #f.write(data)
            else:
                print("%s Finish!" % file_name)
                f.close()
                break