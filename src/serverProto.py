import pandas as pd
import json
import protoFormat_pb2 as proto
from protobuf_to_dict import protobuf_to_dict
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


def processDataProto(RFWDID = 1,
benchmarkType = 'NDBench',
workloadMetric = 'MemoryUtilization_Average',
batchUnit = 3,
batchID = 1,
batchSize = 6,
dataType = 'training',
dataAnalytics = 'avg'):

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
    realBatchID = batchID - 1

    # index of first data from the requested batch
    firstData = (realBatchID * batchUnit)

    # Total number of data points being sent
    totalData = batchSize * batchUnit
    # last index of the requested batches
    lastData = firstData + totalData

    # Total number of batches sent 
    batchesSent = batchSize - realBatchID

    # Id of the final Batch sent
    lastBatchID = realBatchID + batchSize

    data = reqFile.iloc[firstData:lastData, pos].to_list()
    print(data)


    responseJSON = {
        "RFWDID": id,
        "LastBatchID": lastBatchID,
        "dataRequested": data,
        "dataAnalytics": 50.5

    }
    d1 = proto._descriptor_pool
    d2 = d1.DescriptorPool()
    d2.setRFWID("123")
    
    print(d1)
   




    # Length of the file -> len()



processDataProto()

