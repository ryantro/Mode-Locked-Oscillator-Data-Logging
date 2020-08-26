# -*- coding: utf-8 -*-
"""
Created on Tue Aug 25 17:23:01 2020

@author: ryan.robinson

Docs:
https://nidaqmx-python.readthedocs.io/en/latest/
"""

import nidaqmx


class NIUSB6210Device:
    def read(self):
        with nidaqmx.Task() as task:
            task.ai_channels.add_ai_voltage_chan("Dev1/ai0")
            return task.read()

# FOR TESTING PURPOSES
if __name__=="__main__":
    A = NIUSB6210Device()
    print(A.read())