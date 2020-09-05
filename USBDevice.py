# -*- coding: utf-8 -*-
"""
Created on Tue Aug 25 14:50:02 2020

@author: ryan.robinson
"""

import pyvisa



class USBDevice:
    def __init__(self,rname):
        self.inst = pyvisa.ResourceManager().open_resource(rname)
        return None
    
    def settimeout(self,timeout):
        self.inst.timeout = timeout+1000
    
    def send(self,command):
        return self.inst.query(command).strip('\r\n')
    
    def close(self):
        self.inst.close()
        return None



# CODE FOR TESTING
if __name__=="__main__":
    try:
        counter = USBDevice('USB0::0x0957::0x1707::MY50002091::0::INSTR')
        print(counter.send("*IDN?"))
        # counter.settimeout(10000)
        # print(counter.send(":INITiate:CONTinuous ON"))
    finally:
        counter.close()