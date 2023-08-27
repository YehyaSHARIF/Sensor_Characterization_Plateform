
"""
@author: Yehya SHARIF

This file defines an abstract class named "Sensor" 
(parent class of all sensors used in the test bench)

With this class, we can create several of child sensors.
"""

import serial 

class Sensor:
    
    #Abstract Class
    def __init__(self,port,baud):
            """
            
        This function is to initialise an instance object of the class sensor    

        Returns
        -------
        None.

            """ 
            # PARAM7TRES
            self.port = port
            self.baud = baud

            #INIT
            self.value = 0
            self.ser = serial.Serial(self.port,self.baud) 
    
   
    
    def UpdateSensor(self,index):
      
        pass
    
    def get_value(self):
        
        pass
    
    def process(self):
     """
     to return the desired measured value
                 
     Returns
     -------
     value: the measured value

     """
     self.UpdateSensor()
     value=self.get_value()
     return value
