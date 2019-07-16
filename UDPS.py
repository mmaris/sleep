from socket import *
import time
import threading

#*******
# main:

serverPort = 12001
serverSocket = socket(AF_INET, SOCK_DGRAM)
serverSocket.bind(('', serverPort))


with open("Received_Measurements.txt","w") as outfile:
    while 1:
        # await the next message
        try:
            message, clientAddress = serverSocket.recvfrom(serverPort)

            # handle empty message, usually a cause of dropping connection client side.
            if message == '':
                print('Empty message received. Closing socket.')
                break
            print("Received message with length: %i" % len(message))
            
            current = time.time()
            message = message.split()
            for m in message:
                prev = m.split(',')
                if len(prev) > 1:
                    previous = float(prev[1])
                    difference = current-previous
                    print('=%.9f\n'%difference)
                    outfile.write('%.9f %.9f'%(difference,current))

            # make this a thread
            # get interarrival time
            #currentTime = time.time()

            # start a thread to send the interarrival time
            #SendResponse(currentTime)

            #start thread to process stuff

        except Exception as e:
            print(str(e))
            break



serverSocket.close()
