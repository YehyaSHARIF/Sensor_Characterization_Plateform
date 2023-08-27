"""
Created on Tue Jan 25 17:23:53 2022

@author: pchaillo and Yehya SHARIF

This file represents all required functions to initialise the tested sensor 
 and read the measured voltage of this sensor from the arduino.


"""
from Sensor import Sensor
import serial 
import time  
class Testing_Sensor(Sensor):
    
    def flush(self):
        """
        to update the measured data and get a new data at each 0.1 sec
                    
        Returns
        -------
        None.

        """
        self.ser.flush()
        self.ser.flushInput()
        self.ser.flushOutput()
        time.sleep(0.1)
        
    def UpdateSensor(self,index):
        """
        It's only to update and split the message of the arduino and get the output voltage 
        measured from the tested sensor in the experiment

        Returns
        -------
        the measured value (the voltage in V)

        """
        ### to update the measured data and get a new data at each 0.1 sec 
        Sensor.flush(self)
        ###to split the arduino message and get the voltage only 
        ligne_raw = str(self.ser.readline())
        # print(ligne_raw)

        ligne_cut = ligne_raw.split("'")
        ligne_cut2 = ligne_cut[1].split("\\")
        ligne_cut3 = ligne_cut2[0].split(";")

        #print(ligne_cut3[0]) # for debug
        
        ###
        try:
            self.value = float(ligne_cut3[index])

        except:
            print('Attention, lecture impossible')
    
    def get_value(self):
        
        return self.value
    
    