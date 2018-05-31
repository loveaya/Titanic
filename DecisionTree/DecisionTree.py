import pandas as pd
import numpy as np


def getMinDic(dataSet, label):
    return {}


def chooseBestFeature(dataSet, labels):
    return list(labels)[0]


def createTree(dataSet, labels, labelsFull):
    if 1 == len(labels):
        print("yes")
        return getMinDic(dataSet, labels.pop())

    else:
        label = chooseBestFeature(dataSet, labels)
        labels.remove(label)
        labelIndex = labelsFull.index(label)

        cols  = len(dataSet)
        labelEntrys = []
        for ind in range(cols):
            labelEntrys.append(dataSet[ind][labelIndex])
        labelSet = set(labelEntrys)

        partedData = {}.fromkeys(labelSet)
        for entry in labelSet:
            partedData[entry] = createTree(list(filter(lambda x: x[labelIndex] ==  entry, dataSet)), labels.copy(), labelsFull)
        return partedData




if __name__ == '__main__':
    dataPath = "../SourceData/train.csv"
    data = pd.read_csv(dataPath)
    data = data.drop(["Name"], axis=1)
    # 对原始数据重排序
    # (m, n) = dataSet.shape
    labelsEx = data.columns.values.tolist()
    labels = labelsEx[0:1] + labelsEx[2:] + labelsEx[1:2]
    data = data[labels]
    dataSet = data.values.tolist()
    # dataSet = data.values.tolist()
    labelsFull = labels[:-1]
    # print(labels_full.index(labels_full[0]))

    result = createTree(dataSet, set(labelsFull), labelsFull)
    print(result)


