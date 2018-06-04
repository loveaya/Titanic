from functools import reduce
from math import log, inf
from random import choice

import pandas as pd


def getMinDic(dataSet, labelIndex, labelsFull):
    entrys = set(list(map(lambda x: x[labelIndex], dataSet)))
    if len(entrys) > 1:
        result = {labelsFull[labelIndex]: {}.fromkeys(entrys)}
        for entry in entrys:
            result[labelsFull[labelIndex]][entry] = 1 if reduce(lambda x, y: x + y, list(
                map(lambda x: 1 if x[-1] else -1, dataSet))) >= 0 else 0
        return result
    else:
        return 1 if reduce(lambda x, y: x + y, list(map(lambda x: 1 if x[-1] else -1, dataSet))) >= 0 else 0


def getDataEntrpy(dataSet):
    # print("dataSet length : " + str(len(dataSet)))
    numSurvived = reduce(lambda x, y: x + y, list(map(lambda x: x[-1], dataSet)))
    numVicitims = len(dataSet) - numSurvived
    propSurvived = numSurvived / float(len(dataSet))
    propVicitims = numVicitims / float(len(dataSet))
    # print((propVicitims, propSurvived))
    return 0 if abs(propVicitims - propSurvived) == 1 else (
            0 - propSurvived * log(propSurvived, 2) - propVicitims * log(propVicitims, 2))


def getIVEntrpy(dataSet, index):
    entrySet = set(filter(lambda x: x == x, map(lambda x: x[index], dataSet)))
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
    labelIV.update(map(lambda x: (x, getIVEntrpy(dataSet, labelsFull.index(x))), labels))
    for label in labels:
        labelIndex = labelsFull.index(label)
        entrySet = set(filter(lambda x: x == x, map(lambda x: x[labelIndex], dataSet)))
        afterEntropy = 0.0
        while len(entrySet) > 0:
            entry = entrySet.pop()
            partData = list(filter(lambda x: x[labelIndex] == entry, dataSet))
            prop = len(partData) / float(len(dataSet))
            afterEntropy += prop * getDataEntrpy(partData)
        infoGain[label] = baseEntropy - afterEntropy
    meanGain = sum(infoGain.values()) / len(infoGain)
    print((infoGain.keys(), meanGain))
    maxGainRate = 0
    result = list(labels)[0]
    for key, value in infoGain.items():
        if value >= meanGain:
            if labelIV[key] == 0:
                maxGainRate = inf
                result = key
            else:
                gainRate = value / labelIV[key]
                if gainRate > maxGainRate:
                    result = key
    return result

    # return list(labels)[0]


def createTree(dataSet, labels, labelsFull):
    labelSet = set()
    while len(labelSet) <= 1:
        if 1 == len(labels):
            return getMinDic(dataSet, labelsFull.index(labels[0]), labelsFull)
        label = chooseBestFeature(dataSet, labels, labelsFull)
        # print((label, labels))
        labels.remove(label)
        labelIndex = labelsFull.index(label)

        cols = len(dataSet)
        labelEntrys = []
        for ind in range(cols):
            labelEntrys.append(dataSet[ind][labelIndex])
        labelSet = set(filter(lambda x: x == x, labelEntrys))
    result = {label: {}.fromkeys(labelSet)}
    for entry in labelSet:
        # print("key = " + str(entry))
        partedData = list(filter(lambda x: x[labelIndex] == entry, dataSet))
        resultSet = set(map(lambda x: x[-1], partedData))
        print(resultSet)
        if len(resultSet) == 1:
            result[label][entry] = partedData[0][-1]
        else:
            result[label][entry] = createTree(partedData, labels[:], labelsFull)
    return result


