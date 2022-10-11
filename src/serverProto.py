import math
from telnetlib import OUTMRK
import numpy as np
from optparse import Values
import statistics
import pandas as pd
import json
import protoFormat_pb2 as proto
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
                return std, statistics.stdev(arr), np.std(arr)
            case 'min':
                return min(arr)
            case 'max':
                return max(arr)
            case _:
                sortedArr = sorted(arr)
                percentileValue, p = name.split("p", 1)
                intPercentileValue = int(percentileValue)
                # print(intPercentileValue)
                # i, j = 0,0
                # count, percent = 0,0
                # while(i<intPercentileValue):
                #     count = 0
                #     j = 0
                #     while(j < intPercentileValue):
                #         if (sortedArr[i] > sortedArr[j]):
                #             count+=1
                #         j+= 1
                #     percent = (count * 100) // (n-1)
                #     i+=1
                return np.percentile(sortedArr, intPercentileValue)



def processDataProto(RFWDID = 1,
benchmarkType = 'NDBench',
workloadMetric = 'MemoryUtilization_Average',
batchUnit = 10,
batchID = 1,
batchSize = 3,
dataType = 'training',
dataAnalytics = '90p'):

    # Get right file -->  benchmarkType + dataType
    path = f'{benchmarkType}-{dataType}.csv'
    DataUrl = 'https://raw.githubusercontent.com/haniehalipour/Online-Machine-Learning-for-Cloud-Resource-Provisioning-of-Microservice-Backend-Systems/master/Workload%20Data'

    # Get the path to the requested file
    reqFile = pd.read_csv(f'{DataUrl}/{path}')
    
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

    data = reqFile.loc[firstData:lastData, colName].to_list()
    # dataArr = [0.00]*totalData
    # for i in data:
    #     dataArr.append(data[i])
    

    # print(data)
    # print(sorted(data))
    # print(dataArr)
    analytics = dataAnalyticsCal(dataAnalytics, data)

    # Write in JSON file

    responseJSON = {
        "RFWDID": '123',
        "LastBatchID": lastBatchID,
        "dataRequested": data,
        "dataAnalytics": analytics

    }
    with open("responseJSON.json", "w") as outfile:
        json.dump(responseJSON, outfile)
    
    # d1 = proto._descriptor_pool
    # d2 = d1.DescriptorPool()
    # d2.setRFWID("123")
    
    # print(d1)
   




    # Length of the file -> len()



processDataProto()

