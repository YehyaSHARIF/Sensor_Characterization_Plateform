"""
@author: Yehya SHARIF

"""
#import RubberSensor as rs # you can import the sensor that you want to measure the accuracy and the precision
import os
import pandas as pd
import matplotlib.pyplot as plt
from itertools import chain
import math
import random
from statistics import mean
from scipy import stats
import numpy as np

def read_csv_files(path):
    '''
    This function take the path of a folder, and return all files
    in the folder.
    
    For example:
        cycles_list=read_csv_files("./csv/")
    '''
   

    liste = os.listdir(path)
    cycles_list=[]
    for i in liste:
        
        cycle = pd.read_csv( path + i )
        cycles_list.append(cycle)
    
    return cycles_list

def split(cycles_list,title):
    '''
    This function takes the cycles_list and the title of the desired column as input,
    and returns a list that contains all columns with the desired title in each cycle
    
    For example: printer_traction_pos_cycles_list=split(cycles_list,'printer Position Traction (mm)')
     
    '''
    output_list=[None]*len(cycles_list)

    for i in range(len(cycles_list)):
     
        output_list[i]=cycles_list[i][title]
    
    return output_list

def plot_cycles_two_phase(title, xtitle, ytitle, xlist_1, ylist_1, xlist_2, ylist_2):
    """
    This function takes two sets of x and y lists corresponding to two phases,
    as well as the cycles represented in the CSV folder, and plots all of those cycles
    
    For example:
        
    plot_cycles_two_phase("Current Versus Time", "Time(sec)", "i(microA)", time_traction_cycles_list, current_traction_cycles_list, time_repulsion_cycles_list, current_repulsion_cycles_list)

    """ 
    plt.title(title)
    plt.xlabel(xtitle)
    plt.ylabel(ytitle)
    # colors list
    color_list = ["black", "red", "orange","sienna","green","blue","cyan","darkgray","olive","purple"]
    
    for i in range(len(xlist_1)):
        if len(color_list) == 0:
            # If all colors have been used, start reusing them
            color_list = ["black", "red", "orange", "sienna", "green", "blue", "cyan", "darkgray", "olive", "purple"]
        
        random_color = random.choice(color_list)
        color_list.remove(random_color)  # Remove the selected color from the list
        plt.plot(xlist_1[i], ylist_1[i], random_color, label='cycle ' + str(i+1) + ' Traction', linewidth=1, marker='.', markersize=4)
        plt.plot(xlist_2[i], ylist_2[i], random_color, label='cycle ' + str(i+1) + ' Repulsion', linewidth=1, marker='.', markersize=4)
    plt.legend()

def plot_cycles_one_phase(title, xtitle, ytitle, xlist_1, ylist_1):
    '''
This function takes the x and y lists of a single phase, 
along with all cycles represented in the CSV folder, and plots all of those cycles.

For example: plot_cycles_one_phase(" Power loss Versus Time", "Time(sec)", "Power Loss(dB)", time_traction_cycles_list, power_loss_traction_cycles_list)
    '''
    plt.title(title)
    plt.xlabel(xtitle)
    plt.ylabel(ytitle)
    color_list = ["black", "red", "orange","sienna","green","blue","cyan","darkgray","olive","purple"]
    for i in range(len(xlist_1)):
        if len(color_list) == 0:
            # If all colors have been used, start reusing them
            color_list = ["black", "red", "orange", "sienna", "green", "blue", "cyan", "darkgray", "olive", "purple"]
        
        random_color = random.choice(color_list)
        color_list.remove(random_color)  # Remove the selected color from the list
        plt.plot(xlist_1[i], ylist_1[i], random_color, label='cycle ' + str(i+1) + ' Traction', linewidth=1, marker='.', markersize=4)
    plt.legend() 
    
def plot_one_cycle_two_phase(title, xtitle, ytitle, xlist_1, ylist_1, xlist_2, ylist_2):
    '''
This function takes two sets of x and y lists corresponding to two phases,
as well as tone cycle represented in the CSV folder, and plots one cycle and two phases

For example: plot_one_cycle_two_phase ("Voltage Versus Time","Displacement(mm)","Voltage(V)",Sensor_traction_displacement_cycles_list[0], output_traction_cycles_list[0], Sensor_displacement_repulsion_reversed_cycles_list[0],output_repulsion_cycles_list[0])
    '''   
    plt.title(title)
    plt.xlabel(xtitle)
    plt.ylabel(ytitle)
    color_list = ["black", "red", "orange","sienna","green","blue","cyan","darkgray","olive","purple"]
    plt.plot(xlist_1, ylist_1, color=random.choice(color_list), label='Traction', linewidth=1, marker='.', markersize=4)
    plt.plot(xlist_2, ylist_2, random.choice(color_list), label='Repulsion', linewidth=1, marker='.', markersize=4)
    plt.legend() 

