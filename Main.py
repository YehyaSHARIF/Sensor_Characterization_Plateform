"""

@author: Yehya SHARIF

This file represents the main section to use the functions in order
to do the traction and repulsion phase and return a .csv file 
that contains all measured data from the test bench.

Be sure that all files represented in import section are in the same
folder of the main file.

"""

import Distance_Sensor as ds
from pynput import keyboard
# import Testing_Sensor as ts
import Testing_Sensor_Pressure as ts
import time
import matplotlib.pyplot as plt
import cr10.CR10_Duino as CR10
import csv
import Acquisation as aq
import traitement as trt

def write_lists_as_columns(file_path, title, *columns):
    """
    Description
    ----------
    It creates a .csv file that contains all the values measured in the test.
    
    Parameters
    ----------
    file_path : string
        The path of the output .csv file that you want to obtain.
    title : list
        Contains a list of titles for each parameter that you want to measure.
    *columns : lists
        The *columns syntax allows us to pass a variable number of arguments, 
        which will be treated as separate lists representing 
        the columns in the CSV file.

    Returns
    -------
    None.
    
    """
    # Check if all columns have the same length
    length = len(columns[0])
    if not all(len(col) == length for col in columns):
        raise ValueError("All columns must have the same length.")

    # The *columns syntax allows us to pass a variable number of arguments, which will be treated as separate lists representing the columns in the CSV file.
    with open(file_path, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(title)
        # The zip function takes elements from each list and combines them into tuples. Each tuple represents a row in the CSV file.
        for row in zip(*columns):
            # This line writes the current row (tuple) to the CSV file using the writer.writerow method          
            writer.writerow(row)
          
            

def on_key_press(key, target_key):
    
    if key == target_key:
        
        return False  # Stop listening

def wait_for_key(target_key_str):
    target_key = keyboard.KeyCode.from_char(target_key_str)
    
    with keyboard.Listener(on_press=lambda key: on_key_press(key, target_key)) as listener:
        listener.join()



# Code in the current section before waiting for the key
    
#initialiser les capteurs

testsensor= ts.Testing_Sensor_Pressure(port="/dev/ttyACM1",baud="9600")
Distance_Sensor = ds.Distance_Sensor(port="/dev/ttyACM0",baud=115200)

#initialiser le printer
printer = CR10.SerialDuino(port="/dev/ttyUSB0",baud="115200")
time.sleep(2)

print("the sensors and the printers are initialized")

print(" Click on h and Begin the homing movement")

#Homing
# wait_for_key("h") # working with Spyder only
value = input("Press Enter to continue:\n")

printer.home()
printer.purgeSerial()

#enter all the required variables to begin the test phase
print("enter all required values to begin the experiment")

output_property=input("give me the output property of the sensor (Pressure for example)(string):")
output_unit= input("give me the unit of the output property (Pascal for example)(string):")
axe=input("each axe you want? x,y or z:")
begin=int(input("Give me the first position that you want to begin the traction phase (integer between 0 and 305 in mm):"))
lo=int(input("Give me the initial lenght of the sensor:"))#length in mm
max_strain= float(input("give me the maximum strain that you want (0.5 for example, the value should be between 0 and 1):"))
end=float(begin+ max_strain*lo)
step=float(input("Give me please the step between each measurement in mm (float): "))
delay=float(input("Give me please the delay between each measurement in sec (float): "))
pause=float(input("Give me the delay between the two phases in sec:"))
sensor_version= input("Give me the sensor version ( ex:Sensor1 ) (string) to put it in the name of the csv file:")
cycle_number=input("Give me the cycle number ( ex:Cycle1 ) (string) to put it in the name of the csv file:")


csv_file_name= "./csv/"+cycle_number+ "_" + sensor_version + "_" + str(begin)+ "_" + str(end)+ "_" + str(max_strain*100)+ "_" + str(step)+ "_" + str(delay)+ "sec_" + str(pause)+ "sec.csv" 

print(" All inputs are specified !")

#Move the printer into the first position

# wait_for_key("f")
value = input("Press go to the first position:\n")

aq.ChooseAxe(printer,axe)
aq.Move(printer,axe,begin)

#Traction phase

# wait_for_key("t")
value = input("Press Enter to To begin the traction:\n")

printer_positions_traction,sensor_positions_traction,volts_traction,t1=aq.TestPhaseAcquisition(printer,testsensor,Distance_Sensor,output_property,output_unit,axe,begin,end,step,delay)

#pause phase
sensor_positions_pause,volts_pause,t2=aq.PausePhaseAcquisition(printer,testsensor,Distance_Sensor,output_property,output_unit,delay,pause)


#Repulsion Phase
printer_positions_repulsion,sensor_positions_repulsion,volts_repulsion,t3=aq.TestPhaseAcquisition(printer,testsensor,Distance_Sensor,output_property,output_unit,axe,end,begin,-step,delay)
print("The repulsion phase is finished!") 

#Calculate the displacement,strain
printer_strain_t=trt.Strain_Calculation(printer_positions_traction,volts_traction,lo)
printer_strain_c=trt.Strain_Calculation(printer_positions_repulsion,volts_repulsion,lo)
printer_disp_t= trt.Displacement_Calculation(printer_positions_traction,volts_traction)
printer_disp_c= trt.Displacement_Calculation(printer_positions_repulsion,volts_repulsion)
sensor_strain_t=trt.Strain_Calculation(sensor_positions_traction,volts_traction,lo)
sensor_strain_c=trt.Strain_Calculation(sensor_positions_repulsion,volts_repulsion,lo)
sensor_strain_p=trt.Strain_Calculation(sensor_positions_pause,volts_pause,lo)
sensor_disp_t= trt.Displacement_Calculation(sensor_positions_traction,volts_traction)
sensor_disp_c= trt.Displacement_Calculation(sensor_positions_repulsion,volts_repulsion)
sensor_disp_p=trt.Displacement_Calculation(sensor_positions_pause,volts_pause)
#reverse the electrical backward list to do the hysterisis plot
rev_printer_strain_c = printer_strain_c.copy()
rev_printer_strain_c.reverse()
rev_sensor_strain_c = sensor_strain_c.copy()
rev_sensor_strain_c.reverse()

#plot the hysterisis graph



plt.plot(printer_strain_t,volts_traction,color='black', linewidth = 1,
         marker='o', markerfacecolor='black', markersize=3,label="traction")
plt.plot(rev_printer_strain_c,volts_repulsion,color='red', linewidth = 1,
         marker='o', markerfacecolor='red', markersize=3,label="repulsion")
plt.xlabel('printer_strain')
plt.ylabel(output_property+"("+output_unit+")")
plt.legend()


# wait_for_key("c")
value = input("Press Enter to create a .csv file")

#Create the .csv file
title=["printer Position Traction (mm)","Sensor Position Traction (mm)",output_property+" Traction("+output_unit+")",
       "time of traction(sec)","printer Position Repuslsion(mm)","Sensor Position Repulsion(mm)",
       output_property+" Repulsion("+output_unit+")","time of repulsion(sec)","Printer Strain Traction(percentage)",
       "Printer Strain Repulsion(percentage)","Sensor Strain Traction(percentage)","Sensor Strain Repulsion(percentage)",
       "Printer Displacement Traction(mm)","Printer Displacement Repuslion(mm)","Sensor Displacement Traction(mm)","Sensor Displacement Repulsion(mm)"]
data=[printer_positions_traction,sensor_positions_traction,volts_traction,
      t1,printer_positions_repulsion,sensor_positions_repulsion,
      volts_repulsion,t3,printer_strain_t,
      printer_strain_c,sensor_strain_t,sensor_strain_c,
      printer_disp_t,printer_disp_c,sensor_disp_t,sensor_disp_c]
write_lists_as_columns(csv_file_name,title,printer_positions_traction,sensor_positions_traction,volts_traction,t1,printer_positions_repulsion,sensor_positions_repulsion,
      volts_repulsion,t3,printer_strain_t,rev_printer_strain_c,sensor_strain_t,rev_sensor_strain_c,
      printer_disp_t,printer_disp_c,sensor_disp_t,sensor_disp_c)
    

