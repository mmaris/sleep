from socket import *
import threading
import time
from random import *
from math import floor


global currentCycle
global bw
#set cycle structure
availableBandwidth = 10   # worst bandwidth in Mb/s
cycles = [0.1 ,0.5, 0.15, 0.1, 0.12] # percentage factors from bandwidth to be sent
size = 1024
bw = 0
currentCycle = 0
timeout = 0
cycleTime = 10
seed(1)

# Change cycle function: go to the next cycle if not cycle 0(sleep), add noise within range
def ChangeCycle():
    global currentCycle
    global bw
    #increment cycle
    currentCycle = (currentCycle+1)%len(cycles) 

    #change bw and add noise
    bw = cycles[currentCycle]*(1-uniform(-5,5)/100)

    #optionally update the cycles with new bw.
    #cycles[currentCycle] = bw

def SendData(data, addr):
    clientSocket.sendto(data, addr)

#********
# main:
        
#generate data string
a = []
for i in range(size): a += str(randint(0,9))
sample = ''.join(a)

serverName = '10.0.0.2'
serverPort = 12001
clientSocket = socket(AF_INET, SOCK_DGRAM)

while 1:
    if time.time() >= timeout:
        ChangeCycle()
        #calculate new timeout
        if(bw!=0):
            print("sending in %f intervals"%(size/(bw/8*10**6)))
        timeout = time.time()+cycleTime
    
    if bw!= 0:
        #send data
        SendData((sample[:size-28]+',%.9f '%time.time()), (serverName,serverPort))

        #sleep
        time.sleep(size/(bw/8*10**6))

clientSocket.close()
