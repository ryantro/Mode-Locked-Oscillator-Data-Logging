# -*- coding: utf-8 -*-
"""
Created on Mon Aug 24 12:55:41 2020

@author: ryan.robinson


From Vescent Oscillator
- log mode lock indicator
- cavity temp

Counter
- log rep rate on counter

Slice QTC
- log room temp
- log internal box temp

Powermeter
- log optical power



"""

import SLICEDevice, USBDevice, NIUSB6210Device
import os
import time



def main():
    # INSTRAMENT ADDRESSES
    countername = 'USB0::0x0957::0x1707::MY50002091::0::INSTR'
    osccomport = 5
    qtcport = 3
    
    # DATA TAKING INTERVAL
    timeinterval = 1 #seconds

    # START TIME OF THE PROGRAM
    itime = time.strftime("%Y-%m-%d_%H-%M-%S")    
    
    
    try:
        # OPEN DEVICES
        Counter = USBDevice.USBDevice(countername)
        Oscillator = SLICEDevice.SLICE(osccomport)
        QTC = SLICEDevice.SLICE(qtcport)
        Photodetector = NIUSB6210Device.NIUSB6210Device()
        
        # DATA TAKING OBJECTS
        CounterData = DataFile(itime,"CounterData")
        ModeLockData = DataFile(itime,"ModeLockData")
        CavTempData = DataFile(itime,"CavityTempData")
        InBoxTempData = DataFile(itime, "InBoxTempData")
        RoomTempData = DataFile(itime, "RoomTempData")
        PhotodetectorData = DataFile(itime, "PhotodetectorData")
        
        i = 0
        # DATA TAKING LOOP
        while(True):
            print("Measurement Number {}".format(str(i)))
            i += 1
            
            # COLLECT AND SAVE COUNTER DATA
            counterval = Counter.send(":SENSe:DATA?")
            CounterData.appendData(counterval)
            
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
            
            # COLLECT AND SAVE IN BOX TEMPERATURE
            inboxtemp = QTC.SliceSend('TEMP? 1')
            InBoxTempData.appendData(inboxtemp)
            
            # COLLECT AND SAVE ROOM TEMP
            roomtemp = QTC.SliceSend('TEMP? 2')
            RoomTempData.appendData(roomtemp)
            
            # COLLECT AND SAVE PHOTODETECTOR POWER
            pdvoltage = Photodetector.read()
            PhotodetectorData.appendData(pdvoltage)
            
            # WAIT A TIME INTERVAL
            time.sleep(timeinterval)
            
    except KeyboardInterrupt:
        print("Keyboard Interrupt Triggered")
        
    finally:
        # CLOSE DEVICES
        Oscillator.close()
        Counter.close()
        QTC.close()
        
        # ENSURE DATA FILES ARE CLOSED
        ModeLockData.close()
        CavTempData.close()
        CounterData.close()
        InBoxTempData.close()
        RoomTempData.close()
    
    
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