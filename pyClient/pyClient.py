import sys  #for IP and port passing
import socket
import re   #regular expressions
from Connection import Connection
from SocketWrapper import*
from FileWorker import*
from random import randint
import time

class Client(Connection):

    def __init__(self,IP,port, sendBufLen=1024, timeOut=15):
        super().__init__(sendBufLen, timeOut)
        self.sock = TCP_ClientSockWrapper(IP,port,createId=True)
        #send socket id
        self.sock.sendInt(self.sock.id)
        self.udpSock = UDP_ClientSockWrapper(IP,port)
        #fill dictionary with all available commands
        self.__fillCommandDict()

 
    def __fillCommandDict(self):
        self.commands.update({'download':self.recvFileTCP,
                              'upload':self.sendFileTCP,
                              'download_udp':self.recvFileUDP,
                              'upload_udp':self.sendFileUDP})


    def sendFileTCP(self,commandArgs):
        self.sendfile(self.sock,commandArgs,self.recoverTCP)

    def recvFileTCP(self,commandArgs):
        self.receivefile(self.sock,commandArgs,self.recoverTCP)

    def recoverTCP(self,timeOut):
        start = time.time()
        timediff = 0
        while(True):
            timediff = time.time() - start
            if timediff > timeOut:
                raise OSError("reconnection timeout")
            if self.sock.reattachClientSock():
                #send client id to server
                self.sock.sendInt(self.sock.id)
                return self.sock
  

    def sendFileUDP(self,commandArgs):
        self.udpSock.sendInt(1)
        self.sendfile(self.udpSock,commandArgs,self.recoverTCP)

    def recvFileUDP(self,commandArgs):
        self.udpSock.sendInt(1)
        self.receivefile(self.udpSock,commandArgs,self.recoverTCP)

    def workingWithServer(self):
        while True:
            try:
                commandMsg = input('->')
                self.sock.sendMsg(commandMsg)
                self.catchCommand(commandMsg)
                print(self.sock.recvMsg())

            except FileWorkerError as e:
                print(e)
                continue
            except (OSError,FileWorkerError):
                return
       

if __name__ == "__main__":
    client = Client(sys.argv[1],sys.argv[2])
    client.workingWithServer()