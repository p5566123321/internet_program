
import socket
import time
import sys
import select
import os

from zfec.easyfec import Encoder, Decoder
import random
import zfec

import threading
import queue


def test_enc(k,m,orig_str):
  encK = Encoder(k,m)
  decK = Decoder(k,m)
  
  #data   = ' '.join(orig_str)
  data   = orig_str
  b_data = bytearray(data.encode())
  stream = encK.encode(b_data)

  # 由傳送的資料流中隨機取出 k 個封包
  packets = random.sample(list(enumerate(stream)), k)
  for i, d in packets:
    print(i, "Payload:  ", d)
    

  return packets

class Worker(threading.Thread):
  def __init__(self, queue, num):
    threading.Thread.__init__(self)
    self.queue = queue
    self.num = num

  def run(self):
    while self.queue.qsize() > 0:
        # 取得新的資料
        msg = self.queue.get()

        # 處理資料
        if (type(msg) is int):
            if(sock.sendto(str.encode(str(msg)), (UDP_IP, UDP_PORT))):
                data = f.read(buf)
                time.sleep(0.02)  # Give receiver a bit time to save
        else:
            if(sock.sendto(bytes(msg), (UDP_IP, UDP_PORT))):
                data = f.read(buf)
                time.sleep(0.02)  # Give receiver a bit time to save
        print("Worker %d: %s" % (self.num, msg))
        


print("MODE:")
x = input()

if(x == "1"):
    #傳訊息
    localIP = "127.0.0.1"

    localPort = 20001

    bufferSize = 1024

    msgFromServer = "Hello UDP Client"

    bytesToSend = str.encode(msgFromServer)

    # Create a datagram socket

    UDPServerSocket = socket.socket(
        family=socket.AF_INET, type=socket.SOCK_DGRAM)

    # Bind to address and ip

    UDPServerSocket.bind((localIP, localPort))

    print("UDP server up and listening")

    # Listen for incoming datagrams

    while(True):

        bytesAddressPair = UDPServerSocket.recvfrom(bufferSize)

        message = bytesAddressPair[0]

        address = bytesAddressPair[1]
        
        clientMsg = "Message from Client:{}".format(message.decode())
        clientIP = "Client IP Address:{}".format(address)

        print(clientMsg)
        print(clientIP)

        # Sending a reply to client

        UDPServerSocket.sendto(bytesToSend, address)
elif(x == "2"):
    #傳檔案
    UDP_IP = "127.0.0.1"
    UDP_PORT = 5005
    buf = 1024
    print("File name:")
    file_name = input()

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.sendto(str.encode(file_name), (UDP_IP, UDP_PORT))
    print("Sending %s ..." % file_name)

    f = open(file_name, "r")
    data = f.read(buf)

    while(data):
        if(sock.sendto(str.encode(data), (UDP_IP, UDP_PORT))):
            data = f.read(buf)
            time.sleep(0.02)  # Give receiver a bit time to save

    sock.close()
    f.close()

elif(x == "3"):
    #收指令
    localIP = "127.0.0.1"

    localPort = 20001

    bufferSize = 1024


    # Create a datagram socket

    UDPServerSocket = socket.socket(
        family=socket.AF_INET, type=socket.SOCK_DGRAM)

    # Bind to address and ip

    UDPServerSocket.bind((localIP, localPort))

    print("UDP server up and listening")

    # Listen for incoming datagrams

    while(True):

        bytesAddressPair = UDPServerSocket.recvfrom(bufferSize)

        message = bytesAddressPair[0]

        address = bytesAddressPair[1]
        
        clientMsg = "Message from Client:{}".format(message.decode())
        clientIP = "Client IP Address:{}".format(address)

        print(clientMsg)
        print(clientIP)


        
        # Sending a reply to client
        msgFromServer =  os.popen(message.decode()).readlines() 
        t=""
        for x in msgFromServer:
            t=t+x+"\n"
        
        bytesToSend = str.encode(t)
        UDPServerSocket.sendto(bytesToSend, address)
elif(x == "4"):
    #傳檔案zfec
    UDP_IP = "127.0.0.1"
    UDP_PORT = 5005
    buf = 1024
    print("File name:")
    file_name = input()

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.sendto(str.encode(file_name), (UDP_IP, UDP_PORT))
    print("Sending %s ..." % file_name)

    f = open(file_name, "r")
    data = f.read(buf)

    #!!!!!
    k=20
    m=25
    sock.sendto(str.encode(str(k)), (UDP_IP, UDP_PORT))
    sock.sendto(str.encode(str(m)), (UDP_IP, UDP_PORT))
    packets=test_enc(k,m,data)
    print(packets)
    #!!!!!
    while(data):
        for i, d in packets:
            if(sock.sendto(str.encode(str(i)), (UDP_IP, UDP_PORT))):
                data = f.read(buf)
                time.sleep(0.02)  # Give receiver a bit time to save
            if(sock.sendto(bytes(d), (UDP_IP, UDP_PORT))):
                data = f.read(buf)
                time.sleep(0.02)  # Give receiver a bit time to save

    sock.close()
    f.close() 

elif(x == "5"):
    #傳檔案zfec
    UDP_IP = "127.0.0.1"
    UDP_PORT = 5005
    buf = 1024
    print("File name:")
    file_name = input()

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.sendto(str.encode(file_name), (UDP_IP, UDP_PORT))
    print("Sending %s ..." % file_name)

    f = open(file_name, "r")
    data = f.read(buf)

    #!!!!!
    k=20
    m=25
    sock.sendto(str.encode(str(k)), (UDP_IP, UDP_PORT))
    sock.sendto(str.encode(str(m)), (UDP_IP, UDP_PORT))
    packets=test_enc(k,m,data)
    print(packets)
    #!!!!!
    
    my_queue1 = queue.Queue()
    my_queue2 = queue.Queue()
    for i, d in packets:
        my_queue1.put(i)
        my_queue2.put(d)

    my_worker1 = Worker(my_queue1, 1)
    my_worker2 = Worker(my_queue1, 2)


    my_worker1.start()
    my_worker2.start()
    

    my_worker1.join()
    my_worker2.join()
    

    my_worker3 = Worker(my_queue2, 3)
    my_worker4 = Worker(my_queue2, 4)

    my_worker3.start()
    my_worker4.start()

    my_worker3.join()
    my_worker4.join()

    sock.close()
    f.close() 

