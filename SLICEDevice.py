# -*- coding: utf-8 -*-
"""
Created on Mon Aug 24 15:18:11 2020

@author: ryan.robinson
"""



from serial_mod import serialwin32


class SLICE:
    def __init__(self,comNum):
        '''Open the serial port
        Input: comNum'''
        comNum = comNum
        # OPEN SERIAL
        self.SliceSer = serialwin32.Serial(port='COM'+str(comNum),parity='N', baudrate=9600, timeout=1, bytesize=8)
        return None
        
    def SliceSend(self,CommandInput):
        '''Function that sends a serial string command to SLICE Box 
        Input: CommandInput[str]
        Output: SliceOutputReturn'''
        SliceByteRead = 256  # Number of bytes to read on ser.read()
        
        # WRITE COMMAND
        command = str(str(CommandInput) + '\r\n' )     
        
        # SEND COMMAND AND RECIEVE RESULT
        self.SliceSer.write(command.encode())
        SliceOutput = self.SliceSer.read(SliceByteRead).decode() #Read Buffer
        SliceOutputReturn=SliceOutput.strip('\r\n')
        
        # RETURN RESULT
        return SliceOutputReturn
    
    def close(self):
        '''Close the serial port'''
        # CLOSE SERIAL
        self.SliceSer.close() #Close COM Port
        return None

# FOR TESTING PURPOSES    
if __name__=="__main__":
    try:
        A = SLICE(5)
        print(A.SliceSend('CAVTEMP?'))
        # print("ModeLockRMSThreshold = +"+A.SliceSend('MLRMTHR?'))
    finally:
        A.close()