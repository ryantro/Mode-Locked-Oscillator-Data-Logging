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
import matplotlib.pyplot as plt
import numpy as np


def main():
    # DATA TITLE
    title = "_Fixed Plots"
    
    # INSTRAMENT ADDRESSES
    countername = 'USB0::0x0957::0x1707::MY50002091::0::INSTR'
    osccomport = 5
    qtcport = 3
    
    # DATA TAKING INTERVAL
    timeinterval = 10 #seconds

    # START TIME OF THE PROGRAM
    itime = time.strftime("%Y-%m-%d_%H-%M-%S")
    # itime = "2020-09-02_11-13-52"
    itime = itime+title
    starttime = time.time()
    
    
    try:
        # OPEN DEVICES
        Counter = USBDevice.USBDevice(countername)
        Counter.settimeout(10000)
        #Counter.settimeout(timeinterval)
        Oscillator = SLICEDevice.SLICE(osccomport)
        QTC = SLICEDevice.SLICE(qtcport)
        Photodetector = NIUSB6210Device.NIUSB6210Device()
        
        # DATA TAKING OBJECTS
        CounterData = DataFile(itime,"CounterData","Frequency [Hz]",starttime,True)
        ModeLockData = DataFile(itime,"ModeLockData", "Modelocked? [1=Yes,0=No]",starttime)
        CavTempData = DataFile(itime,"CavityTempData","Temperature [C]",starttime)
        InBoxTempData = DataFile(itime, "InBoxTempData","Temperature [C]",starttime)
        RoomTempData = DataFile(itime, "RoomTempData","Temperature [C]",starttime)
        PhotodetectorData = DataFile(itime, "PhotodetectorData","Photodetector Voltage [V]",starttime)
        
        i = 0
        # DATA TAKING LOOP
        while(True):
            print("Measurement Number {}".format(str(i)))
            i += 1
            
            # COLLECT AND SAVE COUNTER DATA
            counterval = Counter.send("READ?") #READ:FREQ?
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
            CavTempData.appendData(cavitytemp.strip("CAVTEMP? "))
            
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
            #time.sleep(timeinterval)
            
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
    def __init__(self,foldername,dataname,ydatalabel = "",starttime = 0, subtract = False):
        '''Create the folder and init data arrays'''
        self.starttime = starttime
        self.subtract = subtract
        self.ydatalabel = ydatalabel
        self.count = 0
        self.plotinterval = 10
        self.dataname = dataname
        self.logfolder = str('\\'.join([os.getcwd(),'TradeshowOscillatorData',foldername,dataname]))
        self.savefile = self.logfolder + '\\' + dataname + ".csv"
        if(os.path.exists(self.logfolder==False)):
            os.makedirs(self.logfolder)
        self.data = []
        self.timedata = []
        return None
        
    def appendData(self,line):
        '''Add data to array and save it'''
        self.count += 1
        takeTime = time.time()
        #self.data.append(float(line))
        #self.timedata.append(takeTime-self.starttime)
        
        # Plot the data
        if self.count%self.plotinterval == 0:
            self.plotData()
        
        # SAVE DATA
        self.file = open(self.savefile,'a')
        self.file.write(",".join([str(takeTime),str(line)+'\n']))
        self.file.close()
        return None
    
    def plotData(self):
        '''Plot the data'''
        print("plotting data")
        # LOAD AND CLEAR THE FIGURE
        plt.figure(self.dataname)
        plt.cla()
        
        # FORMAT FIGURE
        plt.grid()
        plt.title(self.dataname)
        plt.xlabel("Time [seconds]")
        plt.ylabel(self.ydatalabel)
        
        # IMPORT DATA
        data = np.genfromtxt(self.savefile, delimiter=",", names=["x", "y"])

        
        # ARE THESE BEING CENTERED AROUND AN AVERAGE?
        if self.subtract:
            avg = np.average(data["y"])
            cdata = data["y"]-avg
            plt.ylabel(self.ydatalabel + "\n+" + str(avg))
            plt.plot(data["x"]-self.starttime, cdata)
        else:
            plt.plot(data["x"]-self.starttime, data['y'])
        
        # SAVE AND SHOW PLOT
        plt.savefig(self.savefile.replace(".csv",".png"))
        plt.show()
        return None
    
    def close(self):
        self.file.close()
        return None

if __name__=="__main__":
    main()