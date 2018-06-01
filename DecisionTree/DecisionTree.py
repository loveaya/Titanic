from functools import reduce
from math import log, inf

import pandas as pd


def getMinDic(dataSet, labelIndex):
    entrys = set(list(map(lambda x: x[labelIndex], dataSet)))
    result = {}.fromkeys(entrys)
    for entry in entrys:
        result[entry] = 1 if reduce(lambda x, y: x + y, list(map(lambda x: 1 if x[-1] else -1))) >= 0 else 0
    print("result :" + result)
    return result


def getDataEntrpy(dataSet):
    # print("dataSet length : " + str(len(dataSet)))
    numSurvived = reduce(lambda x, y: x + y, list(map(lambda x: x[-1], dataSet)))
    numVicitims = len(dataSet) - numSurvived
    propSurvived = numSurvived / float(len(dataSet))
    propVicitims = numVicitims / float(len(dataSet))
    # print((propVicitims, propSurvived))
    return 0 if abs(propVicitims - propSurvived) == 1 else (0 - propSurvived * log(propSurvived, 2) - propVicitims * log(propVicitims, 2))


def getIVEntrpy(dataSet, index):
    entrySet = set(filter(lambda x : x == x, map(lambda x: x[index], dataSet)))
    entropy = 0.0
    while len(entrySet) > 0:
        # print(len(entrySet))
        entry = entrySet.pop()
        partData = list(filter(lambda x: x[index] == entry, dataSet))
        prop = len(partData) / float(len(dataSet))
        # print(str(entry) + " : " + str(prop))
        entropy -= prop * log(prop, 2)
    return entropy

def chooseBestFeature(dataSet, labels, labelsFull):
    baseEntropy = getDataEntrpy(dataSet)
    infoGain = {}.fromkeys(labels)
    labelIV = {}.fromkeys(labels)
    labelIV.update()
    labelIV.update(map(lambda x : (x , getIVEntrpy(dataSet, labelsFull.index(x))), labels))
    for label in labels:
        labelIndex = labelsFull.index(label)
        entrySet = set(filter(lambda x : x == x , map(lambda x: x[labelIndex], dataSet)))
        afterEntropy = 0.0
        while len(entrySet) > 0:
            entry = entrySet.pop()
            partData = list(filter(lambda x : x[labelIndex] == entry, dataSet))
            prop = len(partData)/float(len(dataSet))
            afterEntropy = prop * getDataEntrpy(partData)
        infoGain[label] = baseEntropy - afterEntropy
    meanGain = sum(infoGain.values())/len(infoGain.values())
    maxGainRate = 0
    result = ""
    for key, value in infoGain.items():
        if value >= meanGain:
            if labelIV[key] == 0 :
                maxGainRate = inf
                result = key
            else:
                gainRate = value/labelIV[key]
                if gainRate > maxGainRate :
                    result = key
    return result

    # return list(labels)[0]


def createTree(dataSet, labels, labelsFull):
    # print(dataSet)
    print(labels)
    if 1 == len(labels):
        return getMinDic(dataSet, labelsFull.index(labels.pop()))

    else:
        label = chooseBestFeature(dataSet, labels, labelsFull)
        # print((label, labels))
        labels.remove(label)
        labelIndex = labelsFull.index(label)

        cols = len(dataSet)
        labelEntrys = []
        for ind in range(cols):
            labelEntrys.append(dataSet[ind][labelIndex])
        labelSet = set(list(filter(lambda x: x == x, labelEntrys)))

        # print(labelSet)
        result = {}
        result[label] = {}.fromkeys(labelSet)
        for entry in labelSet:
            # print("key = " + str(entry))
            partedData = list(filter(lambda x: x[labelIndex] == entry, dataSet))
            if (len(set(list(map(lambda x: x[-1], partedData)))) == 1):
                result[label][entry] = partedData[0][-1]
            else:
                result[label][entry] = createTree(partedData, labels.copy(), labelsFull)
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
    #船舱粗分级
    for ind in range(len(dataSet)):
        dataSet[ind][6] = dataSet[ind][6][0] if type(dataSet[ind][6]).__name__ == 'str' else dataSet[ind][6]
    labelsFull = labels[:-1]
    # print(labels_full.index(labels_full[0]))
    result = createTree(dataSet, set(labelsFull), labelsFull)
    print(result)
