import sys  #for IP and port passing
import socket
import re   #regular expressions
from SocketWrapper import*
from FileWorker import*

class QueryError(Exception):
    pass

class Client:

    def __init__(self,IP,ports):
        self.IP = IP
        self.ports = ports
        self.sock = None 
        #fill dictionary with all available commands
        self.__fillCommandDict()

 
    def __fillCommandDict(self):
        self.commands = ({'time':(self.ports[0],None),
                       'echo':(self.ports[1],None), 
                       'download':(self.ports[2],self.recvFileTCP)})

    def sendfile(self,sock,commandArgs,recoveryFunc):
        try:
            fileWorker = FileWorker(sock,commandArgs,recoveryFunc)
            fileWorker.sendFileInfo()
            fileWorker.sendPacketsTCP()
        except FileWorkerError:
            pass 
       
    def receivefile(self,sock,commandArgs,recoveryFunc):
        try:
            fileWorker = FileWorker(sock,commandArgs,recoveryFunc)
            fileWorker.recvFileInfo()
            fileWorker.recvPacketsTCP()
        except FileWorkerError:
            pass

    def sendFileTCP(self,commandArgs):
        self.sendfile(self.sock,commandArgs,None)

    def recvFileTCP(self,commandArgs):
        self.receivefile(self.sock,commandArgs,None)

    def parseCommand(self,cmd_msg):
        commandRegEx = re.compile("[A-Za-z0-9_]+")
        #match() Determine if the RE matches at the beginning of the string.
        matchObj = commandRegEx.match(cmd_msg)
        if(matchObj == None):
            #there is no suitable command
            return False
        #group()	Return the string matched by the RE
        str_cmd = matchObj.group()
        if not str_cmd in self.commands:
            raise QueryError('command is not implemented')
        #end() Return the ending position of the match
        commandEndPos = matchObj.end()
        #cut finding command from the commandMes
        args = cmd_msg[commandEndPos:]
        #cut spaces after command
        args = args.lstrip()
        return (str_cmd,args)
      

    def workingWithServer(self):
        while True:
            try:
                cmd_msg = input('->')
                str_cmd,args = self.parseCommand(cmd_msg)
                #create socket
                port,routine = self.commands[str_cmd]
                self.sock = TCP_ClientSockWrapper(self.IP,port)
                self.sock.sendMsg(cmd_msg)
                if routine:
                    routine(args)
                print(self.sock.recvMsg())

            except (QueryError) as e:
                print(e)
                continue
            except (OSError,FileWorkerError):
                return
       

if __name__ == "__main__":
    client = Client(sys.argv[1],sys.argv[2:])
    client.workingWithServer()