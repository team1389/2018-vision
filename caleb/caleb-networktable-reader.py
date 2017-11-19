from networktables import NetworkTables
import time
NetworkTables.initialize('192.168.1.6')
sd = NetworkTables.getTable('MotionTracking')

while(True):
    print("offsetX: " + str(sd.getNumber('offsetX', 'N/A')))
    print("offsetY: " + str(sd.getNumber('offsetY', 'N/A')))
