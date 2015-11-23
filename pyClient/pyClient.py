import sys  #for IP and port passing
import socket
import re   #regular expressions
from Connection import Connection
from SocketWrapper import*
from FileWorker import FileWorkerError
from random import randint
import time

class Client(Connection):

    def __init__(self,IP,port, sendBufLen=2048, timeOut=15):
        super().__init__(sendBufLen, timeOut)
        self.sock = TCP_ClientSockWrapper(IP,port)
        #send client id to the server
        self.id = randint(0,sys.maxsize - 1) 
        self.sock.sendInt(self.id)
        #fill dictionary with all available commands
        self.__fillCommandDict()

 
    def __fillCommandDict(self):
        self.commands.update({'download':self.recvFileTCP,
                              'upload':self.sendFileTCP})


    def sendFileTCP(self,commandArgs):
        self.sendfile(self.sock,commandArgs,self.recoverTCP)


    def recvFileTCP(self,commandArgs):
        self.receivefile(self.sock,commandArgs,self.recoverTCP)


    def recoverTCP(self,timeOut):
        start = time.time()
        timediff = 0
        while(timediff < timeOut):
            timediff = time.time() - start
            if self.sock.reattachClientSock():
                #send client id to server
                self.sock.sendInt(self.id)
                return self.sock
        raise FileWorkerError("fail to reconnect")


    def recoverUDP(self,timeOut):
        strobe = timeOut // 6
        start = time.time()
        timediff = 0
        self.sock.raw_sock.settimeout(strobe)
        while (timediff < timeOut):
            timediff = time.time() - start
           
            


    def workingWithServer(self):
        try:
            while True:
                try:
                    commandMsg = input('->')
                    self.sock.sendMsg(commandMsg)
                    self.catchCommand(commandMsg)
                    print(self.sock.recvMsg())

                except FileWorkerError as e:
                    print(e.args[0])
        #raise when server broke connection due to the "quit" command
        except OSError:
            sys.exit(1)
       




if __name__ == "__main__":
    

    client = Client(sys.argv[1],sys.argv[2])
    client.workingWithServer()