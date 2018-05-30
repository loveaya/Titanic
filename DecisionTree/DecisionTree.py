import pandas as pd
import numpy as np


def getMinDic(dataSet, label):
    pass


def chooseBestFeature(dataSet, labels):
    pass


def createTree(dataSet, labels, labels_full):
    if 1 == len(labels):
        return getMinDic(dataSet, labels[0])
    else:
        label = chooseBestFeature(dataSet, labels)
        labels = labels.pop(labels.index(label))
        createTree(dataSet, labels, labels_full)


if __name__ == '__main__':
    dataPath = "../SourceData/train.csv"
    data = pd.read_csv(dataPath)
    data.drop(["Name"], axis=1)
    # 对原始数据重排序
    labels = data.columns.values.tolist()
    labels = labels[0:1] + labels[2:] + labels[1:2]
    data = data[labels]
    dataSet = data.values.tolist()
    labels_full = labels[:-1]
    # print(labels_full.index(labels_full[0]))
    
    # decisionTree = createTree(dataSet, labels_full, labels_full)

