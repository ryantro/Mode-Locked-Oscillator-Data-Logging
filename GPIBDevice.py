# -*- coding: utf-8 -*-
"""
Created on Mon Aug 24 13:20:28 2020

@author: ryan.robinson
"""

import pyvisa

class GPIBDevice:
    def __init__(self,GPIBNum,GPIBSlot):
        self.rm = pyvisa.ResourceManager()
        # View all GPIB Devices with rm.list_resources()
        # print(rm.list_resources())
        self.GPIBstr = 'GPIB%s::%s::INSTR' %(GPIBSlot,GPIBNum)

        return None
    
    def querydevice(self,cmd):
        '''Open device, send command, and close device'''
        self.inst = self.rm.open_resource(self.GPIBstr,write_termination = '\n')
        self.inst.clear()
        read=self.inst.query('%s' %cmd)
        self.inst.clear()
        self.inst.close()
        return read
    
    def close(self):
        self.inst.close()
        return None
        
