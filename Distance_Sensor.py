# -*- coding: utf-8 -*-
"""
Created on Tue Jan 25 17:23:53 2022

@author: pchaillo and Yehya SHARIF

This file represents all required functions to initialise the distance sensor 
 and read the measured distance of this sensor from the arduino.


"""
from Sensor import Sensor
import hc_c1100_p.HG_C1100_P as hc


class Distance_Sensor(Sensor):
    
    
    
    def __init__(self, port, baud):
     
        super().__init__(port, baud) #The super() function is used to give access to methods and properties of a parent or sibling class.
        self.sensor = hc.SerialDuino(port, baud)

    
    def UpdateSensor(self):
        """
        It's only to update and split the message of the arduino and get the output distance 
        measured from the laser sensor in the experiment

        Returns
        -------
        the measured value (the distance in mm)

        """
        self.sensor.UpdateSensors()
    

    
    def get_value(self):
        self.value = self.sensor.GetDist()
        return self.value
    
    
