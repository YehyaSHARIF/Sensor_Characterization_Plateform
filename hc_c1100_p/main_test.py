#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jan 25 17:23:53 2022

@author: pchaillo

script that read the pressure sensor, display the value in the terminal, and record them in a text file (choose the name in this script)

Sensors are connected to the A0, A1 and A2 pins and commincate trough serial connexion (see MPX4250DP.ino script)
"""


import HG_C1100_P as SD

s = SD.SerialDuino()

nom_fichier = "record_dist.txt"

f = open(nom_fichier,'a')

while 1 :
    s.UpdateSensors()
    dist = s.GetDist()
    print(dist)
    print("Distance en mm : " + str(dist))
    # print("kPa : " + str(pressure[0]) + ':' + str(pressure[1]) + ':'+ str(pressure[2]))
    f.write(str(dist)+'\n')
    f.close()
    f = open(nom_fichier,'a')

    # senso = s.sensor
    # print(str(senso.GetPressure()))
    # print(str(s.sensor.GetPressure()))

