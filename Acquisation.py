# -*- coding: utf-8 -*-
"""
Created on Wed Jul 26 12:08:47 2023

This file is used to  define the necessary functions to
collect measurements at each step of deformation by applying
an iterative motion during the stretching and contracting phases.

@author: Yahya
"""

import time 
import numpy as np


def ChooseAxe(printer,axe):
   
    
    if axe =="x":
         
        print("You choose axe x")
    elif axe =="y":

        print("You choose axe y")
    elif axe == "z":
       
        print("You choose axe z")
    else:
         
        print("You should specify x,y and z only.")

def Move(printer,axe,i):
    
    """
    Move the printer only on x, or y, or z axis into position i

    Parameters
    ----------
    
    printer : SerialDuino
        the object of instance of the CR10 printer
    
    axe : string
         the axe of movement(x,y, or z).

    i : float
        the desired position on the axe of movement

    Returns
    -------
    None.

    """
    if axe =="x":
        
        printer.driveToPosition(i,0,0)
    
    elif axe =="y":

        printer.driveToPosition(0,i,0)
    
    elif axe == "z":
      
        printer.driveToPosition(0,0,i)

    
def TestPhaseAcquisition(printer,TestSensor,DistSensor,output_property,output_unit,axe,begin,end,step,delay):
 
  printer_positions,sensor_positions,electrical_values,t=[],[],[],[]
  #take the measures in for loop
  start_time = time.time()  # Set a reference point as the start time
 
  for i in np.arange(begin,end+step,step):
  
    Move(printer,axe,i)
    time.sleep(delay)
    current_time = round(time.time() - start_time,4)  # Calculate the time difference
    t.append(current_time)
    printer_positions.append(i)
    sensor_position=DistSensor.process()
    electrical_value=TestSensor.process()
    sensor_positions.append(sensor_position)
    electrical_values.append(electrical_value)
    print("Current time(sec): "+str(current_time)+";Printer_position(mm): "+str(i)+";Sensor_position(mm): "+str(sensor_position),";"+output_property+"("+ output_unit+"):" +str(electrical_value))      
          
  return printer_positions,sensor_positions,electrical_values,t
  
def PausePhaseAcquisition(printer,TestSensor,DistSensor,output_property,output_unit,delay,pause):
 
     sensor_positions,electrical_values,t=[],[],[]
     start_time = time.time()  # Set a reference point as the start time
     
     
     while True:
               
       time.sleep(delay)
       current_time = round(time.time() - start_time,4)  # Calculate the time difference
       t.append(current_time)
       sensor_position=DistSensor.process()
       electrical_value=TestSensor.process()
       sensor_positions.append(sensor_position)
       electrical_values.append(electrical_value)
       
       print("Current time(sec): "+str(current_time)+";Sensor_position(mm): "+str(sensor_position)+";"+output_property+"("+ output_unit+"):"+str(electrical_value))
      
       if current_time >= pause: break
           
     return  sensor_positions,electrical_values,t
 