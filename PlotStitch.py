# -*- coding: utf-8 -*-
"""
Created on Fri Sep  4 13:27:33 2020

@author: ryan.robinson


Stitches together all the data in the comb log directory
"""


import os
import numpy as np
import matplotlib.pyplot as plt

def main():
    datalocation = "\\".join([os.getcwd(),"TradeshowOscillatorData"])
    datafolders = ["2020-08-28_17-44-49_Weekend Run","2020-08-31_15-37-26_Weekend Run 2","2020-09-02_11-13-52_PC Shutdown","2020-09-03_16-29-07_Fixed Plots"]
    
    namearray = os.listdir("\\".join([datalocation,datafolders[0]]))
    print(namearray)
    
    # Object array
    objlist = []
    
    # Create a data object list
    for name in namearray:
        objlist.append(dataObject(datalocation,name))
    
    # Append all data to all objects
    for datafolder in datafolders:    
        for i in objlist:
            i.appendData(datafolder)
        
    # Plot all data with specific Y axis labels
    objlist[0].plotData("Temperature [C]")
    objlist[1].plotData("Repetition Rate [Hz]",True)
    objlist[2].plotData("Temperature [C]")
    objlist[3].plotData("Modelock Indication [1=On / 0=Off]")
    objlist[4].plotData("Photodetector Voltage [V]")
    objlist[5].plotData("Temperature [C]")
    
    return None






class dataObject:
    def __init__(self,datalocation,dataset):
        self.datalocation = datalocation
        self.dataset = dataset
        self.xdata = np.array([])
        self.ydata = np.array([])
        
        return None
    
    def appendData(self,timefolder):
        file = "\\".join([self.datalocation,timefolder,self.dataset,self.dataset+".csv"])       
        data = np.genfromtxt(file, delimiter=",", names=["x", "y"])
        self.xdata = np.append(self.xdata,data["x"])
        self.ydata = np.append(self.ydata,data["y"])
        
        return None
    
    def plotData(self,ylabel = "",subtract = False):
        plt.figure(self.dataset)
        plt.title(self.dataset)
        plt.xlabel("Time [s]")
        plt.ylabel(ylabel)
        plt.grid()
        if subtract:
            avg = np.average(self.ydata)
            self.ydata = self.ydata-avg
            plt.ylabel(ylabel + "\n+" + str(avg))
        plt.plot(self.xdata-self.xdata[0],self.ydata)
        plt.show()
        return None
    















if __name__=="__main__":
    main()