def dataDiscrete(dataSet, index):
    labelSet = set(map(lambda x: x[index], dataSet))
    dataSetUnkown = list(filter(lambda x: x[index] == 'Unknown', dataSet))
    dataSet = list(filter(lambda x: x[index] != 'Unknown', dataSet))
    dataSet = sorted(dataSet, key=lambda x: x[index])
    result = dataSet[:]
    if len(labelSet) >= 8:
        print("label index : " + str(index))
        currentResult = dataSet[0][-1]
        minEntropy = inf
        for ind in range(1, len(dataSet)):
            if dataSet[ind][-1] != currentResult and dataSet[ind][index] != dataSet[ind - 1][index]:
                currentResult = dataSet[ind][-1]
                key = str(dataSet[ind][index])
                lessList = list(map(lambda x: x[:index] + ["<" + key] + x[index + 1:], dataSet[:ind]))
                greatList = list(map(lambda x: x[:index] + [">=" + key] + x[index + 1:], dataSet[ind:]))
                propLess = len(lessList) / float(len(dataSet))
                propGreat = 1 - propLess
                totalEntropy = propLess * getDataEntrpy(lessList) + propGreat * getDataEntrpy(greatList)
                if totalEntropy < minEntropy:
                    minEntropy = totalEntropy
                    result = lessList + greatList
    return result + dataSetUnkown


def parseData(line):
    line[4] = 'Unknown' if line[4] != line[4] else ('<9.0' if line[4] < 9.0 else '>=9.0')
    line[8] = '<11.1333' if line[8] < 11.1333 else '>=11.1333'
    line[9] = 'Empty' if line[9] != line[9] else line[9][0]
    return line


def getResult(itemMap, tree):
    if type(tree).__name__ == 'dict':
        key1 = list(tree.keys())[0]
        key2 = itemMap[key1]
        print(key1, key2)
        if key2 in tree[key1]:
            return getResult(itemMap, tree[key1][key2])
        else:
            return getResult(itemMap, tree[key1][choice(list(tree[key1].keys()))])
    else:
        print("return :: " + str(tree))
        return tree


def getResultFromTree(testDataSet, resultTree, labels):
    resultList = list()
    for item in testDataSet:
        itemMap = dict(zip(labels, item))
        print(itemMap)
        resultList.append(getResult(itemMap, resultTree.copy()))
    return resultList


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
    # 船舱粗分级,用平均年龄补全缺失年龄，并对连续数据离散化
    noAgeEmpty = list(map(lambda x: x[2], (filter(lambda x: x[2] == x[2], dataSet))))
    # meanAge = round(reduce(lambda x, y: x + y, noAgeEmpty)/reduce(lambda x , y: x + 1, noAgeEmpty))
    for ind in range(len(dataSet)):
        dataSet[ind][6] = dataSet[ind][6][0] if type(dataSet[ind][6]).__name__ == 'str' else "Empty"
        dataSet[ind][2] = "Unknown" if dataSet[ind][2] != dataSet[ind][2] else dataSet[ind][2]
    for ind2 in range(len(dataSet[0])):
        if type(dataSet[ind][ind2]).__name__ == 'int' \
                or type(dataSet[ind][ind2]).__name__ == 'float' \
                or dataSet[ind][ind2] == 'Unknown':
            print(type(dataSet[ind][ind2]).__name__)
            dataSet = dataDiscrete(dataSet, ind2)
    labelsFull = labels[:-1]
    resultTree = createTree(dataSet, labelsFull[:], labelsFull)
    print(resultTree)

    testData = pd.read_csv("../SourceData/test.csv")
    testDataSet = testData.values.tolist()
    testLabelsEx = testData.columns.values.tolist()
    testDataSet = list(map(parseData, testDataSet))
    resultList = getResultFromTree(testDataSet, resultTree, testLabelsEx)

    realResult = pd.read_csv("../SourceData/gender_submission.csv")
    realResultList = list(map(lambda x: x[1], realResult.values.tolist()))
    rCount = 0
    for test, real in zip(resultList, realResultList):
        rCount += (1 if test == real else 0)
    rRate = rCount / float(len(resultList))
    print("测试正确率："  + str(rRate))
