"""

@author: Yehya SHARIF

This file represents all required functions to calculate the strain 
and the displacement after the data aquisition phase.

        
"""
def Strain_Calculation(position_list,electrical_list,lo):
    """
    Description:this function calculate the strain(pourcentage) at 
    each step of the test
    
    Parameters
    ----------
    lo: float in mm
         the first lenght measured by the caliper
    position_list : float list in mm
        the list returned by the traction and repulsion function(it can be from the slider or the laser sensor)
    electrical_list : float list in kohm
        the list returned by the traction and repulsion function

    Returns
    -------
    strain_list : float list
        the calculated strain in percentage
    """
    strain_list=[None]*len(position_list)
    z1=position_list[0] #the first position
    for i in range (len(strain_list)):
       
        z2=position_list[i]# the position at each step
        strain_list[i]=round(abs(((z2-z1)*100)/lo),2)
    return strain_list  
    
def Displacement_Calculation(position_list,electrical_list):
    """
    Description:
        
        this function calculate the displacement at each step of 
        the test
    
    Parameters
    ----------
    position_list : float list in mm
        the list returned by the traction and repulsion function(it can be from the slider or the laser sensor)
    electrical_list : float list in kohm
        the list returned by the traction and repulsion function

    Returns
    -------
    displacement_list :  float list
        the calculated displacement in mm

    """
    displacement_list=[None]*len(position_list)
    z1=position_list[0] #the first position
    for i in range(len(displacement_list)):
        z2=position_list[i] #the position at each step
        displacement_list[i]=round(abs(z2-z1),2)
    return displacement_list  

def shift(Sensor_reading_list):
    """
    Description:
        
        this function shift the measured position t obtain a full
        list of positive positions to facilate the calculation of
        displacement and the strain
   
        use this function only if you obtain negative
        position from the laser sensor    
        
    Parameters
    ----------
    Sensor_reading_list : float list negative and positive one
        
      the list that contains the negative and positive output position 
      measured from the laser sensor

    Returns
    -------
    Sensor_reading_list : positive float list 
      
     the list that contains only the positive output

    """
    #plus petit nombre negative
    shift=abs(Sensor_reading_list[len(Sensor_reading_list)])
    for i in range(len(Sensor_reading_list)):
       Sensor_reading_list[i]+=shift #add the shift to obtain a positive float list
    return Sensor_reading_list  
