import json
from pydoc import cli
from socket import *
from sys import flags


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

    # Connect tp th e server on localhost
    s.connect((host, port))

    # send data to server
    a, b, c, d, e, f, g, h, i = clientInput()


    if i == 1:
        data = makeJson(a, b, c, d, e, f, g, h)
        s.send(data.encode('utf-8'))
    else:
        data = makeProto(a, b, c, d, e, f, g, h)
        s.send(data)
    
    # receive files:
    msg = s.recv(1000000)
    getResponseFromServer(msg)


    print("Connection Broken")
    s.close()


def getResponseFromServer(msg):
    getProto = protoFormat_pb2.responseForWorkload()
    response = getProto.FromString(msg)
    binaryRes= response.SerializeToString()
    stringRes = getProto.FromString(msg)
    # print(f'Response = {binaryRes} \n type of response = {type(binaryRes)}')
    with open("../GeneratedFiles/responseproto.bin", "wb") as fd:
        fd.write(binaryRes)


def clientInput():
    # Getting all inputs from users
    RFWDID = pyip.inputStr("Please enter an ID for your request: \n")
    benchMarckTypeIn = pyip.inputNum("Please enter the Bench Mark type (enter 1 for DVD or 2 for NDBench): \n", min=1, lessThan=3)
    workLoadMetricIn = pyip.inputNum("Please enter the workload metric (enter 1 = CPU, 2 = NetworkIn, 3 = NetworkOut, 4 = Memory, 5 = Final_Target ): \n",  min=1, lessThan=6)
    batchUnit = pyip.inputNum("Please enter the number of samples you wish to have in each batch: \n", min=1, lessThan= 10001)
    batchID = pyip.inputNum("Please enter an batch ID you wish to start sampling from: \n", min=1)
    batchSize = pyip.inputNum("Please enter the number of batches you wish to get: \n", min=1)
    dataTypeIn = pyip.inputNum("Please enter the type of data you wish to get(enter 1 for testing or 2 for training): \n", min=1, lessThan=3)
    dataAnalyticsIn = pyip.inputNum("Please enter what analysis you want done to your data (enter 1 = custom percentile, 2 = avg, 3 = std, 4 = min, 5 = max: \n", min=1, lessThan=6)
    if(dataAnalyticsIn == 1):
        dataAnalyticsP = pyip.inputNum("Please enter what percentile you wish to analyze (min = 1, max = 100): \n", min=1, max=100)
    else:
        dataAnalyticsP = 0

    fileTypeIn = pyip.inputNum("Please enter the file type in which you wish to sned and receive the data(enter 1 for JSON or 2 for Binary): \n", min=1, lessThan=3)
 
    benchMarckType = inputCheckBenchMark(benchMarckTypeIn)
    workLoadMetric = inputCheckWorkLoad(workLoadMetricIn)
    dataType = inputCheckDataType(dataTypeIn)
    dataAnalytics = inputCheckDataAnalytics(dataAnalyticsIn, dataAnalyticsP)

    fileType = inputCheckFileType(fileTypeIn)

    return str(RFWDID),benchMarckType, workLoadMetric, batchUnit, batchID, batchSize, dataType, dataAnalytics, fileTypeIn


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

    protodata = toProto.SerializeToString()
    return protodata
    # print(RFWDID,benchMarckType, workLoadMetric, batchUnit, batchID, batchSize, dataType, dataAnalytics )







if __name__ == '__main__':
    # chatlog = textBox = None
    socketCreatingClient()

    # To Print the content of the binary file
    # with open("../GeneratedFiles/responseproto.bin", 'rb') as f:
    #     read_res = protoFormat_pb2.responseForWorkload()
    #     read_res.ParseFromString(f.read())
    # print(read_res)


