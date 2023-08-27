#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jan 25 17:23:53 2022

@author: pchaillo
"""

import serial
import time
# ser = serial.Serial('/dev/ttyACM0',9600) # choisir le bon port serie si windows ('com1',9600) par exemple

# f = open('fichier.txt','a')

# while 1 :
#     print(str(ser.readline()))
#     f.write(str(ser.readline())+'\n')
#     f.close()
#     f = open('fichier.txt','a')


class SerialDuino:

    # class sensor:

    #     def __init__(self):
    #         self._pres = 0


    def __init__(self,port ='/dev/ttyACM0',baud = 9600 ):
        # PARAM7TRES
        self.port = port
        self.baud = baud

        #INIT
        self._pres = 0
        self.ser = serial.Serial(self.port,self.baud) 
        
    def flush(self):
         """
         to update the measured data and get a new data at each 0.1 sec
                     
         Returns
         -------
         None.

         """
         self.ser.flush()
         self.ser.flushInput()
         self.ser.flushOutput()
         time.sleep(0.1)
         
    def UpdateSensors(self):
        
        self.flush()
        ligne_raw = str(self.ser.readline())
        
        ligne = ligne_raw.split(';')

        #print("ligne raw:"+str(ligne_raw))
        #print("ligne :"+str(ligne)) # for debug
        if len(ligne) > 3:
            #print(ligne[3]) # for debug
            try:
                self._pres = float(ligne[3])
            except:
                # print('ok')
                a = 0
       
        
    def GetPressure(self):
        # print(str(self._pres)) # for debug
        return self._pres

