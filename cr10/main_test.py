#!/usr/bin/env python3
        
# -*- coding: utf-8 -*-
"""
Created on 22/08/2022

@author: pchaillo

Script to use Creality CR10 printer as a test platform
"""

# import CR10Lib as CR10
# CR10.home()

import time
import CR10_Duino as CR10_test

height = 20

printer = CR10_test.SerialDuino()
time.sleep(2)
printer.home()

printer.purgeSerial()
position = printer.getCurrentPosition()
print(position)

Position = height
printer.driveToHeight(Position)
X = height
Y = height
Z = 0
printer.driveToPosition(X,Y,Z)

position = printer.getCurrentPosition()
print(position)


