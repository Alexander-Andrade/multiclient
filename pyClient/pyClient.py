import sys  #for IP and port passing
import socket
import re   #regular expressions
from Connection import Connection
from SocketWrapper import SocketWrapper
from FileWorker import FileWorkerError
from random import randint

class Client(Connection):

    def __init__(self,IP,port, sendBufLen=2048, timeOut=30):
        super().__init__(sendBufLen, timeOut)
        self.IP = IP
        self.port = port
        self.sock = None
        self.addrInfo = None
        self.__createClient(IP,port)
        #send client id to the server
        self.id = randint(0,sys.maxsize - 1) 
        self.sock.sendNum(self.id)
        #fill dictionary with all available commands
        self.__fillCommandDict()

    def __createClient(self,IP,port):
        for self.addrInfo in socket.getaddrinfo(IP,port,socket.AF_UNSPEC,socket.SOCK_STREAM):
            af_family,socktype,proto,canonname,sockaddr = self.addrInfo
            try:
                sock = socket.socket(af_family,socktype,proto)
            except OSError as msg:
                sock = None
                continue
            try:
                sock.connect(sockaddr)
            except OSError as msg:
                sock.close()
                sock = None
                continue
            break
        if sock is None:
            print("fail to onnect to the socket")
            sys.exit(1)            
        #put socket to the SocketWrapper
        self.sock = SocketWrapper(sock)

    def __fillCommandDict(self):
        self.commands.update({'download':self.recvFile,
                              'upload':self.sendFile})


    def sendFile(self):
        pass


    def recvFile(self):
        pass


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