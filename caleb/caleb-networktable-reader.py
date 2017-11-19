from networktables import NetworkTables
import time
NetworkTables.initialize('192.168.1.6')
sd = NetworkTables.getTable('MotionTracking')

offsetX = str(sd.getNumber('offsetX', 'N/A'))
offsetY = str(sd.getNumber('offsetY', 'N/A'))

while(True):
    newOffsetX = str(sd.getNumber('offsetX', 'N/A'))
    newOffsetY = str(sd.getNumber('offsetY', 'N/A'))
    if(offsetX != newOffsetX or offsetY != newOffsetY):
        print("offsetX: " + newOffsetX)
        print("offsetY: " + newOffsetY)
        offsetX = newOffsetX
        offsetY = newOffsetY
