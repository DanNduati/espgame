import socket
import time
import ujson

bufferSize = 1024
UDP_IP_ADDRESS = "192.168.0.182"
UDP_PORT = 6969
serverSock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)

def createSocket():
    #create our datagram serversocket
    serverSock.bind((UDP_IP_ADDRESS,UDP_PORT))
    print('Udp server up and listening')

def receiveData():
    data,addr = serverSock.recvfrom(bufferSize)
    #ack response
    serverSock.sendto(data.upper(),addr)
    #decode the data
    packet = data.decode("utf-8")
    packet = ujson.loads(packet)
    #print('Server Received: ',data,' from: ',addr)
    xval = packet['x']
    yval = packet['y']
    startBtn = packet['s']
    return [xval,yval,startBtn]
def getData():
    states = receiveData()
    return states
