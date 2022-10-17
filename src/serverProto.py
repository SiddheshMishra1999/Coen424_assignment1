
from calendar import day_abbr
from cmath import log
import math
import sys
import socket 
from traceback import print_tb
import numpy as np
import statistics
import pandas as pd
import json
import protoFormat_pb2

from tkinter import *
import _thread
'''
RFWDID = 1,
benchmarkType = 'DVD',
workloadMetric = 'CPU'
batchUnit = 1000,
batchID = 1,
batchSize = 6,
dataType = 'training',
dataAnalytics = 'avg'

1. get the right file
2. which data 
3. batch: Send data from batch ID to batchsize -1
'''

def rightWorkloadMetric(name):
        match name:
            case 'CPUUtilization_Average':
                pos = 0
            case 'NetworkIn_Average':
                pos = 1
            case 'NetworkOut_Average':
                pos = 2
            case 'MemoryUtilization_Average':
                pos = 3
            case 'Final_Target':
                pos = 4
            case _:
                print('Invalid Column name')
        return pos

def avgCal(arr):
    sum = 0.0
    for i in range(len(arr)):
        val = arr[i]
        sum += val
    avg = sum/len(arr)
    return avg

def dataAnalyticsCal(name, arr):
    
    match name:
            case 'avg':
                return avgCal(arr)
            case 'std':
                mean = avgCal(arr)
                sum = 0.0
                for i in range(len(arr)):
                    variance = (arr[i] - mean)
                    varianceSquare = variance * variance
                    sum += varianceSquare
                finalVariance = (sum/(len(arr)-1))
                std = math.sqrt(finalVariance)
                return np.std(arr)
            case 'min':
                return min(arr)
            case 'max':
                return max(arr)
            case _:
                sortedArr = sorted(arr)
                percentileValue, p = name.split("p", 1)
                intPercentileValue = int(percentileValue)
                return np.percentile(sortedArr, intPercentileValue)

def parseProtoDataFromClient(clientReq):
    data = protoFormat_pb2.requestForWorkload()
    readData = data.FromString(clientReq)
    print(f"readData {readData}")
    idReq = readData.RFWDID
    benchmarkType = readData.benchmarkType
    workloadMetric = readData.workloadMetric
    batchUnit = readData.batchUnit
    batchID = readData.batchID
    batchSize = readData.batchSize
    dataType = readData.dataType
    dataAnalytics = readData.dataAnalytics

    return idReq, benchmarkType, workloadMetric, batchUnit, batchID, batchSize, dataType, dataAnalytics



def processData(idReq, benchmarkType, workloadMetric, batchUnit, batchID, batchSize, dataType, dataAnalytics):
     

    print(idReq, benchmarkType, workloadMetric, batchUnit, batchID, batchSize, dataType, dataAnalytics)

    # Get right file -->  benchmarkType + dataType
    path = f'{benchmarkType}-{dataType}.csv'
    # DataUrl = 'https://raw.githubusercontent.com/haniehalipour/Online-Machine-Learning-for-Cloud-Resource-Provisioning-of-Microservice-Backend-Systems/master/Workload%20Data'
    filePath = f"C:/Users/Siddh/Documents/Documents/Concordia/10th Semester Fall 2022/Coen 424/Coen424_assignment1/CSV_Data/{path}"
    # Get the path to the requested file
    reqFile = pd.read_csv(filePath)
    
    # Get the right column --> workloadMetric
    pos = rightWorkloadMetric(workloadMetric)
    # Get column name 
    colName = reqFile.columns[pos]

    # Selecting the batches to send data from using correct index
    realBatchID = batchID -1

    # index of first data from the requested batch
    firstData = (realBatchID * batchUnit)

    # Total number of data points being sent
    totalData = batchSize * batchUnit

    # last index of the requested batches
    lastData = totalData - 1

    # Total number of batches sent 
    batchesSent = batchSize - realBatchID

    # Id of the final Batch sent
    lastBatchID = realBatchID + batchSize

    # Getting the correct data 
    data = reqFile.loc[firstData:lastData, colName].to_list()

    #Getting the Analytics from an analytics file
    analytics = dataAnalyticsCal(dataAnalytics, data)

    return idReq, lastBatchID, data, analytics

def makeJSON(idReq, lastBatchID, data, analytics):

    # Make a disctionary to store the data that will be sent
    responseJSON = {
        "RFWDID": idReq,
        "LastBatchID": lastBatchID,
        "dataRequested": data,
        "dataAnalytics": analytics

    }

    # with open("../GeneratedFiles/responseJSON.json", "w") as outfile:
    #     json.dump(responseJSON, outfile, indent=4, sort_keys=True)
    



