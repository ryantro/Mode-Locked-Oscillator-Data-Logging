# -*- coding: utf-8 -*-
"""
Created on Mon Aug 24 12:55:41 2020

@author: ryan.robinson


From Vescent Oscillator
- log mode lock indicator
- cavity temp

Counter
- log rep rate on counter

Temperature sensor
- log room temp

Powermeter
- log optical power



"""

import SLICEDevice
import os
import time
import numpy as np


def main():
    # TIME AND INTERVAL IN WHICH TO TAKE DATA
    totaltime = 50 # seconds
    timeinterval = 10 #seconds

    # START TIME OF THE PROGRAM
    itime = time.strftime("%Y-%m-%d_%H-%M-%S")    
    
    # MEASUREMENT OBJECTS
    #Counter = GPIBDevice.GPIBDevice(1,1)
    Oscillator = SLICEDevice.SLICE(3)
    
    # DATA TAKING OBJECTS
    #CounterData = DataFile(itime,"CounterData")
    ModeLockData = DataFile(itime,"ModeLockData")
    CavTempData = DataFile(itime,"CavityTempData")
    
    try:
        for i in range(0,totaltime,timeinterval):
            print("Time {} out of {}".format(str(i),str(totaltime)))
            
            # COLLECT AND SAVE COUNTER DATA
            #countervalue=Counter.querydevice('FETC?')
            #CounterData.appendData(countervalue)
            
            # COLLECT AND SAVE MODELOCKED STATUS
            modelockval = Oscillator.SliceSend('MODELOK?')
            if "ON" in modelockval:
                modelockint = 1
            else:
                modelockint = 0
            ModeLockData.appendData(modelockint)
            
            # COLLECT AND SAVE CAVITY TEMP
            cavitytemp = Oscillator.SliceSend('CAVTEMP?')
            CavTempData.appendData(cavitytemp)
            
            
            # WAIT A TIME INTERVAL
    
            time.sleep(timeinterval)
    except KeyboardInterrupt:
        print("Keyboard Interrupt Triggered")
    finally:
        # CLOSE DEVICES
        Oscillator.close()
        #Counter.close()
        # MAKE SURE DATA FILES ARE CLOSED
        ModeLockData.close()
        CavTempData.close()
    
    
    return None


class DataFile:
    '''Data file object that will store and save data for us'''
    def __init__(self,itime,dataname):
        '''Create the folder and init data arrays'''
        self.logfolder = str('\\'.join([os.getcwd(),'TradeshowOscillatorData',itime,dataname]))
        self.savefile = self.logfolder + '\\' + dataname + ".csv"
        #self.timesavefile = self.logfolder + '\\' + dataname + "_time.csv"
        os.makedirs(self.logfolder)
        self.data = []
        self.timedata = []
        return None
        
    def appendData(self,line):
        '''Add data to array and save it'''
        #self.data.append(line)
        #self.timedata.append(time.time())
        
        # SAVE DATA
        self.file = open(self.savefile,'a')
        self.file.write(",".join([str(time.time()),str(line)+'\n']))
        self.file.close()
        return None
    
    def close(self):
        self.file.close()
        return None

if __name__=="__main__":
    main()