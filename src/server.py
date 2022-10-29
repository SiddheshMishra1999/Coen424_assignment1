
import math
import os
import socket
import numpy as np
import pandas as pd
import json
import protoFormat_pb2
from pathlib import Path


# creating a socket 
def serverSocketCreation():
    
    # declaring the host for the socket 
    host = ''
    # declaring the port for the socket 
    port = 666
    # Making a TCP connection
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
        dataFromClient = clientConnection.recv(1000000000)

        #getting the data type of the request
        dataType = checkDataType(dataFromClient) 

        # Parsing data and processing it based on the data type
        match dataType:
            case 1:
                idReq, benchmarkType, workloadMetric, batchUnit, batchID, batchSize, dataType, dataAnalytics = parseJsonDataFromClient(dataFromClient)
                idRes, lastBatchID, data, analytics = processData(idReq, benchmarkType, workloadMetric, batchUnit, batchID, batchSize, dataType, dataAnalytics)
                response = makeJSON(idRes, lastBatchID, data, analytics)
                print(f'Request for {idReq} has been received')
                #make parser, process data, send it
                
            case _:
            # Decoding data from client
                idReq, benchmarkType, workloadMetric, batchUnit, batchID, batchSize, dataType, dataAnalytics= parseProtoDataFromClient(dataFromClient)
                idRes, lastBatchID, data, analytics = processData(idReq, benchmarkType, workloadMetric, batchUnit, batchID, batchSize, dataType, dataAnalytics)
                print(f'Request for {idReq} has been received')

                response = makeProto(idRes, lastBatchID, data, analytics)

        clientConnection.send(response)   
        print(f'Response for {idReq} has been sent') 
        print(f'Closing connection with client adress {address}')
        clientConnection.close()
        print('Socket is listening')

# check if the data being recieved is json or not
def checkDataType(dataFromClient):
    data = dataFromClient.decode('latin-1')
    parseData = data.split(' ')[0]
    if(parseData == '{"RFWDID":'):
        return 1
    else: 
        return 2
    


# Parse the Json data coming from client
def parseJsonDataFromClient(clientReq):
    decodedData = clientReq.decode('latin-1')
    reqDict = json.loads(decodedData)
    idReq = reqDict['RFWDID']
    benchmarkType = reqDict['benchMarckType']
    workloadMetric = reqDict['workLoadMetric']
    batchUnit = reqDict['batchUnit']
    batchID = reqDict['batchID']
    batchSize = reqDict['batchSize']
    dataType = reqDict['dataType']
    dataAnalytics = reqDict['dataAnalytics']



    reqJson = json.dumps(reqDict)
    path = '../GeneratedFiles/Server/JSON/requestjson.json'
    obj = Path(path)
    # Check if the file exists and if it does, append the new reponse
    if(obj.exists()):

        with open(path, "ab+") as outfile:
            outfile.seek(-1, os.SEEK_END)
            outfile.truncate()
            outfile.write((',\n').encode())
            outfile.write(reqJson.encode())
            outfile.write(']'.encode())
            
    else:
        with open(path, "wb+") as outfile:
            outfile.write('['.encode())
            outfile.write(reqJson.encode())
            outfile.write(']'.encode())


    
    
    return idReq, benchmarkType, workloadMetric, batchUnit, batchID, batchSize, dataType, dataAnalytics


# Parse the proto data coming from client
def parseProtoDataFromClient(clientReq):
    data = protoFormat_pb2.requestForWorkload()
    readData = data.FromString(clientReq)
    idReq = readData.RFWDID
    benchmarkType = readData.benchmarkType
    workloadMetric = readData.workloadMetric
    batchUnit = readData.batchUnit
    batchID = readData.batchID
    batchSize = readData.batchSize
    dataType = readData.dataType
    dataAnalytics = readData.dataAnalytics
    with open("../GeneratedFiles/Server/Proto/requestproto.txt", "w") as fd:
        fd.write(str(readData))
    dataP = data.SerializeToString('latin-1')
    with open("../GeneratedFiles/Server/Proto/requestproto.bin", "wb") as f:
        f.write(dataP)

    return idReq, benchmarkType, workloadMetric, batchUnit, batchID, batchSize, dataType, dataAnalytics



