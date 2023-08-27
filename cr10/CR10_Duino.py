import numpy as np
import serial
import time

class SerialDuino:

    def __init__(self):
        # PARAM7TRES
        self.port = '/dev/ttyUSB0'
        self.baud = 115200

        #INIT
        self.ser = serial.Serial(self.port,self.baud, timeout = 0.1) 

        self.Condition = False
        self.Increment = 0.1 # mm
        self.DirectionSign = np.sign(self.Increment)
        self.Stop = 5.5
        self.ErrorStr = 'err'
        # Feedrates stuff ... max available feedrates are displayed at bootup of the CR10 (in mm/s!)
        self.FeedRateXY = 1800 # mm/min, this is the unit used to set them (not mm/s!)
        self.FeedRateZ = 300 # mm/min

    def purgeSerial(self):
        Finished = False
        print('Purging serial ...')		
        while Finished != True:
            ReceivedText = ''
            ReceivedText = self.ser.readline().decode()
            print(ReceivedText)        
            if (ReceivedText == ''):
                Finished = True
                print('Purging serial ... Finished!')

    def setCondition(self,Condition_ext):
        #global Condition
        self.Condition = Condition_ext

    def sendCommand(self,CommandStr, BoolPrint = 0):
        self.ser.write((CommandStr+'\n').encode())
        time.sleep(0.0005) 
        # print("TEST")
        ReturnStr = self.ser.readline() #just relying on the timeout here ...
        if BoolPrint:
        #if True:
            print('ReturnedStr: '+ ReturnStr)
        return ReturnStr.decode()

    def calcTrajectoryExecutionTime(self,CurrentPos, TargetPos):
        
        Diff = [TargetPos[0]-CurrentPos[0], TargetPos[1]-CurrentPos[1], TargetPos[2]-CurrentPos[2]]
        TimeXYZ = (np.sqrt(Diff[0]**2 + Diff[1]**2 + Diff[2]**2)/FeedRateXY) * 60 # The feedrate actually applies to the total movement, not the axis independently
        TimeZ = (abs(Diff[2])/self.FeedRateZ) * 60 
        MaxTime = max(TimeXYZ, TimeZ) # Execution speed is limited by the Feedrate of the Z axis.     
        
        return MaxTime

    def getCurrentPosition(self):
        FullPositionStr = self.sendCommand('M114')
        OkStr = self.ser.readline()
        if OkStr.decode() != 'ok\n':
            print('Didn\'t get ok from M114')	
            return self.ErrorStr
        
        SplitStr = FullPositionStr.split(':')
        Split1 = SplitStr[1]
        Split2 = SplitStr[2]
        Split3 = SplitStr[3]

        SplitForX = Split1.split('Y')
        CurrentX = float(SplitForX[0])

        SplitForY = Split2.split('Z')
        CurrentY = float(SplitForY[0])

        SplitForZ = Split3.split('E')
        CurrentZ = float(SplitForZ[0])    
        
        return [CurrentX, CurrentY, CurrentZ]

    def driveToHeight(self,Position):
        OkStr = self.sendCommand('G0 Z'+str(Position))
        if OkStr != 'ok\n':
          print('Didn\'t get ok from G0')

    def driveToPosition(self,X,Y,Z):
        OkStr = self.sendCommand('G0 '+ 'X'+str(X) + ' Y'+str(Y) + ' Z'+str(Z))
        if OkStr != 'ok\n':
            print('Didn\'t get ok from G0')

    def robustGetCurrentPosition(self):
        MaxFailCount = 10
        FailCounter = 0
        
        while FailCounter <= MaxFailCount:
            CurrentPos = getCurrentPosition2()
            if not CurrentPos==self.ErrorStr:
                return CurrentPos
            else:
                print('Uff!')
                purgeSerial()
            
            FailCounter = FailCounter + 1
            print('FailCounter: ' + str(FailCounter))
        
        print("Something's wrong!")
        return self.ErrorStr
                
    	
    def driveUntilCondition(self,Sign=1):	
       # global Condition 
        i = 0
        CurrentPos = robustGetCurrentPosition()
        CurrentZ = CurrentPos[2]
        CurrentTarget = CurrentZ + Sign*self.Increment # we are at some position and the next command will drive us one increment further
        driveToPosition(CurrentTarget)
        while(not self.Condition):
            i = i + 1
            CurrentPos = robustGetCurrentPosition()
            CurrentZ = CurrentPos[2]
            #print('CurrentZ: '+ str(CurrentZ))
            #print('Current Target: '+str(CurrentTarget))
            
            BeyondStop = False
            if self.DirectionSign == 1:
                BeyondStop = CurrentZ > self.Stop
            else:
                BeyondStop = CurrentZ < self.Stop                                        
                    
            if abs(CurrentZ-CurrentTarget) < 0.9*abs(self.Increment):                    
                CurrentTarget = CurrentTarget + Sign*self.Increment # If we're within one Increment of reaching our target, dispatch the next one
                #print('Next Target: '+str(CurrentTarget))
                driveToPosition(CurrentTarget)		    
            		    
            self.Condition = False # reset
            FullPositionStr = self.sendCommand('M114')    
        
        OkStr = SerialObj.readline()
        return

                
    def home(self):
        OkStr = self.sendCommand('G28')  
        Finished = False
        while Finished != True:
            Str = self.ser.readline()
            # print(Str) # TRES UTILES POUR IMPRIMER LES RETOURS
            if Str.decode() == 'ok\n':            
                Finished = True            
                self.sendCommand('G0 F' + str(self.FeedRateXY)) # Set the feedrate to the desired value
                print('Finished homing')
                break
