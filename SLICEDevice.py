# -*- coding: utf-8 -*-
"""
Created on Mon Aug 24 15:18:11 2020

@author: ryan.robinson
"""



from serial_mod import serialwin32


class SLICE:
    def __init__(self,comNum):
        self.comNum = comNum
        return None
        
    def SliceSend(self,CommandInput):
        '''Function that sends a serial string command to SLICE Box 
        Input: CommandInput[str]
        Output: None (unless print line uncommented)/Read buffer always emptied!
        Note 1: COM Port is opened/closed each time function is run. 
        This is so if the program fails midway through the com devices won't need to be powercycled'''
        #Open Port w/ SLICE COM Default Settings
        SliceTimeout = .1  # Communication Timeout (seconds)
        SliceByteRead = 256  # Number of bytes to read on ser.read()
        SliceDelay = .01  # Delay in seconds after sending Slice Command to ensure execution        
        
        # OPEN SERIAL
        self.SliceSer = serialwin32.Serial(port='COM'+str(self.comNum),parity='N', baudrate=9600, timeout=1, bytesize=8)
        #self.SliceSer = serial.Serial(port='COM'+str(int(self.comNum,)),baudrate=9600,timeout=SliceTimeout,parity='N',stopbits=1,bytesize=8)

        # WRITE COMMAND
        command = str(str(CommandInput) + '\r\n' )     
        #Send Commands/Close Port
        self.SliceSer.write(command.encode())
        #time.sleep(SliceDelay)
        SliceOutput = self.SliceSer.read(SliceByteRead).decode() #Read Buffer
        #time.sleep(SliceDelay)
        self.SliceSer.close() #Close COM Port
        SliceOutputReturn=SliceOutput.strip('\r\n')
        return SliceOutputReturn
    
    def close(self):
        self.SliceSer.close() #Close COM Port
        return None

# FOR TESTING PURPOSES    
if __name__=="__main__":
    A = SLICE(3)
    print(A.SliceSend('MODELOK?'))