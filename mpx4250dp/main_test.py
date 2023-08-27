#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jan 25 17:23:53 2022

@author: pchaillo

script that read the pressure sensor, display the value in the terminal, and record them in a text file (choose the name in this script)
"""


import MPX4250DP_Duino as SD


s = SD.SerialDuino(port="/dev/ttyACM0",baud="9600")


nom_fichier = "experience_03_05.txt"

f = open(nom_fichier,'a')

while 1 :
    s.UpdateSensors()
    pressure = s.GetPressure()
    print("Pression dans la paire de chambre (kPa) : " + str(pressure))
    f.write(str(pressure)+'\n')
    f.close()
    f = open(nom_fichier,'a')

    # senso = s.sensor
    # print(str(senso.GetPressure()))
    # print(str(s.sensor.GetPressure()))

