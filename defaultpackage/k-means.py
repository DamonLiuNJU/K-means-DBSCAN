#!/usr/bin/env python
# -*- coding: utf-8 -*-
import random as rd
import time


def K_Means(data, k, origin_label_list):
    begin_time = time.time()
    repeat_counter = 1

    label_history = []
    for i in range(len(data)):
        label_history.append([])

    while repeat_counter > 0:
        cluster_set = []
        for i in range(k):
            cluster_set.append([])
        center_set = get_random_seed_point(data, k)  # size==[k,1]
        while True:
            did_change = False
            for point in data:
                cluster_index = get_closest_cluster(center_set, point)
                if cluster_index != point.cluster_index:
                    if point.cluster_index > 0:
                        cluster_set[point.cluster_index].remove(point)
                    cluster_set[cluster_index].append(point)
                    point.cluster_index = cluster_index
                    did_change = True

            center_set = update_cluster_center(cluster_set)
            if not did_change:
                break;

        for i in range(len(data)):
            point = data[i]
            label_history[i].append(point.cluster_index)
            point.cluster_index = -1
        # print 'k-means counting down:', repeat_counter
        repeat_counter -= 1

    cluster_set = []
    for i in range(k):
        cluster_set.append([])

    for i in range(len(data)):
        final_label = get_final_label(label_history[i])
        data[i].cluster_index = final_label
        cluster_set[final_label].append(data[i])
    purity = tool.get_purity(cluster_set, len(data))
    fscore = tool.get_F_score(cluster_set, origin_label_list)
    print 'purity : ', purity
    print 'F-score : ', fscore
    end_time = time.time()
    print 'using time : %.2f' % (end_time - begin_time)
    return cluster_set, purity, fscore


def get_random_seed_point(data, k):
    center_set = []
    for i in range(k * 5):
        random_index = rd.random() * len(data)
        center_set.append(data[int(random_index)])
    from operator import itemgetter, attrgetter
    center_set = sorted(center_set, key=attrgetter('x', 'y'), reverse=False)
    seed_set = []
    for i in range(k):
        avg_x = 0
        avg_y = 0
        for j in range(5):
            avg_x += center_set[i * 5 + j].x
            avg_y += center_set[i * 5 + j].y
        avg_x /= 5
        avg_y /= 5
        from tool import Point
        seed_set.append(Point(avg_x, avg_y))
    return seed_set


def get_final_label(label_array):
    dic = {}
    for item in label_array:
        if dic.has_key(item):
            dic[item] += 1
        else:
            dic.setdefault(item, 1)
        pass
    # 找到出现次数最多的那个数,找到重数
    top_value = 0
    top_key = -1
    for key, value in dic.iteritems():
        if value > top_value:
            top_value = value
            top_key = key
        pass
    return top_key


def update_cluster_center(cluster_set):
    new_center_set = []
    for cluster in cluster_set:
        if len(cluster) == 0:
            continue
        avg_x = -1
        avg_y = -1
        for point in cluster:
            avg_x += point.x
            avg_y += point.y
        avg_x /= len(cluster)
        avg_y /= len(cluster)
        from tool import Point
        new_center_set.append(Point(avg_x, avg_y))
    return new_center_set


def distance(center, point):
    dis = pow(pow((center.x - point.x), 2) + pow((center.y - point.y), 2), 0.5)
    return dis


def get_closest_cluster(cluster_center_set, point):
    cluster_index = -1
    import sys
    min_distance = sys.maxint
    for i in range(len(cluster_center_set)):
        center = cluster_center_set[i]
        if distance(center, point) < min_distance:
            cluster_index = i
            min_distance = distance(center, point)
    return cluster_index


import tool
from matplotlib import pyplot as plt


def Kmeans_on_data_set_2():
    figure = plt.figure(1)
    for k in range(4, 12):
        x, y = tool.get_data_set_2()
        cluster_set, purity, fscore = K_Means(x, k, y)
        x_index = k / 4
        y_index = k % 4 + 1
        print x_index, ',', y_index
        tmp = plt.subplot(2, 4, k - 3)
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
        string = 'k:%d Purity:%.2f F-score:%.2f' % (k, purity, fscore)
        tmp.set_title(string)
        plt.scatter(x, y, c=T, s=25, alpha=0.4, marker='o')
    # plt.show()
# # print len(cluster_set)
# tool.show_cluster_set(cluster_set)


def Kmeans_on_data_set_1():
    figure = plt.figure(1)
    for k in range(12, 22):
        x, y = tool.get_data_set_1()
        cluster_set, purity, fscore = K_Means(x, k, y)
        # x_index = k / 5
        # y_index = k % 4 + 1
        # print x_index, ',', y_index
        tmp = plt.subplot(2, 5, k - 11)
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
        string = 'k:%d Purity:%.2f F-score:%.2f' % (k, purity, fscore)
        tmp.set_title(string)
        plt.scatter(x, y, c=T, s=25, alpha=0.4, marker='o')
    # plt.show()
    # print len(cluster_set)

print 'dataset 1'
Kmeans_on_data_set_1()
print 'dataset 2'
Kmeans_on_data_set_2()