def reverse(liste):
    '''
    This function reverse a set of series (values only)
    For example:printer_strain_repulsion_reversed_cycles_list=reverse(printer_strain_repulsion_cycles_list)
    '''
    reversed_list=[None]*len(liste)
    
    for i in range(len(liste)):
        
        reversed_list[i]=liste[i].iloc[::-1]
        
    return reversed_list 
def reverse_reset_index(liste):
    '''
    This function reverse a set of series (index only)
    For example: output_repulsion_cycles_list_rev=reverse_reset_index(output_repulsion_cycles_list)
    '''
    reversed_list=[None]*len(liste)
    
    for i in range(len(liste)):
        
        reversed_list[i]=liste[i].iloc[::-1].reset_index(drop = True)
        
    return reversed_list 

def hysterisis_cycles_calculation(physical_forward_list,physical_backward_list,electrical_forward_list,electrical_backward_list):
    '''
    Explication
    -------
    this function takes the lists of the physical and electrical measurements in forward and backward directions and in each cycle,
    and returns the following lists

    Returns
    -------
    diff_list : float list
        
         this is the difference between the electrical values in forward and backward directions in each cycle
        
    max_percentage_list : float list
         
         this is a list of the maximum hysterisis percentage in each cycle
    
    avg_hysterisis_list : float list
    
        this is a list of the average hysterisis percentage in each cycle
        
    Example: 
    ---------
    
    diff_list,max_hysterisis_percentage_list,avg_hysterisis_percentage_list = hysterisis_cycles_calculation( Sensor_traction_strain_cycles_list,Sensor_repulsion_strain_cycles_list,output_traction_cycles_list,output_repulsion_cycles_list_rev)
    mean_avg_hysterisis_percentage=mean(avg_hysterisis_percentage_list)
    mean_max_hysterisis_percentage=mean(max_hysterisis_percentage_list)
    '''
    
    #reverse the electrical backward list
    print(electrical_forward_list)
    print(electrical_backward_list)
    diff_list=[None]*len(physical_forward_list)
    sum_diff_list=[None]*len(physical_forward_list)
    avg_sum_diff=[None]*len(physical_forward_list)
    max_diff_list=[None]*len(physical_forward_list)
    max_loading_electrical_list=[None]*len(physical_forward_list)
    min_loading_electrical_list=[None]*len(physical_forward_list)
    max_percentage_list=[None]*len(physical_forward_list)
    output_electrical_range=[None]*len(physical_forward_list)
    avg_hysterisis_list=[None]*len(physical_forward_list)
    for i in range(len(physical_forward_list)):
        diff_list[i]=abs(electrical_forward_list[i]-electrical_backward_list[i])
        sum_diff_list[i]=sum(diff_list[i])
        #calculate the average sum of the diff list to be used in average hysteris formula
        avg_sum_diff[i]=sum_diff_list[i]/len(diff_list[i])
        max_diff_list[i]=max(diff_list[i])
        #calculate the maximmum and the minimum boundaries of the output electrical range
        max_loading_electrical_list[i]=max(chain(electrical_forward_list[i],electrical_backward_list[i]))
        min_loading_electrical_list[i]=min(chain(electrical_forward_list[i],electrical_backward_list[i]))
        output_electrical_range[i]=(max_loading_electrical_list[i]-min_loading_electrical_list[i])
        max_percentage_list[i]=(max_diff_list[i]*100)/output_electrical_range[i]
        avg_hysterisis_list[i]=(avg_sum_diff[i]*100)/output_electrical_range[i]  
    return diff_list,max_percentage_list,avg_hysterisis_list

