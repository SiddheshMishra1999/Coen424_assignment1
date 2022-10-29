import json
import math
import os
from socket import *
from pathlib import Path


import pyinputplus as pyip

import protoFormat_pb2

def socketCreatingClient():
    headersize = 10
    # Create a Socket
    s = socket(AF_INET, SOCK_STREAM)

    # Defining the host to which I want to connect
    host = 'localhost'
    # Defining the port on which I want to connect
    port = 666

    # Connect tp the server on localhost
    s.connect((host, port))
    print(f'Connected to server on host: {host} and port {port}')
    # send data to server
    a, b, c, d, e, f, g, h, i = clientInput()
    if i == 1:
        data = makeJson(a, b, c, d, e, f, g, h)
        s.send(data.encode('latin-1'))
        print(f'Request {a} has been sent.')
    else:
        data = makeProto(a, b, c, d, e, f, g, h)
        s.send(data)
        print(f'Request {a} has been sent.')
    
    # receive files:
    msg = s.recv(1000000000)
    # print(msg.decode())
    if i == 1:
        jsonResponse(msg)
    else:
        protoResponse(msg)
    print(f'Response for {a} has been received') 

    print("Connection Broken")
    s.close()


def clientInput():
    # Getting all inputs from users
    RFWDID = pyip.inputStr("Please enter an ID for your request: \n")
    benchMarckTypeIn = pyip.inputNum("Please enter the Bench Mark type (enter 1 for DVD or 2 for NDBench): \n", min=1, lessThan=3)
    workLoadMetricIn = pyip.inputNum("Please enter the workload metric (enter 1 = CPU, 2 = NetworkIn, 3 = NetworkOut, 4 = Memory): \n",  min=1, lessThan=5)
    batchUnit = pyip.inputNum("Please enter the number of samples you wish to have in each batch: \n", min=1, lessThan= 10001)
    batchID = pyip.inputNum("Please enter an batch ID you wish to start sampling from: \n", min=1)
    batchSize = pyip.inputNum("Please enter the number of batches you wish to get: \n", min=1)
    dataTypeIn = pyip.inputNum("Please enter the type of data you wish to get(enter 1 for testing or 2 for training): \n", min=1, lessThan=3)
    dataAnalyticsIn = pyip.inputNum("Please enter what analysis you want done to your data (enter 1 = custom percentile, 2 = avg, 3 = std, 4 = min, 5 = max: \n", min=1, lessThan=6)
    if(dataAnalyticsIn == 1):
        dataAnalyticsP = pyip.inputNum("Please enter what percentile you wish to analyze (min = 1, max = 100): \n", min=1, max=100)
    else:
        dataAnalyticsP = 0

    # Asking user which type of request you 
    fileTypeIn = pyip.inputNum("Please enter the file type in which you wish to send and receive the data(enter 1 for JSON or 2 for Proto): \n", min=1, lessThan=3)
    
    benchMarckType = inputCheckBenchMark(math.floor(benchMarckTypeIn))
    workLoadMetric = inputCheckWorkLoad(math.floor(workLoadMetricIn))
    dataType = inputCheckDataType(math.floor(dataTypeIn))
    dataAnalytics = inputCheckDataAnalytics(dataAnalyticsIn, math.floor(dataAnalyticsP))

    fileType = inputCheckFileType(fileTypeIn)

    return str(RFWDID),benchMarckType, workLoadMetric, batchUnit, batchID, batchSize, dataType, dataAnalytics, math.floor(fileTypeIn)


def inputCheckBenchMark(benchMarckType):
    # matching the case for benchMarckType
    match benchMarckType:
        case 1:
            benchMarckType = "DVD"
        case _:
            benchMarckType = "NDBench"
    return benchMarckType

def inputCheckWorkLoad(workLoadMetric):
    # matching the case for workLoadMetric
    match workLoadMetric:
        case 1:
            workLoadMetric = "CPUUtilization_Average"
        case 2:
            workLoadMetric = "NetworkIn_Average"
        case 3:
            workLoadMetric = "NetworkOut_Average"
        case 4:
            workLoadMetric = "MemoryUtilization_Average"
        case _:
            workLoadMetric = "Final_Target"

    return workLoadMetric

def inputCheckDataType(dataType):
    # matching the case for dataType
    match dataType:
        case 1:
            dataType = "testing"
        case _:
            dataType = "training"
    return dataType

