from functools import reduce
from math import log

import pandas as pd


def getMinDic(dataSet, labelIndex):
    entrys = set(list(map(lambda x: x[labelIndex], dataSet)))
    result = {}.fromkeys(entrys)
    for entry in entrys:
        result[entry] = 1 if reduce(lambda x, y : x + y, list(map(lambda x: 1 if x[-1] else -1))) >= 0 else 0
    return result


def getDataEntrpy(dataSet, index):
    numSurvived = reduce(lambda x, y: x + y, list(map(lambda x: x[index], dataSet)))
    numVicitims = len(dataSet) - numSurvived
    propSurvived = numSurvived / float(len(dataSet))
    propVicitims = numVicitims / float(len(dataSet))
    print((propVicitims, propSurvived))
    if abs(propSurvived - propVicitims) == 1 :
        return 0
    else :
        return(0 - propSurvived * log(propSurvived, 2) - propVicitims * log(propVicitims, 2))


def chooseBestFeature(dataSet, labels, labelsFull):
    baseEntropy = getDataEntrpy(dataSet, -1)
    afterEntropys = {}.fromkeys(labels)
    for label in labels:
        labelIndex = labelsFull.index(label)
        entrySet = set(map(lambda x : x[labelIndex], dataSet))


    return list(labels)[0]


def createTree(dataSet, labels, labelsFull):
    print(dataSet)
    print(labels)
    if 1 == len(labels):
        return getMinDic(dataSet, labelsFull.index(labels.pop()))

    else:
        label = chooseBestFeature(dataSet, labels, labelsFull)
        labels.remove(label)
        labelIndex = labelsFull.index(label)

        cols  = len(dataSet)
        labelEntrys = []
        for ind in range(cols):
            labelEntrys.append(dataSet[ind][labelIndex])
        labelSet = set(list(filter(lambda x : x == x, labelEntrys)))

        print(labelSet)
        result = {}.fromkeys(labelSet)
        for entry in labelSet:
            print("key = " + str(entry))
            partedData = list(filter(lambda x: x[labelIndex] ==  entry, dataSet))
            if (len(set(list(map(lambda x : x[-1], partedData)))) == 1) :
                result[entry] = partedData[0][-1]
            else :
                result[entry] = createTree(partedData, labels.copy(), labelsFull)
        return result




if __name__ == '__main__':
    dataPath = "../SourceData/train.csv"
    data = pd.read_csv(dataPath)
    data = data.drop(["PassengerId", "Name", 'Ticket'], axis=1)
    # 对原始数据重排序
    labelsEx = data.columns.values.tolist()
    labels = labelsEx[1:] + labelsEx[0:1]
    data = data[labels]
    dataSet = data.values.tolist()
    # dataSet = data.values.tolist()
    labelsFull = labels[:-1]
    # print(labels_full.index(labels_full[0]))
    print(set(labelsFull))
    result = createTree(dataSet, set(labelsFull), labelsFull)
    print(result)


