#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@Date: 2022/02/24 20:13:16
@Author: rojer
"""
import operator
import os
import numpy as np
import read
import sys


def produce_item_sim(file_path):
    if not os.path.exists(file_path):
        return {}

    linenum = 0
    fp = open(file_path)
    record = {}
    for line in fp:
        if linenum == 0:
            linenum += 1
            continue
        items = line.strip().split(" ")
        if len(items) < 129:
            continue
        item_id, item_vec = items[0], items[1:]
        if item_id == "</s>":
            continue
        record[item_id] = [float(vec) for vec in item_vec]

    return record


def get_sim_from_sim_item_vec(item_id, item_vec, count=10):
    if item_id not in item_vec:
        print("item id: %s not exist in item_vec" % (item_id))
        return {}

    record = {}
    for i in item_vec:
        if i == item_id:
            continue
        # 用cos距离公式计算两个item的距离

        fenmu = np.linalg.norm(item_vec[item_id]) * np.linalg.norm(item_vec[i])
        if fenmu == 0:
            record[i] = 0
        else:
            record[i] = round(np.dot(item_vec[item_id], item_vec[i]) / fenmu, 4)

    return {
        i: r
        for i, r in sorted(record.items(), key=operator.itemgetter(1), reverse=True)[
            :count
        ]
    }


if __name__ == "__main__":
    print(sys.argv)
    if len(sys.argv) < 3:
        print("python produce_item_sim.py item_id item_vec_path")
        sys.exit()

    item_id = sys.argv[1]
    item_vec_path = sys.argv[2]
    item_vec = produce_item_sim(item_vec_path)
    sim_items = get_sim_from_sim_item_vec(item_id, item_vec)
    infos = read.get_item_info("../data/movies.txt")
    print("target item info:")
    print(infos[item_id])
    print("===================")
    print("recommend list:")
    for itemid, rating in sim_items.items():
        print(infos[itemid], rating)
