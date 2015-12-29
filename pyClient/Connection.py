﻿import sys
import re
from SocketWrapper import*
from FileWorker import*

class Connection:
    
    def __init__(self,sendBufLen,timeOut):
        self.sendBufLen = sendBufLen
        self.timeOut = timeOut
        self.commands = dict()

    def catchCommand(self,commandMsg):
       commandRegEx = re.compile("[A-Za-z0-9_]+")
       #match() Determine if the RE matches at the beginning of the string.
       matchObj = commandRegEx.match(commandMsg)
       if(matchObj == None):
           #there is no suitable command
           return False
       #group()	Return the string matched by the RE
       command = matchObj.group()
       if command in self.commands:
           #end() Return the ending position of the match
           commandEndPos = matchObj.end()
           #cut finding command from the commandMes
           request = commandMsg[commandEndPos:]
           #cut spaces after command
           request = request.lstrip()
           self.commands[command](request)
           return True
       return False 


    def sendfile(self,sock,commandArgs,recoveryFunc):
        try:
            fileWorker = FileWorker(sock,commandArgs,recoveryFunc,self.sendBufLen,self.timeOut)
            fileWorker.sendFileInfo()
            fileWorker.sendPacketsTCP()
        except FileWorkerError:
            pass 
        

    def receivefile(self,sock,commandArgs,recoveryFunc):
        try:
            fileWorker = FileWorker(sock,commandArgs,recoveryFunc,self.sendBufLen,self.timeOut)
            fileWorker.recvFileInfo()
            fileWorker.recvPacketsTCP()
        except FileWorkerError:
            pass
                
