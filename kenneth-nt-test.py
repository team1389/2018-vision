#!/usr/bin/env python
from networktables import NetworkTables
import logging
logging.basicConfig(level=logging.DEBUG)
#NetworkTables.setIPAddress("10.13.89.99")
NetworkTables.initialize("10.13.89.99")
sd = NetworkTables.getTable('vision')
count=0
sd.putNumber('test', count)
sd.putNumber('test', count)
while(True):
    sd.putNumber('test', count)
    #print(sd.getNumber('test', 1))
    count=count+1
    #print('running')

