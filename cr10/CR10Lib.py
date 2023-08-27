import numpy as np
import serial
import time

SerialObj = serial.Serial('/dev/ttyUSB0', 115200, timeout=0.1) #port used by CR 10
Condition = False
Increment = 0.1 # mm
DirectionSign = np.sign(Increment)
Stop = 5.5
ErrorStr = 'err'
# Feedrates stuff ... max available feedrates are displayed at bootup of the CR10 (in mm/s!)
FeedRateXY = 1800 # mm/min, this is the unit used to set them (not mm/s!)
FeedRateZ = 300 # mm/min

def purgeSerial():
    Finished = False
    print('Purging serial ...')		
    while Finished != True:
        ReceivedText = ''
        ReceivedText = SerialObj.readline().decode()
        print(ReceivedText)        
        if (ReceivedText == ''):
            Finished = True
            print('Purging serial ... Finished!')

def setCondition(Condition_ext):
    global Condition
    Condition = Condition_ext

def sendCommand(CommandStr, BoolPrint = 0):
    SerialObj.write((CommandStr+'\n').encode())
    #time.sleep(0.0005) 
    ReturnStr = SerialObj.readline() #just relying on the timeout here ...
    # print("TEST")
    if BoolPrint:
    #if True:
        print('ReturnedStr: '+ ReturnStr)
    return ReturnStr.decode()

def calcTrajectoryExecutionTime(CurrentPos, TargetPos):
    
    Diff = [TargetPos[0]-CurrentPos[0], TargetPos[1]-CurrentPos[1], TargetPos[2]-CurrentPos[2]]
    TimeXYZ = (np.sqrt(Diff[0]**2 + Diff[1]**2 + Diff[2]**2)/FeedRateXY) * 60 # The feedrate actually applies to the total movement, not the axis independently
    TimeZ = (abs(Diff[2])/FeedRateZ) * 60 
    MaxTime = max(TimeXYZ, TimeZ) # Execution speed is limited by the Feedrate of the Z axis.     
    
    return MaxTime
    
def getCurrentPosition():
    FullPositionStr = sendCommand('M114')
    OkStr = SerialObj.readline()
    if OkStr.decode() != 'ok\n':
        print('Didn\'t get ok from M114')
        return ErrorStr

    SplitStr = FullPositionStr.split('Z:')
    CurrentZ = float(SplitStr[-1]) # The current position is encoded in the last element of the split
    return CurrentZ


def getCurrentPosition2():
    FullPositionStr = sendCommand('M114')
    OkStr = SerialObj.readline()
    if OkStr.decode() != 'ok\n':
        print('Didn\'t get ok from M114')	
        return ErrorStr
    
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

def driveToPosition(Position):
    OkStr = sendCommand('G0 Z'+str(Position))
    if OkStr != 'ok\n':
      print('Didn\'t get ok from G0')

def driveToPosition2(X,Y,Z):
    OkStr = sendCommand('G0 '+ 'X'+str(X) + ' Y'+str(Y) + ' Z'+str(Z))
    if OkStr != 'ok\n':
        print('Didn\'t get ok from G0')

def robustGetCurrentPosition():
    MaxFailCount = 10
    FailCounter = 0
    
    while FailCounter <= MaxFailCount:
        CurrentPos = getCurrentPosition2()
        if not CurrentPos==ErrorStr:
            return CurrentPos
        else:
            print('Uff!')
            purgeSerial()
        
        FailCounter = FailCounter + 1
        print('FailCounter: ' + str(FailCounter))
    
    print("Something's wrong!")
    return ErrorStr
            
	
def driveUntilCondition(Sign=1):	
    global Condition 
    i = 0
    CurrentPos = robustGetCurrentPosition()
    CurrentZ = CurrentPos[2]
    CurrentTarget = CurrentZ + Sign*Increment # we are at some position and the next command will drive us one increment further
    driveToPosition(CurrentTarget)
    while(not Condition):
        i = i + 1
        CurrentPos = robustGetCurrentPosition()
        CurrentZ = CurrentPos[2]
        #print('CurrentZ: '+ str(CurrentZ))
        #print('Current Target: '+str(CurrentTarget))
        
        BeyondStop = False
        if DirectionSign == 1:
            BeyondStop = CurrentZ > Stop
        else:
            BeyondStop = CurrentZ < Stop                                        
                
        if abs(CurrentZ-CurrentTarget) < 0.9*abs(Increment):                    
            CurrentTarget = CurrentTarget + Sign*Increment # If we're within one Increment of reaching our target, dispatch the next one
            #print('Next Target: '+str(CurrentTarget))
            driveToPosition(CurrentTarget)		    
        		    
        Condition = False # reset
        FullPositionStr = sendCommand('M114')    
    
    OkStr = SerialObj.readline()
    return


            
def home():
    OkStr = sendCommand('G28')  
    Finished = False
    while Finished != True:
        Str = SerialObj.readline()
        if Str.decode() == 'ok\n':            
            Finished = True            
            sendCommand('G0 F' + str(FeedRateXY)) # Set the feedrate to the desired value
            print('Finished homing')
            break
