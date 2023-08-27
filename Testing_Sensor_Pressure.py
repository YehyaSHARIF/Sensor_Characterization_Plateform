"""
Created on Tue Jan 25 17:23:53 2022

@author: pchaillo and Yehya SHARIF

This file represents all required functions to initialise the tested sensor 
 and read the measured voltage of this sensor from the arduino.


"""
from Sensor import Sensor
import serial 
import time  
import mpx4250dp.MPX4250DP_Duino as mpx


class Testing_Sensor_Pressure(Sensor):

    def __init__(self, port, baud):
            """
            
        This function is to initialise an instance object of the class sensor    

        Returns
        -------
        None.

            """
            super().__init__(port, baud)# The super() function is used to give access to methods and properties of a parent or sibling class.
            self.sensor = mpx.SerialDuino(port,baud)

    
    def flush(self):
        """
        to update the measured data and get a new data at each 0.1 sec
                    
        Returns
        -------
        None.

        """
        self.sensor.ser.flush()
        self.sensor.ser.flushInput()
        self.sensor.ser.flushOutput()
        time.sleep(0.1)
        
    def UpdateSensor(self):
        """
        It's only to update and split the message of the arduino and get the output voltage 
        measured from the tested sensor in the experiment

        Returns
        -------
        the measured value (the voltage in V)

        """
        self.sensor.UpdateSensors()
    
    def get_value(self):
        self.value = self.sensor.GetPressure()
        return self.value
    
    