def processData(idReq, benchmarkType, workloadMetric, batchUnit, batchID, batchSize, dataType, dataAnalytics):
     

    print(idReq, benchmarkType, workloadMetric, batchUnit, batchID, batchSize, dataType, dataAnalytics)

    # Get right file -->  benchmarkType + dataType
    path = f'{benchmarkType}-{dataType}.csv'
    # DataUrl = 'https://raw.githubusercontent.com/haniehalipour/Online-Machine-Learning-for-Cloud-Resource-Provisioning-of-Microservice-Backend-Systems/master/Workload%20Data'
    filePath = f"../CSV_Data/{path}"
    # Get the path to the requested file
    reqFile = pd.read_csv(filePath)
    
    # Get the right column --> workloadMetric
    pos = rightWorkloadMetric(workloadMetric)
    # Get column name 
    colName = reqFile.columns[pos]

    # Getting all the batch data
    firstData, lastData, lastBatchID = batches(batchUnit, batchID, batchSize)
    print(f'BatchUnit = {batchUnit} \n batchID = {batchID} \n batchSize = {batchSize}\n')
    print(f'First Data Point at index: {firstData}\nLast data Point= {lastData}\nTotal Data printed = {batchUnit * batchSize}\nLast Batch ID = {lastBatchID}')
    # Getting the correct data 
    data = reqFile.loc[firstData:lastData, colName].to_list()

    #Getting the Analytics from an analytics file
    analytics = dataAnalyticsCal(dataAnalytics, data)


    return idReq, lastBatchID, data, analytics

def batches(batchUnit, batchID, batchSize):

    # Total number of data points being sent
    totalData = batchUnit * batchSize
    # index of first data from the requested batch
    dataStart = (batchUnit *(batchID-1))
    # last index of the requested batches
    dataEnd = totalData + dataStart - 1
    # Id of the final Batch sent   
    lastBatchID = (batchSize + (batchID -1))
    return dataStart, dataEnd, lastBatchID
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
                intPercentileValue = int(p)
                return np.percentile(sortedArr, intPercentileValue)




def makeJSON(idRes, lastBatchID, data, analytics):

    # Make a disctionary to store the data that will be sent
    responseDict = {
        "RFWDID": idRes,
        "LastBatchID": lastBatchID,
        "dataRequested": data,
        "dataAnalytics": analytics
    }
    responseJson = json.dumps(responseDict)
    path = '../GeneratedFiles/Server/JSON/responsejson.json'
    obj = Path(path)
    # Check if the file exists and if it does, append the new reponse
    if(obj.exists()):
        # To append to the file

        with open(path, "ab+") as outfile:
            outfile.seek(-1, os.SEEK_END)
            outfile.truncate()
            outfile.write((',\n').encode())
            outfile.write(responseJson.encode())
            outfile.write(']'.encode())
            

        encodedRes = responseJson.encode('latin-1')
    else:
        with open(path, "wb+") as outfile:
            outfile.write('['.encode())
            outfile.write(responseJson.encode())
            outfile.write(']'.encode())
        encodedRes = responseJson.encode('latin-1')
    return encodedRes


def makeProto(idRes, lastBatchID, data, analytics):
    

    protoBuf = protoFormat_pb2.responseForWorkload()

    protoBuf.RFWDID = idRes
    protoBuf.LastBatchID = lastBatchID
    protoBuf.dataRequested.extend(data)
    protoBuf.dataAnalytics = analytics

    
    path = '../GeneratedFiles/Server/Proto/responseproto.txt'
    obj = Path(path)
    print(obj.exists())
    if(obj.exists()):
        with open(path, "a") as d:
            d.write(str(protoBuf))
        response = protoBuf.SerializeToString('latin-1')

        with open("../GeneratedFiles/Server/Proto/responseproto.bin", "wb") as fd:
            fd.write(response)
    
    else:
        with open(path, "w") as d:
            d.write(str(protoBuf))
        response = protoBuf.SerializeToString('latin-1')
        with open("../GeneratedFiles/Server/Proto/responseproto.bin", "wb") as fd:
            fd.write(response)

    return response




if __name__ == '__main__':
    serverSocketCreation()


  

