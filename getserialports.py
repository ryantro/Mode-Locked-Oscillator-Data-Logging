# -*- coding: utf-8 -*-
"""
Created on Mon Aug 24 17:47:29 2020

@author: ryan.robinson
"""

import serial.tools.list_ports
 
ports = list(serial.tools.list_ports.comports())
for p in ports:
    print(p)