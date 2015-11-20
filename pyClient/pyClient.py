import sys  #for IP and port passing
import socket
import re   #regular expressions
from Connection import*


class Client(Connection):

    def __init__(self,IP,port, sendBufLen, timeOut):
        return super().__init__(sendBufLen, timeOut)
        self.IP = IP
        self.port = port
        self.sock = None
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


















if __name__ == "__main__":
    

    server = TCPServer(sys.argv[1],sys.argv[2])