def makeProto(idReq, lastBatchID, data, analytics):
    

    protoBuf = protoFormat_pb2.responseForWorkload()

    protoBuf.RFWDID = idReq
    protoBuf.LastBatchID = lastBatchID
    protoBuf.dataRequested.extend(data)
    protoBuf.dataAnalytics = analytics
    response = protoBuf.SerializeToString()
    return response

    # print(f"binary: {}")
    
    # with open("../GeneratedFiles/responseproto", "wb") as fd:
    #     fd.write(protoBuf.SerializeToString())

    # print(protoBuf.RFWDID)
    # print(protoBuf.LastBatchID)
    # print(protoBuf.dataRequested)
    # print(protoBuf.dataAnalytics)

    # parse from string, deserialize 








# declaring the host for the socket 
host = ''
# declaring the port for the socket 
port = 666

# creating a socket 
def socketCreation():
    headersize = 10
    # Making a TXP connection
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print(f"Socket Successfuly created!")

                # bind the socket to the port 
    s.bind((host, port))
    print(f"Socket successfully connected to port {port}")

        # Making the socket listen 
    s.listen()
    print('Socket is listening ')

    while True:
        # Connecting to client
        clientConnection, address = s.accept()
        print(f'Connection received from {address}')
        
        # Receiving data from client
        dataFromClient = clientConnection.recv(1000000)

        dataType = checkDataType(dataFromClient) 

        match dataType:
            case 1:
                decodedData = dataFromClient.decode('utf-8')
                #make parser, process data, send it
                
            case _:
            # Decoding data from client
                a, b, c, d, e, f, g, h = parseProtoDataFromClient(dataFromClient)
                i, j, k, l = processData(a, b, c, d, e, f, g, h)

                response = makeProto(i, j, k, l)
                clientConnection.send(response)    
        clientConnection.close()
        sys.exit()

# check if the data being recieved is json or not
def checkDataType(dataFromClient):
    data = dataFromClient.decode()
    parseData = data.split(' ')[0]
    if(parseData == '{"RFWDID":'):
        return 1
    else: 
        return 2
    




# def socketCreatingServer():
#     # Create a Socket
#     s = socket(AF_INET, SOCK_STREAM)

#     # Defining the host to which I want to connect
#     host = 'localhost'
#     # Defining the port on which I want to connect
#     port = 667

#     # Connect tp th e server on localhost
#     s.bind((host, port))
#     s.listen(1)
#     connection, address = s.accept()

#     return connection

# # to receive message
# def receive():
#     while 1:
#         try:
#             data = connection.recv(1024)
#             msg = data.decode('ascii')
#             if msg!= '':
#                 update_chat(msg, 1)
#         except: 
#             pass



# def update_chat(msg, state):
#     global chatlog

#     chatlog.config(state =NORMAL)
#     # Update the message in chat window
#     if state == 0:
#         chatlog.insert(END, f'Server: {msg}')
#     else:
#         chatlog.insert(END, f'Client: {msg}')
#     chatlog.config(state = DISABLED)
#     # Show the lattest meesages
#     chatlog.yview(END)

# # send command to a client 
# def sendCommand():
#     global chatlog
#     global textBox
#     # Get the message
#     msg = textBox.get('0.0', END)

#     #update the log
#     update_chat(msg, 0)

#     #send message
#     connection.send(msg.encode('ascii'))

#     textBox.delete('0.0', END)
#     # while True:
#     #     # take input from us
#     #     cmd = input()

#     #     if(cmd == 'quit'):
#     #         connection.close()
#     #         socket.close()
#     #         sys.exit()
#     #     #length of the encded string sent to another computer
#     #     if(len(str.encode(cmd)) > 0):
#     #         # send data to another computer 
#     #         connection.send(str.encode(cmd))
#     #         # Converting the response from byte to string
#     #         clientResponse = str(connection.recv(1024), 'ascii')
#     #         # after printning, and go to a new line
#     #         print(clientResponse, end="")





# def GUI():
#     global chatlog
#     global textBox
#     # Initialize tkinter object 
#     gui = Tk()
#     # Set title for the window
#     gui.title('Server Request and response for workload')
#     # Set size of window
#     gui.geometry("500x500")

#     # text space to display messages
#     chatlog = Text(gui, bg='white')
#     chatlog.config(state=DISABLED)

#     # Button to send messages 
#     sendButton = Button(gui, bg ='orange', fg = 'black', text = 'SEND', command=sendCommand)

#     # textbox to type messages
#     textBox = Text(gui, bg ='white')

#     # Place the components in the window

#     chatlog.place(x = 40, y=6, width = 400, height =400 )
#     textBox.place(x=40, y = 470 , width = 360, height =20)
#     sendButton.place(x = 401, y = 470 , width = 50, height =20)



#     # # # Create thread to capture messages continuously 
#     # _thread.start_new_thread(receive(),())
#         # to keep window open
#     gui.mainloop()


# processDataProto()










if __name__ == '__main__':
    # chatbox = textBox = None
    socketCreation()
    # processDataProto()
    # GUI()

  

