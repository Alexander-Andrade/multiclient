import sys  #for IP and port passing
import socket
import re   #regular expressions
from Connection import*


class Client(Connection):

    def __init__(self,IP,port, sendBufLen=2048, timeOut=30):
        super().__init__(sendBufLen, timeOut)
        self.IP = IP
        self.port = port
        self.sock = None
        self.__createClient(IP,port)
        #send client id to the server
        self.id = randint(0,sys.maxsize - 1) 
        self.sendNum(self.sock,self.id)
        #fill dictionary with all available commands
        self.__fillCommandDict()

    def __createClient(self,IP,port):
        for addrInfo in socket.getaddrinfo(IP,port,socket.AF_UNSPEC,socket.SOCK_STREAM):
            af_family,socktype,proto,canonname,sockaddr = addrInfo
            try:
                self.sock = socket.socket(af_family,socktype,proto)
            except OSError as msg:
                self.sock = None
                continue
            try:
                self.sock.connect(sockaddr)
            except OSError as msg:
                self.sock.close()
                self.sock = None
                continue
            break
        if self.sock is None:
            print("fail to onnect to the socket")
            sys.exit(1)            


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
                commandMsg = input('->')
                self.sendMsg(self.sock,commandMsg)
                self.catchCommand(commandMsg)
                print(self.recvMsg(self.sock))
        #raise when server broke connection due to the "quit" command
        except OSError as msg:
            return




if __name__ == "__main__":
    

    client = Client(sys.argv[1],sys.argv[2])
    client.workingWithServer()