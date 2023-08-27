#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jan 25 17:23:53 2022

@author: pchaillo
"""

import serial


class SerialDuino:

    def __init__(self):
        # PARAM7TRES
        self.port = '/dev/ttyACM1'
        self.baud = 115200

        #INIT
        self.dist = 0
        self.ser = serial.Serial(self.port,self.baud) 

    def UpdateSensors(self):

        ligne_raw = str(self.ser.readline())
        # print(ligne_raw)

        ligne = ligne_raw.split(';')
        # ligne = float(ligne_raw)

        # print(ligne) # for debug
        if len(ligne) > 2:
            # print(ligne[3]) # for debug
            try:
                self.dist = float(ligne[1])
                # self._presB = float(ligne[2])
                # self._presC = float(ligne[3])
                # print(self.dist)

            except:
                print('Attention, lecture impossible')
                a = 0

    def GetDist(self):
        # print(str(self._pres)) # for debug
        return self.dist

