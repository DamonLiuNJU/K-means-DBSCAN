#!/usr/bin/env python
# -*- coding: utf-8 -*-
import tool
import random as rd
import time
import sys
from progressbar import AnimatedMarker, Bar, BouncingBar, Counter, ETA, \
    AdaptiveETA, FileTransferSpeed, FormatLabel, Percentage, \
    ProgressBar, ReverseBar, RotatingMarker, \
    SimpleProgress, Timer


def DBSCAN(data, origin_label_list, r, MinPts):
    begin_time = time.time()
    clusterset = []
    # for point in data:
    # point.visited = False

    # pbar = ProgressBar(maxval=101).start()

    total_count = len(data)
    unvisited_point_count = len(data)
    # pbar.start()
    while unvisited_point_count > 0:
        random_index = len(data) * rd.random()
        random_point = data[int(random_index)]
        unvisited_point_count = mark_point_visited(random_point, unvisited_point_count, total_count)

        neighbor_points = get_neighbor_points(data, random_point, r)
        if len(neighbor_points) >= MinPts:
            cluster = []
            add_point_to_cluster(random_point, cluster)
            for point in neighbor_points:
                if not point.visited:
                    unvisited_point_count = mark_point_visited(point, unvisited_point_count, total_count)

                    tmp_set = get_neighbor_points(data, point, r)
                    if len(tmp_set) >= MinPts:
                        neighbor_points = neighbor_points + tmp_set
                if not point.in_cluster:
                    add_point_to_cluster(point, cluster)
            clusterset.append(cluster)
        else:
            random_point.is_noise = True
    # pbar.finish()

    for cluster_index in range(len(clusterset)):
        for point in clusterset[cluster_index]:
            point.cluster_index = cluster_index
    purity = tool.get_purity(clusterset, len(data))
    Fscore = tool.get_F_score(clusterset, origin_label_list)
    # print 'purity : ', purity
    # print 'F-score : ', Fscore
    end_time = time.time()
    print 'using time : %.2f' % (end_time - begin_time)
    return clusterset, purity, Fscore


def add_point_to_cluster(point, cluster):
    cluster.append(point)
    point.cluster_index = cluster
    point.in_cluster = True


def mark_point_visited(point, unvisited_point_count, total_count):
    point.visited = True
    unvisited_point_count -= 1
    percentage = (1 - (float(unvisited_point_count) / float(total_count))) * 100
    # if int(percentage) <= 100:
    # pbar.update(int(percentage))
    return unvisited_point_count


def get_neighbor_points(data, center, radius):
    result = []
    for point in data:
        if point != center:
            distance = pow(pow((center.x - point.x), 2) + pow((center.y - point.y), 2), 0.5)
            if distance <= radius:
                result.append(point)

    return result


from matplotlib import pyplot as plt


def DBSCAN_on_data_set_2():
    for r in range(10, 15):
        figure = plt.figure(r - 9)
        counter = 1
        for MinPts in range(11, 19):
            print 'using param : ', r, ':', MinPts
            x, y = tool.get_data_set_2()
            cluster_set, purity, fscore = DBSCAN(x, y, r, MinPts)
            tmp = plt.subplot(2, 4, counter)
            counter += 1
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
            string = 'r:%d MinPts:%d k:%d\nPurity:%.2f F-score:%.2f' % (r, MinPts, len(cluster_set), purity, fscore)
            tmp.set_title(string)
            plt.scatter(x, y, c=T, s=25, alpha=0.4, marker='o')
    plt.show()
    #
    # tool.show_cluster_set(cluster_set)
    # print len(cluster_set)


def DBSCAN_on_data_set_1():
    for r in range(100000, 200000, 25000):
        figure = plt.figure(r - 99999)
        counter = 1
        for MinPts in range(9, 11):
            print 'param : ', r, ':', MinPts
            x, y = tool.get_data_set_1()
            cluster_set, purity, fscore = DBSCAN(x, y, r, MinPts)
            tmp = plt.subplot(1, 2, counter)
            counter += 1
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
            string = 'r:%d MinPts:%d k:%d\nPurity:%.2f F-score:%.2f' % (r, MinPts, len(cluster_set), purity, fscore)
            tmp.set_title(string)
            plt.scatter(x, y, c=T, s=25, alpha=0.4, marker='o')
    plt.show()


DBSCAN_on_data_set_1()
# DBSCAN_on_data_set_2()