#linear regression traction(Powerloss=F(Strain))
def linear_function_plot(title, xtitle, ytitle,x,y, xlist_1, ylist_1):
    '''
    this function takes list of series of the x measurement,and of the y measurement and plot the linear relation betwwen the x and y properties

    Returns
    -------
    slope_mean : float 
        The mean of slopes of each linear function of each cycles 
    intercept_mean : float
        The mean of intercept of each linear function of each cycles 
    linear_function : float list
        list of y values calculated by the linear regression function
    std_err : float list
        it tells you how wrong the regression model is on average using the units of the response variable.

     Example
     ---------
     slope_t,intercept_t,linear_function_t,std_error_t=linear_function_plot("PowerLoss versus strain","Strain(%)","Power Loss(dB)",Sensor_traction_strain_cycles_list[1],power_loss_traction_cycles_list[1],Sensor_traction_strain_cycles_list,power_loss_traction_cycles_list)
     slope_r,intercept_r,linear_function_r,std_error_r=linear_function_plot("PowerLoss versus strain","Strain(%)","Power Loss(dB)",Sensor_repulsion_strain_cycles_list[1],power_loss_repulsion_cycles_list[1],Sensor_repulsion_strain_cycles_list,power_loss_repulsion_cycles_list)
    '''
    linear_function=[None]*len(x)
    slope=[None]*len(xlist_1)
    intercept=[None]*len(xlist_1)
    r=[None]*len(xlist_1)
    p=[None]*len(xlist_1)
    std_err=[None]*len(xlist_1)
    for i in range(len(xlist_1)):
    
      slope[i],intercept[i],r[i],p[i],std_err[i]=stats.linregress(xlist_1[i],ylist_1[i])
    
    slope_mean=mean(slope)
    intercept_mean=mean(intercept)
    linear_function=slope_mean*xlist_1[0]+intercept_mean # we choose to pick the first cycle for regression to avoid any error when there are less than 2
    plot_cycles_one_phase(title, xtitle, ytitle, xlist_1, ylist_1)
    plt.plot(xlist_1[0],linear_function)
    plt.show()

    return slope_mean,intercept_mean,linear_function,std_err

def accuracy(lenght,y_data_sheet,number_of_samples):
    """
    This function takes two inputs (lenght,resistor_data_sheet,number_of_samples) and return:
        1. error_list:the difference list between the linear and the actual measured value of the electrical list
        2. max_error: the non_linearity error percentage between the linear one and the actual one
        3. slope: sensitivity of the linear function
    and plot the measured value with the true value to visualize the absolute error
    
    Example: res_measure_1,avg_resis_1,abs_error_1=accuracy(lenght_1,res_data_sheet_1,30)
    
    """
    y_measure=[None]*number_of_samples#to store the y measures
    abs_error=[None]*number_of_samples# to calculate the absolute error
    y_datasheet_list=[None]*number_of_samples
    avg_y_list=[None]*number_of_samples
    t=[None]*number_of_samples
    sum_y=0#to calculate the average of the measured y
    for i in range(number_of_samples):
       t[i]=i
       y_measure[i]=RubberRead() # you can change it based on the sensor that you want to characterise
       y_datasheet_list[i]=y_data_sheet
       sum_y+=y_measure[i]
    avg_y=sum_y/number_of_samples
    for i in range(number_of_samples):
        avg_y_list[i]=avg_y
        abs_error[i]=abs(avg_y-y_data_sheet)
    #plot the actual and the linear curve of the electrical characteristics in a specific input range
    
    plt.xlim([0, number_of_samples])
    plt.ylim([0, 2])
  
    plt.plot(t,y_measure,color='black', linewidth = 1,
             marker='o', markerfacecolor='black', markersize=3)
    plt.plot(t,y_datasheet_list,color='red')
    plt.plot(t,avg_y,color='blue')
    plt.show()
    return y_measure,avg_y,abs_error

def linearity_error(physical,electrical):
    
    """
    This function takes two inputs (physical,electrical) and return:
        1. linear_error_list:the difference list between the linear regression and the actual measured value of the electrical list
        2. linear_err: the non_linearity error percentage between the linear one and the actual one
        3. slope: sensitivity of the linear regression function
    Example:   linearity_error_list,linearity_error_1,sensitivity_12=linearity_error(printer_strain_t_linear_1,resistor_t_linear_1)
    """
    slope, intercept, r, p, std_err = stats.linregress(physical,electrical)
    linear_function=[None]*len(physical)
    linear_error_list=[None]*len(physical)
    for i in range(len(physical)):
     linear_function[i]= slope * physical[i]+intercept
     linear_error_list[i]=abs(linear_function[i]-electrical[i])
    max_error=max(linear_error_list)
    output_full_range=max(electrical)-min(electrical)
    linear_err=(max_error/output_full_range)*100
    plt.plot(physical,electrical,color='black', linewidth = 1,
             marker='o', markerfacecolor='black', markersize=3)
    plt.plot(physical, linear_function)
    plt.show()
    return linear_error_list,linear_err,slope    