def inputCheckDataAnalytics(dataAnalyticsIn, dataAnalyticsP):
    # matching the case for dataAnalytics
    match dataAnalyticsIn:
        case 1:
            dataAnalytics = f"p{dataAnalyticsP}"
        case 2:
            dataAnalytics = "avg"
        case 3:
            dataAnalytics = "std"
        case 4:
            dataAnalytics = "min"
        case _:
            dataAnalytics = "max"

    return dataAnalytics

def inputCheckFileType(fileTypeIn):
    # matching the case for dataType
    match fileTypeIn:
        case 1:
            fileTypeIn = "JSON"
        case _:
            fileTypeIn = "binary"

    return fileTypeIn


def makeJson(RFWDID,benchMarckType, workLoadMetric, batchUnit, batchID, batchSize, dataType, dataAnalytics):
    requesJSON = {
        "RFWDID": RFWDID,
        "benchMarckType": benchMarckType,
        "workLoadMetric": workLoadMetric,
        "batchUnit": batchUnit,
        "batchID": batchID,
        "batchSize": batchSize,
        "dataType": dataType,
        "dataAnalytics": dataAnalytics
    }
    requestJSON = json.dumps(requesJSON)
    # with open("../GeneratedFiles/Client/requestJSON.json", "w") as outfile:
    #         json.dump(requesJSON, outfile, indent=4)
    # reqJson = json.dumps(reqDict)
    path = '../GeneratedFiles/Client/JSON/requestjson.json'
    obj = Path(path)
    # Check if the file exists and if it does, append the new reponse
    if(obj.exists()):
        # To append to the file
        with open(path, "ab+") as outfile:
            outfile.seek(-1, os.SEEK_END)
            outfile.truncate()
            outfile.write((',\n').encode())
            outfile.write(requestJSON.encode())
            outfile.write(']'.encode())
            
    else:
        with open(path, "wb+") as outfile:
            outfile.write('['.encode())
            outfile.write(requestJSON.encode())
            outfile.write(']'.encode())
    return requestJSON

def makeProto(RFWDID,benchMarckType, workLoadMetric, batchUnit, batchID, batchSize, dataType, dataAnalytics):
    toProto = protoFormat_pb2.requestForWorkload()
    toProto.RFWDID = RFWDID
    toProto.benchmarkType = benchMarckType
    toProto.workloadMetric = workLoadMetric
    toProto.batchUnit = batchUnit
    toProto.batchID = batchID
    toProto.batchSize = batchSize
    toProto.dataType = dataType
    toProto.dataAnalytics =dataAnalytics
    with open("../GeneratedFiles/Client/Proto/requestproto.txt", "w") as fd:
        fd.write(str(toProto))
    protodata = toProto.SerializeToString('latin-1')
    with open("../GeneratedFiles/Client/Proto/requestproto.bin", "wb") as f:
        f.write(protodata)
    return protodata



def jsonResponse(msg):
    data = msg.decode('latin-1')
    responseJson = json.dumps(data)

    path = '../GeneratedFiles/Client/JSON/responsejson.json'
    obj = Path(path)
    # Check if the file exists and if it does, append the new reponse
    if(obj.exists()):

        with open(path, "ab+") as outfile:
            outfile.seek(-1, os.SEEK_END)
            outfile.truncate()
            outfile.write((',\n').encode())
            outfile.write(responseJson.encode())
            outfile.write(']'.encode())            
    else:
        with open(path, "wb+") as outfile:
            outfile.write('['.encode())
            outfile.write(responseJson.encode())
            outfile.write(']'.encode())
    with open(path) as f:
        dataLoad = json.load(f)
    print(dataLoad)

def protoResponse(msg):
    getProto = protoFormat_pb2.responseForWorkload()
    response = getProto.FromString(msg)
    path = '../GeneratedFiles/Client/Proto/responseproto.txt'
    obj = Path(path)
    print(obj.exists())
    if(obj.exists()):
        with open(path, "a") as d:
            d.write(str(response))
        response = getProto.SerializeToString('latin-1')

        with open("../GeneratedFiles/Client/Proto/responseproto.bin", "ab") as fd:
            fd.write(response)
    
    else:
        with open(path, "w") as d:
            d.write(str(response))
        response = getProto.SerializeToString('latin-1')

        with open("../GeneratedFiles/Client/Proto/responseproto.bin", "wb") as fd:
            fd.write(response)

        # To Print the content of the binary file
    with open(path, 'r') as f:
        read_res  = f.read()
        f.close()
        print(read_res)


if __name__ == '__main__':
    socketCreatingClient()




