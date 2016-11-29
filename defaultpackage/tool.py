#!/usr/bin/env python
# -*- coding: utf-8 -*-


from matplotlib import pyplot as plt
import numpy as np


class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.visited = False
        self.in_cluster = False
        self.is_noise = False
        self.cluster_index = -1
        self.origin_label = -1


def get_data_set_1():
    path1 = '../data/dataset1.dat'
    path2 = '../data/dataset1-label.dat'
    dataset = []
    labelset = []
    x = []
    y = []
    file = open(path1, 'r')
    for line in file:
        # line.replace("\r",'')
        line = line.strip('\r\n')
        point = line.split(',')
        point[0] = int(point[0])
        point[1] = int(point[1])
        x.append(point[0])
        y.append(point[1])
        dataset.append(Point(point[0], point[1]))
    file.close()

    # figure = plt.figure()
    # T = np.arctan2(x, y)
    # # T:散点的颜色
    # # s：散点的大小
    # # alpha:是透明程度
    # plt.scatter(x, y, c=T, s=25, alpha=0.4, marker='o')
    # plt.show()

    file = open(path2, 'r')
    for line in file:
        line = line.strip('\r\n')
        label = int(line)
        labelset.append(label)

    for i in range(len(labelset)):
        dataset[i].origin_label = labelset[i]

    dic_count = count_array(labelset)

    # figure = plt.figure()
    # T = labelset
    # # T:散点的颜色
    # # s：散点的大小
    # # alpha:是透明程度
    # plt.scatter(x, y, c=T, s=25, alpha=0.4, marker='o')
    # plt.show()

    # figure = plt.figure()
    # plt.bar(dic_count.keys(),dic_count.values())
    # plt.show()

    # print len(dataset)
    # print len(labelset)
    return dataset, labelset


def count_array(mylist):
    myset = set(mylist)  # myset是另外一个列表，里面的内容是mylist里面的无重复 项
    dic = {}
    # for item in myset:
    # print("the %d has found %d" % (item, mylist.count(item)))
    from collections import Counter
    return Counter(mylist)


def get_data_set_2():
    path1 = '../data/dataset2.dat'
    path2 = '../data/dataset2-label.dat'
    x = []
    y = []
    dataset = []
    labelset = []
    file = open(path1, 'r')
    for line in file:
        # line.replace("\r",'')
        line = line.strip('\r\n')
        point = line.split(',')
        point[0] = float(point[0])
        point[1] = float(point[1])
        x.append(point[0])
        y.append(point[1])
        dataset.append(Point(point[0], point[1]))
    file.close()

    # figure = plt.figure()
    # T = np.arctan2(x, y)
    # # T:散点的颜色
    # # s：散点的大小
    # # alpha:是透明程度
    # plt.scatter(x, y, c=T, s=25, alpha=0.4, marker='o')
    # plt.show()

    file = open(path2, 'r')
    for line in file:
        line = line.strip('\r\n')
        label = int(line)
        labelset.append(label)

    for i in range(len(labelset)):
        dataset[i].origin_label = labelset[i]

    dic_count = count_array(labelset)

    # figure = plt.figure()
    # T = labelset
    # # T:散点的颜色
    # # s：散点的大小
    # # alpha:是透明程度
    # plt.scatter(x, y, c=T, s=25, alpha=0.4, marker='o')
    # plt.show()

    # figure = plt.figure()
    # plt.bar(dic_count.keys(), dic_count.values())
    # plt.show()

    # print len(dataset),dataset
    # print len(labelset),labelset
    return dataset, labelset

def show_cluster_set(cluster_set, static_counter=0):
    figure = plt.figure(static_counter)
    T = []
    x = []
    y = []
    for cluster in cluster_set:
        for point in cluster:
            T.append(point.cluster_index)
            x.append(point.x)
            y.append(point.y)
    # T:散点的颜色
    # s：散点的大小
    # alpha:是透明程度
    plt.scatter(x, y, c=T, s=25, alpha=0.4, marker='o')
    plt.show()


def get_purity(cluster_set, total_count):
    sum = 0
    for cluster in cluster_set:
        sum += (float(len(cluster)) / float(total_count)) * get_purity_for_cluster(cluster)
    return sum


def get_purity_for_cluster(cluster):
    if len(cluster) == 0:
        return 0
    # according to http://blog.csdn.net/vernice/article/details/46467449
    dic = {}
    for i in range(len(cluster)):
        point = cluster[i]
        if dic.has_key(point.origin_label):
            dic[point.origin_label] += 1
        else:
            dic.setdefault(point.origin_label, 1)
        pass
    max_value = -1
    for key, value in dic.iteritems():
        if value > max_value:
            max_value = value
    return float(max_value) / float(len(cluster))


def get_F_score(cluster_set, origin_label):
    # according to https://www.zhihu.com/question/19635522
    J = len(cluster_set)
    dic = count_array(origin_label)
    I = len(dic.keys())
    sum = 0
    for i in range(I):
        for j in range(J):
            if len(cluster_set[j])==0:
                precision = 0
                recall = 0
            else :
                precision = get_count_from_cluster(cluster_set[j], i+1) * 1.0 / len(cluster_set[j])*1.0
                recall = get_count_from_cluster(cluster_set[j], i+1) * 1.0 / float(dic.get((i+1)))*1.0
            if precision + recall == 0:
                f = 0
            else:
                f = 2 * precision * recall / (precision + recall)
            sum += f * dic.get((i+1))
    sum /= len(origin_label)
    return sum


def get_count_from_cluster(cluster, origin_label):
    counter = 0
    for point in cluster:
        if point.cluster_index == origin_label:
            counter += 1
    return counter


def get_precision():
    return 0.0


def get_recall():
    return 0.0

# get_data_set_1()
# get_data_set_2()