''' To do the polynomial regression and to plot it
#polynomial regression traction(v=F(strain))
coef=np.polyfit(Sensor_strain_t_range,voltage_traction_range,4)
poly_reg=np.poly1d(coef)
x=np.linspace(7.8, 50,120)
plt.plot(Sensor_strain_t,voltage_traction, color='blue',label='Traction',linewidth = 1,
         marker='.', markerfacecolor='blue', markersize=4)

plt.plot(x,poly_reg(x),color='orange',label='PolynomialRelation')
'''

def powerloss(incident_power):
    '''
 function to compute the power loss from the incident power (useful for exemple to characterize optical sensor)

exemple : 
    current_repulsion_cycles_list[i]=(1/feedback_resistance)*output_repulsion_cycles_list[i] #  to convert voltage to current
    incident_power_traction_cycles_list[i] = (1/responsivity)*current_traction_cycles_list[i] # to convert current to incident power
    power_loss_traction_cycles_list[i] = powerloss(incident_power_traction_cycles_list[i])
    
    You can see also the Electrical Conversion.png
    '''
    Io_traction=incident_power[0]
    
    power_loss_list=[None]*len(incident_power)

    for i in range(len(incident_power)):
     
        power_loss_list[i]= 10 * math.log10(Io_traction/incident_power[i])
    
    return power_loss_list
    
cycles_list=read_csv_files("./csv/")   

printer_repulsion_disp_cycles_list=split(cycles_list,'Printer Displacement Repuslion(mm)')
printer_traction_disp_cycles_list=split(cycles_list,'Printer Displacement Traction(mm)')
printer_repulsion_disp_cycles_list=split(cycles_list,'Printer Displacement Repuslion(mm)')
pressure_traction_cycles_list=split(cycles_list,'Pressure Traction(KPa)')
pressure_repulsion_cycles_list=split(cycles_list,'Pressure Repulsion(KPa)')
printer_strain_repulsion_reversed_cycles_list=reverse(printer_repulsion_disp_cycles_list)
printer_strain_repulsion_reversed_cycles_list=reverse_reset_index(printer_strain_repulsion_reversed_cycles_list)
plot_one_cycle_two_phase ("Pressure Versus Displacement","Displacement(mm)","P(Kpa)",np.asarray(printer_traction_disp_cycles_list[0]), np.asarray(pressure_traction_cycles_list[0]), np.asarray(printer_strain_repulsion_reversed_cycles_list[0]),np.asarray(pressure_repulsion_cycles_list[0]))
diff_list,max_hysterisis_percentage_list,avg_hysterisis_percentage_list = hysterisis_cycles_calculation( printer_traction_disp_cycles_list,printer_repulsion_disp_cycles_list,pressure_traction_cycles_list,pressure_repulsion_cycles_list)
mean_avg_hysterisis_percentage=mean(avg_hysterisis_percentage_list)
mean_max_hysterisis_percentage=mean(max_hysterisis_percentage_list)
# slope_t,intercept_t,linear_function_t,std_error_t=linear_function_plot("PowerLoss versus strain","Strain(%)","Power Loss(dB)",printer_traction_disp_cycles_list[0],pressure_traction_cycles_list[0],printer_traction_disp_cycles_list,pressure_traction_cycles_list)
# slope_r,intercept_r,linear_function_r,std_error_r=linear_function_plot("PowerLoss versus strain","Strain(%)","Power Loss(dB)",printer_repulsion_disp_cycles_list[0],pressure_repulsion_cycles_list[0],printer_repulsion_disp_cycles_list,pressure_repulsion_cycles_list)

print("Mean maximum hysteresis (percentage): ")
print(mean_max_hysterisis_percentage)
print("Mean average hysteresis (percentage): ")
print(mean_avg_hysterisis_percentage)