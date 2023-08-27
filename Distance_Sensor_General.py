# -*- coding: utf-8 -*-
"""
Created on Tue Jan 25 17:23:53 2022

@author: pchaillo and Yehya SHARIF

This file represents all required functions to initialise the distance sensor 
 and read the measured distance of this sensor from the arduino.


"""
from Sensor import Sensor
import serial 
import hc-c1100-p.HG_C1100_P as hg_sensor

class Distance_Sensor_General(Sensor):
    
    def __init__(self):
            """
            
        This function is to initialise an instance object of the class sensor    

        Returns
        -------
        None.

            """ 
        self.sensor = hg_sensor.SerialDuino

    
    def UpdateSensor(self):
        """
        It's only to update and split the message of the arduino and get the output distance 
        measured from the laser sensor in the experiment

        Returns
        -------
        the measured value (the distance in mm)

        """
        self.sensor.UpdateSensor()
    
    def get_value(self):
        
        self.value = self.sensor.GetDist()
        
        return self.value
    
    